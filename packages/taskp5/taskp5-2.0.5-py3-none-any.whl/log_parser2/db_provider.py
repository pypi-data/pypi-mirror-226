import random
from abc import abstractmethod, ABCMeta
from collections import Counter
from enum import Enum
from typing import Dict, List, Tuple, NamedTuple

import mysql.connector
import psycopg2
import pymongo
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extras import execute_values
from mysql.connector.cursor import MySQLCursor

from log_parser2.logging import logger


class DBAggregation(NamedTuple):
    class Direction(Enum):
        MIN = 'ASC'
        MAX = 'DESC'

    direction: Direction
    top_count: int


class DBProvider(metaclass=ABCMeta):
    def __init__(self, db_config: Dict, db_name: str = None, table_name: str = None):
        self._db_config = db_config
        self._db_name = db_name
        self._table_name = table_name
        self._is_temp_table: bool = table_name is not None

        self._connection = self.connect(db_config)
        self._instantiate_()

    @staticmethod
    @abstractmethod
    def connect(db_config: Dict):
        pass

    @staticmethod
    @abstractmethod
    def _get_fields_() -> Dict:
        pass

    def _instantiate_(self):
        if self._db_name:
            self.create_db(self._db_name)

        self._table_name = self._table_name if self._table_name \
            else f'log_data_{random.randint(1000, 10000)}'

        fields = self._get_fields_()

        self.create_table(self._table_name, fields, self._db_name, True)

    def close(self):
        if self._db_name:
            self.drop_db(self._db_name)
        elif self._is_temp_table:
            self.drop_table(self._table_name, self._db_name)

        self._connection.close()

    @abstractmethod
    def create_db(self, name: str):
        pass

    @abstractmethod
    def drop_db(self, name: str):
        pass

    @abstractmethod
    def create_table(self, name: str, fields: Dict, db_name: str = None, temporary: bool = False):
        pass

    @abstractmethod
    def drop_table(self, name: str, db_name: str = None):
        pass

    @abstractmethod
    def insert(self, data: List[Tuple], table_name: str = None, db_name: str = None):
        pass

    @abstractmethod
    def select(self, aggregation: DBAggregation, table_name: str = None, db_name: str = None) -> List[Tuple]:
        pass


class MYSQLProvider(DBProvider):
    def __get_cursor__(self) -> MySQLCursor:
        try:
            cursor = self._connection.cursor()
        except mysql.connector.errors.OperationalError as _:
            self._connection = self.connect(self._db_config)
            cursor = self._connection.cursor()

        return cursor

    def _execute_(self, query: str, data=None):
        cursor = self.__get_cursor__()

        cursor.execute(query, data)
        self._connection.commit()
        cursor.close()

    def _execute_many_(self, query: str, data: List):
        cursor = self.__get_cursor__()

        cursor.executemany(query, data)
        self._connection.commit()
        cursor.close()

    def __use_query__(self, db_name: str):
        db_name = db_name if db_name else self._db_name
        query = f"""
            {f'USE {db_name};' if db_name else ''}
        """

        self._execute_(query)

    @staticmethod
    def connect(db_config: Dict):
        return mysql.connector.connect(**db_config)

    @staticmethod
    def _get_fields_() -> Dict:
        return dict(id='INT NOT NULL AUTO_INCREMENT PRIMARY KEY',
                    selection='VARCHAR(380)',
                    aggregate='VARCHAR(380) NULL',
                    counter='INT')

    def create_db(self, name: str):
        query = f"""
            CREATE DATABASE IF NOT EXISTS {name}
        """

        self._execute_(query)

        logger.debug(f'A new database "{name}" was created in MySQL.')

    def drop_db(self, name: str):
        query = f"""
            DROP DATABASE IF EXISTS {name}
        """

        self._execute_(query)

        logger.debug(f'The database "{name}" was dropped in MySQL.')

    def create_table(self, name: str, fields: Dict, db_name: str = None, temporary: bool = False):
        self.__use_query__(db_name)

        fields_str = ',\n'.join([f'{name} {field_type}' for name, field_type in fields.items()])

        query = f"""
            CREATE {'TEMPORARY ' if temporary else ''}TABLE IF NOT EXISTS {name} (
                {fields_str}, INDEX idx_selection_aggregate_counter (selection, aggregate, counter)
            ) ENGINE = InnoDB;
        """

        self._execute_(query)

        logger.debug(f'A new table "{name}" was created in MySQL.')

    def drop_table(self, name: str, db_name: str = None):
        self.__use_query__(db_name)

        query = f"""
            DROP TABLE IF EXISTS {name};
        """

        self._execute_(query)

        logger.debug(f'The table "{name}" was dropped in MySQL.')

    def insert(self, data: List[Tuple], table_name: str = None, db_name: str = None):
        if len(data) > 10000:
            self.insert(data[10000:], table_name, db_name)
            data = data[:10000]

        self.__use_query__(db_name)

        # noinspection DuplicatedCode
        data = [
            (
                el[0][:380],
                list(el[1].keys())[0][:380] if type(el[1]) is Counter else el[1],
                list(el[1].values())[0] if type(el[1]) is Counter else el[1],
            )
            for el in data
        ]

        query = f"""
            INSERT INTO {table_name if table_name else self._table_name} (selection, aggregate, counter) VALUES
            {", ".join("(%s, %s, %s)" for _ in data)}
        """

        # Flatten the data list to create a single list of values
        flat_data = [value for row in data for value in row]

        self._execute_(query, flat_data)

        logger.info(f'{len(data)} rows were inserted in MySQL.')

    def select(self, aggregation: DBAggregation, table_name: str = None, db_name: str = None) -> List[Tuple]:
        self.__use_query__(db_name)

        query = f"""
            SELECT *
            FROM
                (SELECT
                    selection,
                    SUM(counter) AS sum
                FROM
                    {table_name if table_name else self._table_name}
                GROUP BY
                    selection, counter) as aggregation
            {f'''ORDER BY
                sum {aggregation.direction.value}''' if aggregation else ''}
            {f'LIMIT {aggregation.top_count}' if aggregation and aggregation.top_count else ''}
        """

        cursor = self.__get_cursor__()
        cursor.execute(query)

        result = cursor.fetchall()

        self._connection.commit()
        cursor.close()

        logger.info(f'{len(result)} rows were selected from '
                    f'{table_name if table_name else self._table_name} in MySQL.')

        return result


class PostgresProvider(DBProvider):
    def __execute__(self, query: str, data: List = None, isolation_level: int = None):
        if isolation_level is not None:
            self._connection.set_isolation_level(isolation_level)

        cursor = self._connection.cursor()
        cursor.execute(query, data)
        self._connection.commit()
        cursor.close()

    def __execute_many__(self, query: str, data: List, isolation_level: int = None):
        if isolation_level is not None:
            self._connection.set_isolation_level(isolation_level)

        cursor = self._connection.cursor()
        execute_values(cursor, query, data)
        self._connection.commit()
        cursor.close()

    def __change_db__(self, db_name: str):
        self._connection.close()
        self._db_config['database'] = db_name

        self._connection = self.connect(self._db_config)

    def _instantiate_(self):
        if self._db_name:
            self.__initial_db = self._db_config.get('database', None)

        super()._instantiate_()

    def close(self):
        if self._db_name and self.__initial_db:
            self.__change_db__(self.__initial_db)
            self.drop_db(self._db_name)
        elif self._is_temp_table:
            self.drop_table(self._table_name, self._db_name)

        self._connection.close()

    @staticmethod
    def connect(db_config: Dict):
        return psycopg2.connect(**db_config)

    @staticmethod
    def _get_fields_() -> Dict:
        return dict(id='SERIAL PRIMARY KEY',
                    selection='VARCHAR(500)',
                    aggregate='VARCHAR(500) NULL',
                    counter='INT')

    def create_db(self, name: str):
        query = f"""
            CREATE DATABASE {name};
        """

        try:
            self.__execute__(query, isolation_level=ISOLATION_LEVEL_AUTOCOMMIT)
        except psycopg2.Error as e:
            if e.pgcode != '42P04':  # DB exists
                raise e

        self.__change_db__(name)

        logger.debug(f'A new database "{name}" was created in Postgres.')

    def drop_db(self, name: str):
        query = f"""
            DROP DATABASE {name}; 
        """

        try:
            self.__execute__(query, isolation_level=ISOLATION_LEVEL_AUTOCOMMIT)
        except psycopg2.Error as e:
            if e.pgcode != '42P04':  # DB does not exist
                raise e

        logger.debug(f'The database "{name}" was dropped in Postgres.')

    def create_table(self, name: str, fields: Dict, db_name: str = None, temporary: bool = False):
        if db_name:
            self.__change_db__(db_name)

        fields_str = ',\n'.join([f'{name} {field_type}' for name, field_type in fields.items()])

        query = f"""
            CREATE {'TEMPORARY ' if temporary else ''}TABLE IF NOT EXISTS {name} (
                {fields_str}
            )
        """

        self.__execute__(query)

        logger.debug(f'A new table "{name}" was created in Postgres.')

        query = f"""
            CREATE INDEX IF NOT EXISTS idx_selection_aggregate_counter ON {name} (selection, aggregate, counter)
        """

        self.__execute__(query)

        logger.debug(f'A new table index idx_selection_aggregate_counter was created in Postgres.')

    def drop_table(self, name: str, db_name: str = None):
        if db_name:
            self.__change_db__(db_name)

        query = f"""
            DROP TABLE IF EXISTS {name};
        """

        self.__execute__(query)

        logger.debug(f'The table "{name}" was dropped in Postgres.')

    def insert(self, data: List[Tuple], table_name: str = None, db_name: str = None):
        if len(data) > 10000:
            self.insert(data[10000:], table_name, db_name)
            data = data[:10000]

        if db_name:
            self.__change_db__(db_name)

        # noinspection DuplicatedCode
        data = [
            (
                el[0][:380],
                list(el[1].keys())[0][:380] if type(el[1]) is Counter else el[1],
                list(el[1].values())[0] if type(el[1]) is Counter else el[1],
            )
            for el in data
        ]

        query = f"""
            INSERT INTO {table_name if table_name else self._table_name} (selection, aggregate, counter) VALUES
            {", ".join("(%s, %s, %s)" for _ in data)}
        """

        # Flatten the data list to create a single list of values
        flat_data = [value for row in data for value in row]

        self.__execute__(query, flat_data)

        logger.info(f'{len(data)} rows were inserted in Postgres.')

    def select(self, aggregation: DBAggregation, table_name: str = None, db_name: str = None) -> List[Tuple]:
        if db_name:
            self.__change_db__(db_name)

        query = f"""
                SELECT *
                FROM
                    (SELECT
                        selection,
                        SUM(counter) AS sum
                    FROM
                        {table_name if table_name else self._table_name}
                    GROUP BY
                        selection, counter) as aggregation
                {f'''ORDER BY
                    sum {aggregation.direction.value}''' if aggregation else ''}
                {f'LIMIT {aggregation.top_count}' if aggregation and aggregation.top_count else ''}
            """

        cursor = self._connection.cursor()
        cursor.execute(query)

        result = cursor.fetchall()

        self._connection.commit()
        cursor.close()

        logger.info(f'{len(result)} rows were selected from '
                    f'{table_name if table_name else self._table_name} in Postgres.')

        return result


class MongoProvider(DBProvider):
    @staticmethod
    def connect(db_config: Dict):
        return pymongo.MongoClient(**db_config)

    @staticmethod
    def _get_fields_() -> Dict:
        return dict(id='unique')

    def create_db(self, name: str):
        _ = self._connection[name]

        logger.debug(f'A new database "{name}" was created in MongoDB.')

    def drop_db(self, name: str):
        self._connection.drop_database(name)

        logger.debug(f'The database "{name}" was dropped in MongoDB.')

    def create_table(self, name: str, fields: Dict, db_name: str = None, temporary: bool = False):
        dbase = self._connection[db_name] if db_name else self._connection.get_default_database()

        if any([el for el in dbase.list_collection_names() if el == name]):
            return dbase[name]

        collection = dbase.create_collection(name, capped=True, size=1000000)  # default size is 1 MB

        indexes = [
            pymongo.IndexModel(
                [(field, pymongo.DESCENDING if 'desc' in options.lower() else pymongo.ASCENDING,)],
                name=f'index_{field}',
                unique='unique' in options.lower()
            )
            for field, options in fields.items()
            if 'unique' in options.lower() or 'indexed' in options.lower()
        ]

        if indexes:
            collection.create_indexes(indexes)

        logger.debug(f'A new table "{name}" was created in MongoDB.')

    def drop_table(self, name: str, db_name: str = None):
        dbase = self._connection[db_name] if db_name else self._connection.get_default_database()
        dbase.drop_collection(name)

        logger.debug(f'The table "{name}" was dropped in MongoDB.')

    def insert(self, data: List[Tuple], table_name: str = None, db_name: str = None):
        dbase = self._connection[db_name] if db_name else self._connection.get_default_database()
        collection = dbase[table_name if table_name else self._table_name]

        query_data = [
            {
                'selection': el[0],
                'aggregate': key,
                'counter': value,
            }
            for el in data if type(el[1]) is Counter
            for key, value in el[1].items()
        ]

        query_data.extend([
            {
                'selection': el[0],
                'aggregate': el[1],
                'counter': el[1],
            }
            for el in data if type(el[1]) is not Counter
        ])
        collection.insert_many(query_data)

        logger.info(f'{len(data)} rows were inserted in MongoDB.')

    def select(self, aggregation: DBAggregation, table_name: str = None, db_name: str = None) -> List[Tuple]:
        dbase = self._connection[db_name] if db_name else self._connection.get_default_database()
        collection = dbase[table_name if table_name else self._table_name]

        pipeline = [
            # Group by selection and counter and calculate the sum
            {"$group": {
                "_id": {"selection": "$selection", "counter": "$counter"},
                "sum": {"$sum": "$counter"}
            }},
            {"$project": {
                "_id": 0,
                "selection": "$_id.selection",
                "sum": 1
            }}
        ]

        if aggregation:
            # Sort by sum in the given direction
            pipeline.append({"$sort": {"sum": -1 if aggregation.direction.value == "DESC" else 1}})

            if aggregation.top_count:  # Limit by the top count
                pipeline.append({"$limit": int(aggregation.top_count)})

        result = list(collection.aggregate(pipeline))

        logger.info(f"{len(result)} rows were selected from "
                    f"{table_name if table_name else self._table_name} in MongoDB.")

        return [(row.get('selection', ''), row.get('sum', 0), ) for row in result]


class DBTypes(Enum):
    MYSQL = MYSQLProvider
    PostgresSQL = PostgresProvider
    MongoDB = MongoProvider

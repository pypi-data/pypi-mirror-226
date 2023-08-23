import os
import sys
from dotenv import load_dotenv
load_dotenv()
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from typing import Any


current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, '..', 'circles_local_database_python')
sys.path.append(src_path)
from circles_local_database_python.connector import Connector
DATABASE_WITHOUT_ORM_PYTHON_PACKAGE_COMPONENT_ID = 13
DATABASE_WITHOUT_ORM_PYTHON_PACKAGE_COMPONENT_NAME = 'circles_local_database_python\generic_crud'
DEVELOPER_EMAIL='sahar.g@circ.zone'
obj={
  'component_id' : DATABASE_WITHOUT_ORM_PYTHON_PACKAGE_COMPONENT_ID,
  'component_name' : DATABASE_WITHOUT_ORM_PYTHON_PACKAGE_COMPONENT_NAME,
  'component_category' : LoggerComponentEnum.ComponentCategory.Code.value,
  'developer_email' : DEVELOPER_EMAIL
}
logger=Logger.create_logger(object=obj)

class GenericCRUD:

    def __init__(self):
        pass

    @staticmethod
    def get_records_by_id(schema_name: str, table_name: str, id: str, id_col_name: str = "id")->Any:
        """
        This method gets the data from the database for the given id and table name.
        :param db_name: The name of the database
        :param table_name: The name of the table
        :param id: The id of the data
        :param id_col_name: The name of the id column in the table (default: id)
        :return: The data from the database
        """
        obj={
            'schema_name':schema_name,
            'table_name':table_name,
            'id':id,
            'id_col_name': id_col_name
        }
        logger.start(object=obj)
        try:
            # Connect to the database
            connection = Connector.get_connection(schema_name=schema_name)
        except Exception as e:
            message = "error: connection to the database failed"
            logger.exception(message, object=e)
            return {'message': message}
        try:
            # Use the table name
            connection.cursor().execute(f"USE {schema_name}")
            if id_col_name == "":
                # If the id column name is empty, select all the data from the table
                connection.cursor().execute(f"SELECT * FROM {table_name}")
            else:
                # Else, select the data from the table where the id column name is equal to the id
                connection.cursor().execute(
                    f"SELECT * FROM {table_name} WHERE {id_col_name} = {id}")
            # Get the result
            result = connection.cursor().fetchall()
            # Close the connection
            connection.close()
            # Return the result
            logger.end(object={'result':result})
            return result
        except Exception as e:
            message = "error: connection to the database failed"
            logger.exception(message, object=e)
            logger.end(object={'message': message})
            return {'message': message}

    @staticmethod
    def get_records_by_where_condition(schema_name: str, table_name: str, where_condition: str = "")-> Any:
        """
        This method gets the data from the database for the given table name.
        :param db_name: The name of the database
        :param table_name: The name of the table
        :param where_cond: The where condition for the query (default: "")
        :return: The data from the database for the given table name and where condition
        """
        obj={
            'schema_name':schema_name,
            'table_name': table_name,
            'where_condition': where_condition
        }
        logger.start(object=obj)
        try:
            # Connect to the database
            connection = Connector.get_connection(schema_name=schema_name)
        except Exception as e:
            # If the connection fails, write an error message to the log
            message = "error: connection to the database failed"
            logger.exception(message, object=e)
            return {'message': message}
        try:
            # Select the database
            connection.cursor().execute(f"USE {schema_name}")
            # Get data from the table
            if where_condition == "":
                connection.cursor().execute(f"SELECT * FROM {table_name}")
            else:
                connection.cursor().execute(
                    f"SELECT * FROM {table_name} WHERE {where_condition}")
            result = connection.cursor().fetchall()
            connection.close()
            logger.end(object={'result':result})
            return result
        except Exception as e:
            # If the database query fails, write an error message to the log
            message = "error: failed to get data from the database"
            logger.exception(message, object=e)
            logger.end(object={'message': message})
            return {'message': message}

    @staticmethod
    def insert(schema_name: str, table_name: str, json_data)->Any:
        """
        This method inserts the data into the database for the given table name.
        :param db_name: The name of the database
        :param table_name: The name of the table
        :param json_data: The data to insert into the database (default: None)
        :return: The message and the ids of the inserted data
        """
        obj={
            'schema_name':schema_name,
            'table_name': table_name,
            'json_data': json_data
        }
        logger.start(object=obj)
        try:
            connection = Connector.get_connection(schema_name=schema_name)
        except Exception as e:
            message = "error: connection to the database failed"
            logger.exception(message, object=e)
            return {'message': message}
        added_ids = []

        try:
            connection.cursor().execute(f"USE {schema_name}")
            if not json_data:
                message = 'No data provided'
                logger.error(message)
                return {'message': message}

            # Extract the data from the json
            for row, data in json_data.items():
                for param in data:
                    keys = ','.join(param.keys())
                    values = ['"{}"'.format(y) for y in param.values()]
                    values = ','.join(values)
                    query = f"INSERT INTO {table_name} ({keys}) VALUES ({values})"
                    connection.cursor().execute(query)
                    added_ids.append(connection.cursor().lastrowid())
            # close connectin
            connection.commit()
            connection.close()
            logger.end(object={'message': 'Contacts added successfully', 'contacts ids': added_ids})
            return {'message': 'Contacts added successfully', 'contacts ids': added_ids}
        except Exception as e:
            message = "error: connection to the database failed"
            logger.exception(message, object=e)
            logger.end(object={'message': message})
            return {'message': message}

    @staticmethod
    def update(schema_name: str, table_name: str, data_json, id_column_name: str)->Any:
        """
        This method updates the data in the database for the given table name.
        :param db_name: The name of the database
        :param table_name: The name of the table
        :param json_data: The data to update in the database
        :param id_col_name: The name of the id column in the table (default: id)
        :return: The message and the ids of the updated data
        """
        obj={
            'schema_name':schema_name,
            'table_name': table_name,
            'id_column_name': id_column_name
        }
        logger.start(object=obj)
        try:
            connection = Connector.get_connection(schema_name=schema_name)
        except Exception as e:
            message = "error: connection to the database failed"
            logger.exception(message, object=e)
            return {'message': message}

        updated_ids = []
        try:
            connection.cursor().execute(f"USE {schema_name}")
            if not data_json:
                message = 'No data provided'
                logger.error(message)
                return {'message': message}

            # Extract the data from the json
            for row, data in data_json.items():
                for param in data:
                    keys = ','.join(param.keys())
                    values = ['"{}"'.format(y) for y in param.values()]
                    values = ','.join(values)
                    query = f" UPDATE {table_name} SET {keys} = {values} WHERE {id_column_name} = {param['id']}"
                    connection.cursor().execute(query)
                    updated_ids.append(connection.cursor().lastrowid())
            # close connectin
            connection.commit()
            connection.close()
            logger.end('updated successfully', object=updated_ids)
            return {'message': 'Contacts updated successfully', 'contacts ids': updated_ids}
        except Exception as e:
            message = "error: failed to update data in the database"
            logger.exception(message, object=e)
            return {'message': message}

    @staticmethod
    def delete(schema_name: str, table_name: str, data_json, id_column_name: str)->None:
        """
        This method deletes the data from the database for the given table name.
        :param db_name: The name of the database
        :param table_name: The name of the table
        :param json_data: The data to delete from the database
        :param id_col_name: The name of the id column in the table (default: id)
        :return: The message and the ids of the deleted data
        """
        obj={
            'schema_name':schema_name,
            'table_name': table_name,
            'id_column_name': id_column_name
        }
        logger.start(object=obj)
        try:
            connection = Connector.get_connection(schema_name=schema_name)
        except Exception as e:
            message = "error: connection to the database failed"
            logger.exception(message, object=e)
            return {'message': message, 'error': str(e)}

        deleted_ids = []
        try:
            connection.cursor().execute(f"USE {schema_name}")
            if not data_json:
                message = 'No data provided'
                logger.error(message)
                logger.end()
                return {'message': message}

            id = data_json[id_column_name]
            query = f"UPDATE {table_name} SET end_timestamp = NOW() WHERE id = {id};"
            cursor=connection.cursor()
            cursor.execute(query)
            deleted_ids.append(connection.cursor().lastrowid())
            connection.commit()
            connection.close()
            logger.end('Deleted successfully',object={'contacts ids': deleted_ids})
            return {'message': 'Deleted successfully', 'contacts ids': deleted_ids}
        except Exception as e:
            message = "error: failed to delete data from the database"
            logger.exception(message, object=e)
            logger.end(message)
            return {'message': message, 'error': str(e)}

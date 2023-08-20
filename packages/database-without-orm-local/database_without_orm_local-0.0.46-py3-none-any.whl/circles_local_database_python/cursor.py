import os
import sys
from dotenv import load_dotenv
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.LoggerLocal import logger
load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, '..', 'circles_local_database_python')
sys.path.append(src_path)
DATABASE_WITHOUT_ORM_PYTHON_PACKAGE_COMPONENT_ID = 13
COMPONENT_NAME = 'circles_local_database_python/cursor.py'
DEVELOPER_EMAIL='valeria.e@circ.zone and idan.a@circ.zone'
logger=logger(component_id=DATABASE_WITHOUT_ORM_PYTHON_PACKAGE_COMPONENT_ID,component_name=COMPONENT_NAME,component_category=LoggerComponentEnum.ComponentCategory.Code,developer_email=DEVELOPER_EMAIL)
class Cursor():


    def __init__(self, cursor) -> None:
        self.cursor = cursor
    def execute(self, sql_statement, sql_parameters=None):
        if sql_parameters:
            quoted_parameters = [
                "'" + str(param) + "'" for param in sql_parameters]
            formatted_sql = sql_statement % tuple(quoted_parameters)
            sql_parameters_str = ", ".join(quoted_parameters)
        else:
            formatted_sql = sql_statement
            sql_parameters_str = "None"
        EXECUTE_METHOD_NAME = 'database-without-orm-local-python-package cursor.py execute()'
        logger.start(EXECUTE_METHOD_NAME, object={
            "full_sql_query": formatted_sql,
            "sql_parameters": sql_parameters_str,
            "sql_statement": sql_statement
        })
        self.cursor.execute(sql_statement, sql_parameters)
        logger.end(EXECUTE_METHOD_NAME)

    def fetchall(self):
        logger.start()
        result = self.cursor.fetchall()
        logger.end()
        return result

    def fetchone(self):
        logger.start()
        result = self.cursor.fetchone()
        logger.end()
        return result

    def description(self):
        logger.start()
        result = self.cursor.description
        logger.end()
        return result

    def lastrowid(self):
        logger.start()
        result = self.cursor.lastrowid
        logger.end()
        return result

    def close(self):
        logger.start()
        self.cursor.close()
        logger.end()

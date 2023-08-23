import sys
import os
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_directory, '..', 'db'))
from circles_local_database_python.connector import Connector
from dotenv import load_dotenv
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.Logger import Logger
from datetime import datetime

load_dotenv()
EXTERNAL_USER_LOCAL_PYTHON_PACKAGE_COMPONENT_ID = 115
EXTERNAL_USER_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME='external_user_local'
DEVELOPER_EMAIL="idan.a@circ.zone"
object_init = {
    'component_id':EXTERNAL_USER_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
    'component_name':EXTERNAL_USER_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
    'component_category':LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email':DEVELOPER_EMAIL,
}
logger=Logger.create_logger(object=object_init)



class ExternalUserDb:
    def __init__(self):
        pass

    @staticmethod
    def insert_or_update_external_user_access_token(username, profile_id, system_id, access_token):
        try:
            object_start = {
                'username': username,
                'profile_id': profile_id,
                'access_token': access_token
            }
            logger.start(object=object_start)
            connection = Connector.get_connection('external_user')
            query_insert_external = "INSERT INTO external_user.external_user_table (system_id,username,access_token) VALUES (%s,%s,%s)"
            values = (system_id, username, access_token)
            cursor = connection.cursor()
            cursor.execute(query_insert_external, values)
            id_new = cursor.lastrowid()
            values = (id_new, profile_id)
            query_insert_external_user_profile = "INSERT INTO external_user_profile.external_user_profile_table (external_user_id,profile_id) VALUES (%s,%s)"
            cursor = connection.cursor()
            cursor.execute(query_insert_external_user_profile, values)
            connection.commit()
            cursor.close()
            object_info = {
                'username': username,
                'system_id': system_id,
                'profile_id': profile_id,
                'access_token': access_token,
            }
            logger.info("external user inserted",object=object_info)
        except Exception as error:
            logger.exception(object=error)
        logger.end(object={})

    @staticmethod
    def get_access_token(username, profile_id, system_id):
        access_token = None
        try:
            object_start = {
                'username': username,
                'profile_id': profile_id,
                'system_id': system_id
            }
            logger.start(object=object_start)
            connection = Connector.get_connection('external_user')
            query_get = "SELECT access_token FROM external_user.external_user_view as eu join external_user_profile.external_user_profile_table as eup on eu.external_user_id=eup.external_user_id WHERE eu.username=%s AND eu.system_id=%s And eup.profile_id=%s"
            cursor = connection.cursor()
            cursor.execute(query_get, (username, system_id, profile_id))
            access_token = cursor.fetchone()
            cursor.close()
        except Exception as error:
            logger.exception(object=error)
        logger.end(object={'access_token': access_token})
        return access_token
    
    @staticmethod
    def get_all_tokens_by_system_id(system_id):
        # good for update users details by system
        access_tokens = None
        try:
            object_start = {
                'system_id': system_id
            }
            logger.start(object=object_start)
            connection = Connector.get_connection('external_user')
            query_get_all = "SELECT access_token FROM external_user.external_user_view WHERE system_id=%s"
            cursor = connection.cursor()
            cursor.execute(query_get_all, (system_id))
            access_tokens = cursor.fetchall()
            cursor.close()
            return access_tokens
        except Exception as error:
            logger.exception(object=error)
        logger.end(object={'access_tokens': access_tokens})

    @staticmethod
    def update_access_token(username, system_id, profile_id, access_token):
        try:
            object_start = {
                'username': username,
                'system_id': system_id,
                'profile_id': profile_id,
                'access_token': access_token,
            }
            logger.start(object=object_start)
            connection = Connector.get_connection('external_user')
            update_query = "UPDATE external_user.external_user_table AS eu JOIN external_user_profile.external_user_profile_table AS eup ON eu.external_user_id = eup.external_user_id SET eu.access_token = %s WHERE eu.username = %s AND eu.system_id = %s AND eup.profile_id = %s;"
            values = (access_token, username, system_id, profile_id)
            cursor = connection.cursor()
            cursor.execute(update_query, values)
            connection.commit()
            cursor.close()
            object_info = {
                'username': username,
                'system_id': system_id,
                'profile_id': profile_id,
                'access_token': access_token,
            }
            logger.info("external user updated",object=object_info)
        except Exception as error:
            logger.exception(object=error)
        logger.end(object={})

    @staticmethod
    def delete_access_token(username, system_id, profile_id):
        try:
            object_start = {
                'username': username,
                'system_id': system_id,
                'profile_id': profile_id,
            }
            logger.start(object=object_start)
            connection = Connector.get_connection('external_user')
            cursor = connection.cursor()
            update_query = "UPDATE external_user.external_user_table AS eu JOIN external_user_profile.external_user_profile_table AS eup ON eu.external_user_id = eup.external_user_id SET eu.end_timestamp = %s WHERE eu.username = %s AND eu.system_id = %s AND eup.profile_id = %s;"
            current_datetime = datetime.now()
            current_date = current_datetime.date()
            values = (current_date, username, system_id, profile_id)
            cursor.execute(update_query, values)
            cursor.close()
            connection.commit()
            object_info = {
                'username': username,
                'system_id': system_id,
                'profile_id': profile_id,
            }
            logger.info("external user updated",object=object_info)
        except Exception as error:
            logger.exception(object=error)
        logger.end(object={})

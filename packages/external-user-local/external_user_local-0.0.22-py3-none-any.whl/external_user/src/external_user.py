import dotenv
import os
import sys
from logger_local.Logger import Logger
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..')))
from db.external_user_db import ExternalUserDb
from logger_local.LoggerComponentEnum import LoggerComponentEnum
dotenv.load_dotenv()
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

class ExternalUser:

    @staticmethod
    def insert_or_update_external_user_access_token(username, profile_id, system_id, access_token):
        object_start = {
            'username': username,
            'profile_id': profile_id,
            'system_id': system_id,
            'access_token': access_token
        }
        logger.start(object=object_start)
        ExternalUserDb.insert_or_update_external_user_access_token(
            username, profile_id, system_id, access_token)
        logger.end(object={})

    @staticmethod
    def get_access_token(username, profile_id, system_id):
        object_start = {
            'username': username,
            'profile_id': profile_id,
            'system_id': system_id
        }
        logger.start(object=object_start)
        access_token = ExternalUserDb.get_access_token(
            username, profile_id, system_id)
        logger.end(object={'access_token': access_token})
        return access_token

    @staticmethod
    def update_external_user_access_token(username, system_id, profile_id, access_token):
        object_start = {
            'username': username,
            'system_id': system_id,
            'profile_id': profile_id,
            'access_token': access_token,
        }
        logger.start(object=object_start)
        ExternalUserDb.update_access_token(
            username, system_id, profile_id, access_token)
        logger.end(object={})

    @staticmethod
    def get_all_tokens_by_system_id(system_id):
        # might be helpfull if we want update users accounts from social media
        object_start = {
            'system_id': system_id
        }
        logger.start(object=object_start)
        access_tokens = ExternalUserDb.get_all_tokens_by_system_id(system_id)
        logger.end(object={'access_tokens': access_tokens})
        return access_tokens

    @staticmethod
    def delete_access_token(username, system_id, profile_id):
        object_start = {
            'username': username,
            'system_id': system_id,
            'profile_id': profile_id,
        }
        logger.start(object=object_start)
        ExternalUserDb.delete_access_token(username, system_id, profile_id)
        logger.end(object={})

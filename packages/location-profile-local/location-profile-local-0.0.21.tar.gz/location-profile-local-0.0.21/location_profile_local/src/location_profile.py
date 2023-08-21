from logger_local.LoggerLocal import logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from circles_local_database_python.connection import Connection
from circles_local_database_python.generic_crud.src.generic_crud import GenericCRUD

LOCATION_PROFILE_LOCAL_COMPONENT_ID = 167
COMPONENT_NAME = 'location_profile_local/location_profile.py'

object_to_insert = {
    'payload': 'method get_location_id_by_profile_id in location-profile-local',
    'component_id': LOCATION_PROFILE_LOCAL_COMPONENT_ID,
    'component_name': COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'testing_framework': LoggerComponentEnum.testingFramework.pytest.value,
    'developer_email': 'tal.g@circ.zone'
}

logger_local=logger(component_id=LOCATION_PROFILE_LOCAL_COMPONENT_ID,component_name=COMPONENT_NAME,component_category=LoggerComponentEnum.ComponentCategory.Code.value,developer_email="tal.g@circ.zone")

logger_local.init(object=object_to_insert)



class LocationProfile(GenericCRUD):
    def __init__(self):
        INIT_METHOD_NAME = '__init__'
        logger_local.start(INIT_METHOD_NAME)
        self.database = Connection("location_profile")
        self.connection = self.database.connect()
        self.cursor = self.connection.cursor()
        logger_local.end(INIT_METHOD_NAME)

    def __del__(self):
        DEL_METHOD_NAME = '__del__'
        logger_local.start(DEL_METHOD_NAME)
        self.cursor.close()
        self.connection.close()
        logger_local.end(DEL_METHOD_NAME)


    def get_last_location_id_by_profile_id(self, profile_id: int) -> int:
        GET_LAST_LOCATION_ID_BY_PROFILE_ID_METHOD_NAME = "get_last_location_id_by_profile_id"
        logger_local.start(GET_LAST_LOCATION_ID_BY_PROFILE_ID_METHOD_NAME, object={'profile_id': profile_id})
  
        logger_local.info(object={'profile_id':profile_id})
        query_get = "SELECT location_id FROM location_profile.location_profile_view WHERE profile_id=%s ORDER BY start_timestamp DESC LIMIT 1"
        self.cursor.execute(query_get, (profile_id,))
        rows = self.cursor.fetchall()
        location_id = None
        if len(rows) > 0:
            location_id, = rows[0]

        logger_local.end(GET_LAST_LOCATION_ID_BY_PROFILE_ID_METHOD_NAME, object={'location_id':location_id})
        return location_id
    
    def get_location_ids_by_profile_id(self, profile_id: int) -> list[int]:
        GET_LOCATION_IDS_BY_PROFILE_ID_METHOD_NAME = "get_location_ids_by_profile_id"
        logger_local.start(GET_LOCATION_IDS_BY_PROFILE_ID_METHOD_NAME, object={'profile_id': profile_id})
  
        logger_local.info(object={'profile_id':profile_id})
        query_get = "SELECT location_id FROM location_profile.location_profile_view WHERE profile_id=%s ORDER BY start_timestamp DESC"
        self.cursor.execute(query_get, (profile_id,))
        rows = self.cursor.fetchall()
        location_ids = [None]
        if len(rows) > 0:
            for row in rows:
                location_id, = row
                location_ids.append(location_id)

        logger_local.end(GET_LOCATION_IDS_BY_PROFILE_ID_METHOD_NAME, object={'location_id':location_id})
        return location_ids

    def insert_location_profile(self, profile_id: int, location_id: int, lang_code: str = 'en', title: str = 'Home', title_approved = True):
        INSERT_LOCATION_PROFILE_METHOD_NAME = 'insert_location_profile'
        logger_local.start(INSERT_LOCATION_PROFILE_METHOD_NAME, object = {"location_id": location_id})

        query_insert = "INSERT INTO location_profile.location_profile_table(profile_id, location_id) VALUES (%s, %s)"
        self.cursor.execute(query_insert, (profile_id, location_id))

        reaction_id = self.cursor.lastrowid()
        query_insert_ml = "INSERT INTO location_profile.location_profile_ml_table(location_profile_id, lang_code, title, title_approved) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(query_insert_ml, (reaction_id, lang_code, lang_code, title, title_approved))            
        self.connection.commit()

        logger_local.end(INSERT_LOCATION_PROFILE_METHOD_NAME)
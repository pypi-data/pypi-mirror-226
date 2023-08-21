from circles_local_database_python import connection
from circles_local_database_python.generic_crud.src import generic_crud
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.Logger import Logger

EXTERNAL_USER_COMPONENT_ID = 169
EXTERNAL_USER_COMPONENT_NAME = 'person-local'
object_init = {
    'component_id': EXTERNAL_USER_COMPONENT_ID,
    'component_name':EXTERNAL_USER_COMPONENT_NAME,
    'component_category':LoggerComponentEnum.ComponentCategory.Code.value,
    "developer_email":"jenya.b@circ.zone"
}
loger_local = Logger.create_logger(object=object_init)

class DeletePerson(generic_crud.GenericCRUD):
    def __init__(self):
        pass

    def delete(person_id: int) -> None:
        loger_local.start("Delete person by ID",object={"person_id":person_id})
        conn = connection.Connection("person").connect()
        db_cursor = connection.Connection.cursor(conn)
        query = ("UPDATE person.person_table SET end_timestamp = CURRENT_TIMESTAMP WHERE person_id = {}".format(person_id))
        db_cursor.execute(query)
        conn.commit()
        loger_local.end()

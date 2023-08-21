from circles_local_database_python import connection
import mysql.connector
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


def insert_person(number: int, gender_id: int, last_coordinate: str, location_id: int) -> int:
    loger_local.start("Insert person",object={"number": number, "gender_id": gender_id, "last_coordinate": last_coordinate , "location_id": location_id})
    try:
        conn = connection.Connection.get_connection("person")
        db_cursor = connection.Connection.cursor(conn)
        query = ("INSERT INTO person.person_table (number, gender_id, last_coordinate, location_id,start_timestamp) VALUES ({}, {}, {}, {}, CURRENT_TIMESTAMP)".
                 format(number, gender_id, last_coordinate, location_id))

        db_cursor.execute(query)
        conn.commit()
        loger_local.info("Person inserted successfully.")
        db_cursor.execute("SELECT LAST_INSERT_ID()")
        last_inserted_id = db_cursor.fetchone()[0]
    except mysql.connector.Error as err:
        loger_local.exception(err)
    loger_local.end("Person added", object={'person_id': last_inserted_id})
    return last_inserted_id    



def insert_person_ml( person_id: int) -> int:
    loger_local.start("Insert person",object={"id":id})
    conn = connection.Connection.get_connection("person")
    db_cursor = connection.Connection.cursor(conn)

    query = ("INSERT INTO person.person_ml_table (id) VALUES ({})".format(id))

    db_cursor.execute(query)
    conn.commit()
    loger_local.end("Person added", object={'person_id': person_id})
    return person_id
    
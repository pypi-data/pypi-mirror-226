from circles_local_database_python import connection
import datetime
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



class UpdatePerson:
    db_conn = connection.Connection.get_connection("person")

    def __init__(self):
        pass

    def conn_db(query: str) -> None:
        loger_local.start("Sending query to db",object={"query":query})
        #db_cursor = connection.Connection.cursor(conn)
        db_cursor = connection.Connection.cursor(UpdatePerson.db_conn)
        db_cursor.execute(query)
        UpdatePerson.db_conn.commit()
        loger_local.end()

    def update_person_day(id: int,day: int) -> None:
        loger_local.start("Update day by ID",object={"id":id,"day":day})
        query = ("UPDATE person.person_table SET day = {} WHERE person_id = {}".format(day,id))
        UpdatePerson.conn_db(query)
        loger_local.end()

    def update_person_month(id: int,month: int) -> None:
        loger_local.start("Update month by ID",object={"id":id,"month":month})
        query = ("UPDATE person.person_table SET month = {} WHERE person_id = {}".format(month,id))
        UpdatePerson.conn_db(query)
        loger_local.end()

    def update_person_year(id: int,year: int) -> None:
        loger_local.start("Update year by ID",object={"id":id,"year":year})
        query = ("UPDATE person.person_table SET year = {} WHERE person_id = {}".format(year,id))
        UpdatePerson.conn_db(query)
        loger_local.end()

    def update_person_birthday_date(id: int,birthday_date: datetime.date) -> None:
        loger_local.start("Update birthday date by ID",object={"id":id,"birthday_date":birthday_date})
        query = ("UPDATE person.person_table SET birthday_date = '{}' WHERE person_id = {}".format(birthday_date,id))
        UpdatePerson.conn_db(query)
        loger_local.end()

    def update_person_first_name(id: int,first_name: str) -> None:
        loger_local.start("Update first name by ID",object={"id":id,"first_name":first_name})
        query = ("UPDATE person.person_table SET first_name = '{}' WHERE person_id = {}".format(first_name,id))
        UpdatePerson.conn_db(query)
        UpdatePerson.update_person_ml_first_name(id,first_name)
        loger_local.end()

    def update_person_ml_first_name(id: int,first_name: str) -> None:
        loger_local.start("Update first name in ml table by ID",object={"id":id,"first_name":first_name})
        query = ("UPDATE person.person_ml_table SET first_name = '{}' WHERE person_id = {}".format(first_name,id))
        UpdatePerson.conn_db(query)
        loger_local.end() 

    def update_person_nickname(id: int,nickname: str) -> None:
        loger_local.start("Update nickname by ID",object={"id":id,"nickname":nickname})
        query = ("UPDATE person.person_table SET nickname = '{}' WHERE person_id = {}".format(nickname,id))
        UpdatePerson.conn_db(query)
        loger_local.end()

    def update_person_last_name(id: int,last_name: str) -> None:
        loger_local.start("Update last name by ID",object={"id":id,"last_name":last_name})
        query = ("UPDATE person.person_table SET last_name = '{}' WHERE person_id = {}".format(last_name,id))
        UpdatePerson.conn_db(query)
        UpdatePerson.update_person_ml_last_name(id,last_name)
        loger_local.end()

    def update_person_ml_last_name(id: int,last_name: str) -> None:
        loger_local.start("Update last name in ml table by ID",object={"id":id,"last_name":last_name})
        query = ("UPDATE person.person_ml_table SET last_name = '{}' WHERE person_id = {}".format(last_name,id))
        UpdatePerson.conn_db(query)
        loger_local.end()

# --------------------------------------------------------
# pip install mysql-connector-python
import config
import mysql.connector
from mysql.connector import errorcode



def init_database():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user=config.DATABASE_USER,
            password=config.DATABASE_USER_PASSWD,
            database=config.TEATR_DATABASE_NAME
        )
    except  Exception as ex:
        if ex.errno == errorcode.ER_BAD_DB_ERROR:
            print("Brak bazy danych. Zakładam nową.")
            mydb = mysql.connector.connect(
                host="localhost",
                user=config.DATABASE_USER,
                password=config.DATABASE_USER_PASSWD,
            )
            mycursor = mydb.cursor()
            print("DB:", mycursor)
            sql_txt = "CREATE DATABASE " + config.TEATR_DATABASE_NAME
            mycursor.execute(sql_txt)
        else:
            print("Bląd inicjalizacji bazy danych:", ex)

    return mydb


def init_database2():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user=config.DATABASE_USER,
            password=config.DATABASE_USER_PASSWD,
        )
        mycursor = mydb.cursor()

        mycursor.execute("SHOW DATABASES")
        fnd = False
        for x in mycursor:
            if x[0] == config.TEATR_DATABASE_NAME:
                fnd = True;
                break;
        if fnd:
            mydb.close();
            mydb = mysql.connector.connect(
                host="localhost",
                user=config.DATABASE_USER,
                password=config.DATABASE_USER_PASSWD,
                database=config.TEATR_DATABASE_NAME
            )
        else:
            print("Brak bazy danych. Zakładam nową.")
            mycursor.execute("CREATE DATABASE " + config.TEATR_DATABASE_NAME)
        return mydb
    except  Exception as ex:
        print("Bląd inicjalizacji bazy danych:", ex)
        return None

TABELA_IMPREZ = "imprezy"
#https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html

def init_tabele(mycurcor):
    m = mycurcor.execute("SHOW TABLES")
    Fnd = False
    for x in mycursor:
        if x[0] == TABELA_IMPREZ:
            Fnd = True
            break

    print(mycurcor.stored_results())
    if not Fnd:
        print("Dodaje tabele:", TABELA_IMPREZ)
        mycursor.execute("CREATE TABLE " + TABELA_IMPREZ + " (name VARCHAR(255), address VARCHAR(255))")


print("\n\n------Teatr-------")

mydb = init_database()
mycursor = mydb.cursor()

init_tabele(mycursor)

mycursor.execute("SHOW DATABASES")

for x in mycursor:
    print(x)

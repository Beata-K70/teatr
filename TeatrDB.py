# --------------------------------------------------------
# pip install mysql-connector-python
#


import config
import mysql.connector
from mysql.connector import errorcode
import KlientDef


def init_database():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user=config.DATABASE_USER,
            password=config.DATABASE_USER_PASSWD,
            database=config.TEATR_DATABASE_NAME,
            buffered=True,
        )
    except  Exception as ex:
        if ex.errno == errorcode.ER_BAD_DB_ERROR:
            print("Brak bazy danych. Zakładam nową.")
            mydb = mysql.connector.connect(
                host="localhost",
                user=config.DATABASE_USER,
                password=config.DATABASE_USER_PASSWD,
                buffered=True,
            )
            create_database(mydb.cursor())

        else:
            print("Bląd inicjalizacji bazy danych:", ex)

    return mydb


def create_database(cursor):
    try:
        print("DB:", cursor)
        sql_txt = "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(config.TEATR_DATABASE_NAME)
        cursor.execute(sql_txt)

    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


TABELA_IMPREZ = "imprezy"
TABELA_KLIENT = "klienci"
TABELA_BILETOW = "bilety"

TABLES = {}
TABLES['klienci'] = (
    "CREATE TABLE `klienci` ("
    "  `klient_no` int(11) NOT NULL AUTO_INCREMENT UNIQUE KEY,"
    "  `name` varchar(60) NOT NULL,"
    "  `city` varchar(60),"
    "  `street` varchar(60),"
    "  `email`  varchar(60),"
    "  `phone`  varchar(20),"
    "  PRIMARY KEY (`klient_no`)"
    ") ENGINE=InnoDB")

TABLES['imprezy'] = (
    "CREATE TABLE `imprezy` ("
    "  `impreza_no` int(11) NOT NULL AUTO_INCREMENT UNIQUE KEY,"
    "  `nazwa` varchar(60) NOT NULL,"
    "  `date` date NOT NULL,"
    "  `sala` varchar(10) NOT NULL,"
    "  PRIMARY KEY (`impreza_no`), UNIQUE KEY `nazwa` (`nazwa`)"
    ") ENGINE=InnoDB")

TABLES['bilety'] = (
    "CREATE TABLE `bilety` ("
    "  `bilet_no` int(11) NOT NULL,"
    "  `impreza_no` int(11) NOT NULL,"
    "  `klient_no` int(11) NOT NULL,"
    "  `place` varchar(10) NOT NULL,"
    "  PRIMARY KEY (`bilet_no`),"
    "  CONSTRAINT fk_impreza FOREIGN KEY (impreza_no) REFERENCES imprezy(impreza_no),"
    "  CONSTRAINT fk_klient FOREIGN KEY (klient_no) REFERENCES klienci(klient_no)"
    ") ENGINE=InnoDB")


#    "  FOREIGN KEY ('klientimprez_no') REFERENCES imprezy(imprez_no),"


# https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html


def init_tabele(cursor):
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Dodaje tabele {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")


def init_db():
    mydb = init_database()
    if mydb is not None:
        my_cursor = mydb.cursor()
        init_tabele(my_cursor)
        init_database()
        init_tabele()
        return True
    return False


def add_klient(klient):
    db1 = init_database()
    cursor1 = db1.cursor()

    sql = f'INSERT INTO {TABELA_KLIENT} (name, city, street, email, phone) VALUES (%s, %s, %s, %s, %s)'
    val = (klient.imie_nazwisko, klient.miejscowosc, klient.adres, klient.email, klient.telefon)
    cursor1.execute(sql, val)
    db1.commit()


def load_klints():
    db1 = init_database()
    cursor1 = db1.cursor()
    cursor1.execute(f"SELECT * FROM {TABELA_KLIENT}")
    myresult = cursor1.fetchall()
    return myresult


# ---Test----------------------------------
if __name__ == "__main__":
    print("\n\n------Teatr-------")

    mydb = init_database()
    my_cursor = mydb.cursor()
    init_tabele(my_cursor)

    my_cursor.execute("SHOW TABLES")

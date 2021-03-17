import psycopg2


def databaseconnect(database, user, password):
    '''Deze functie maakt een connectie met een PGAdmin database'''
    connection = psycopg2.connect(
        database=database,
        user=user,
        password=password)
    return connection


def makecursor(connection):
    '''Deze functie maakt een cursor die nodig is om queries uit te voeren'''
    return connection.cursor()


def insertdata(cursor, query, values):
    '''Deze functie voert data in in de database'''
    cursor.execute(query, values)


def getdata(cursor, query, values, fetchone=True):
    '''Deze functie haalt data op uit de PGAdmin database'''
    cursor.execute(query, values)
    if fetchone:
        return cursor.fetchone()
    return cursor.fetchall()


def updatedata(cursor, query, values):
    '''Deze functie kan waardes veranderen van bepaalde rijen'''
    cursor.execute(query, values)


def maketable(cursor, query):
    '''Deze functie kan een nieuwe tabel aanmaken'''
    cursor.execute(query)


def droptable(cursor, query):
    '''Deze functie dropt een tabel'''
    cursor.execute(query)


def closeconnection(connection, cursor):
    '''Deze functie sluit de connectie met de PGAdmin database'''
    cursor.close()
    connection.close()

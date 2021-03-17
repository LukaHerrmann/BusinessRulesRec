import PGInteract as P







connection = P.databaseconnect('BusinessRules', 'postgres', 'broodje123')
cursor = P.makecursor(connection)

P.closeconnection(connection, cursor)
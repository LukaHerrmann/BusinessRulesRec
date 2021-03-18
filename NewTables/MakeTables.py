import PGInteract as P


def profilecategories(connection, cursor):
    '''Deze functie maakt een nieuwe tabel aan met daarin het profiel en de categorie die het meest bekeken is
    door dit profiel'''
    print('Creating table')
    # maakt een nieuwe table aan
    P.droptable(cursor, 'drop table if exists BestCategories CASCADE')
    P.maketable(cursor, 'create table BestCategories(profileid varchar, bestcategory varchar, frequency int, '
                        'foreign key (profileid) references profiles(id))')
    connection.commit()
    print('Getting data')
    # sql query die de nieuwe informatie genereert
    # bestaat uit twee gegenereerde tables die zijn samengevoegd
    # de eerste table pakt de hoogste frequency van de categorie die voorkomt
    # de tweede table heeft de frequencies van alle categorieen van de bekenen producten
    profilequery = 'SELECT a.profid, b.category, a.highestfreq ' \
                   'FROM (select profid, max(frequency) as highestfreq from(' \
                   'select profid, category, count(category) as frequency ' \
                   'from profiles_previously_viewed ' \
                   'inner join products on prodid = id ' \
                   'group by profid, category) as subsub1 ' \
                   'group by profid) as a ' \
                   'INNER JOIN (select profid, category, count(category) as frequency ' \
                   'from profiles_previously_viewed inner join products on prodid = id ' \
                   'group by profid, category) as b ' \
                   'ON a.profid = b.profid AND a.highestfreq = b.frequency'
    profileinfo = P.getdata(cursor, profilequery, False)
    totalsize = len(profileinfo)
    iteration = 0
    percentile = 0
    print('Inserting data')
    # zet de gegenereerde data in de nieuwe table
    for profile in profileinfo:
        insertquery = f"insert into BestCategories values ('{profile[0]}', '{profile[1]}', '{profile[2]}')"
        P.insertdata(cursor, insertquery)
        iteration += 1
        if iteration/totalsize*100 >= percentile:
            print(str(percentile)+'%')
            percentile += 10
    connection.commit()


connection = P.databaseconnect('BusinessRules', 'postgres', 'broodje123')
cursor = P.makecursor(connection)
profilecategories(connection, cursor)
P.closeconnection(connection, cursor)
import PGInteract as P


def profilecategories(connection, cursor):
    print('Creating table')
    P.droptable(cursor, 'drop table if exists BestCategories CASCADE')
    P.maketable(cursor, 'create table BestCategories(profileid varchar, bestcategory varchar,'
                        'foreign key (profileid) references profiles(id))')
    connection.commit()
    print('Getting data')
    profilequery = 'select profid, category, max(frequency) as highestfreq from( ' \
                   'select profid, category, count(category) as frequency ' \
                    'from profiles_previously_viewed ' \
                    'inner join products on prodid = id ' \
                    'group by category, profid) as subsub ' \
                    'group by profid, category ' \
                    'order by highestfreq ASC '
    profileinfo = P.getdata(cursor, profilequery, False)
    totalsize = len(profileinfo)
    iteration = 0
    percentile = 0
    print('Inserting data')
    for profile in profileinfo:
        insertquery = f"insert into BestCategories values ('{profile[0]}','{profile[1]}')"
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
import GrapicalInterface as G
import PGInteract as P
import MongoInteract as M
from tkinter import *
from pymongo import MongoClient

# algemene variabelen
background = '#42b0f5'
textcolor = 'black'
bgbutton = 'white'
bgbuttonactivated = 'gray'
# bij het toevoegen van kolommen moet de selling_price als laatste blijven; werkt niet bij nested values
displayedcolumns = ('_id', 'name', 'brand', 'type', 'category', 'selling_price')


def start():
    '''Deze functie start het startscherm en zet alle elementen erin en verbindt deze met de juiste
    acties'''
    root = G.makewindow(500, 700, 'Recommendations', background)
    generalframe = G.makeframe(root, TOP, background, 1, BOTH, 'n')
    productsframe = G.makeframe(root, BOTTOM, background, 1, BOTH, 's')
    G.makelabel(generalframe, 0.02, 0.24, 'Filtering:', ('', 15), textcolor, background, 'w')
    contentbutton = G.makebutton(generalframe, 0.2, 0.24, 12, 2, 'Content', ('', 10, 'bold'),
                                 textcolor, bgbuttonactivated, bgbutton, 'w', 'sunken')
    contentbutton['command'] = lambda: G.switchbutton(contentbutton, collaborativebutton, bgbutton, bgbuttonactivated)
    collaborativebutton = G.makebutton(generalframe, 0.45, 0.24, 12, 2, 'Collaborative', ('', 10, 'bold'),
                                       textcolor, bgbutton, bgbuttonactivated, 'w', 'raised')
    collaborativebutton['command'] = lambda: G.switchbutton(collaborativebutton, contentbutton, bgbutton,
                                                            bgbuttonactivated)
    G.makelabel(generalframe, 0.02, 0.1, 'Profileid:', ('', 15, 'bold'), textcolor, background, 'w')
    profileentry = G.makeentry(generalframe, 0.2, 0.1, 30, ('', 10), textcolor, 'white', 'w')
    submitbutton = G.makebutton(generalframe, 0.7, 0.24, 6, 1, 'Change', ('', 8),
                                textcolor, bgbutton, bgbuttonactivated, 'w', 'raised')
    connection, cursor = setupconnection()
    submitbutton['command'] = lambda: submit(cursor, contentbutton, collaborativebutton, profileentry,
                                             submitbutton, productsframe, root)
    root.mainloop()
    # connectie met PGAdmin database sluit wanneer het scherm wordt afgesloten
    P.closeconnection(connection, cursor)


def submit(cursor, button1, button2, entry, submitbutton, frame, root):
    '''Deze functie wordt geactiveerd wanneer de 'change' knop wordt geactiveerd. Deze functie zal
    controleren welke knoppen zijn ingedrukt en zal dan de benodigde acties uitvoeren'''
    if button1['relief'] == 'sunken' or button2['relief'] == 'sunken':
        frame.destroy()
        frame = G.makeframe(root, BOTTOM, background, 1, BOTH, 's')
        submitbutton['command'] = lambda: submit(cursor, button1, button2, entry, submitbutton, frame, root)
        title = G.makelabel(frame, 0.05, 0.1, 'Recommendations:', ('', 15, 'bold'), textcolor, background, 'w')
        if button1['relief'] == 'sunken':
            contentfilter(entry.get(), cursor, frame, root)
        else:
            collabfilter(entry.get(), cursor, frame, root)


def setupconnection():
    '''Deze functie maakt een connectie aan met de PGAdmin database en maakt daarna nog een cursor
    voor interctie met deze database'''
    connection = P.databaseconnect('BusinessRules', 'postgres', 'broodje123')
    cursor = P.makecursor(connection)
    return connection, cursor


def contentfilter(profileid, cursor, frame, root):
    '''Deze functie recommend nieuwe producten op basis van de meest bekeken categorie van
    het profiel dat op dit moment aangegeven staat'''
    check = checkprofileid(profileid, cursor)
    if check:
        bestcategory, alreadyviewed = getprofileinfo(cursor, profileid)
        # maakt een filter om producten die al een keer bekeken zijn buiten beschouwing te laten
        filters = makefilter(alreadyviewed)
        thefilter = {'$and': [{'category': bestcategory}]+filters}
        client = MongoClient()
        db = client.huwebshop
        collection = db.products
        newproducts = M.getitems(collection, thefilter, limit=4)
        displayproducts(newproducts, displayedcolumns, frame, root)
    else:
        handleerror(frame, 'Dit profileid staat niet in de database')


def collabfilter(profileid, cursor, frame, root):
    '''Deze functie recommend nieuwe producten op basis van de producten die andere
    profielen bekeken hebben met dezelfde favoriete categorie als het profiel dat
    aangegeven staat'''
    check = checkprofileid(profileid, cursor)
    if check:
        bestcategory, alreadyviewed = getprofileinfo(cursor, profileid)
        newproductquery = f"select prodid " \
                          f"from profiles_previously_viewed " \
                          f"inner join bestcategories on profid=profileid " \
                          f"where bestcategory='{bestcategory}' " \
                          f"and not profid='{profileid}'"
        newproductquery = makefilter(alreadyviewed, newproductquery)
        newproductquery += f" limit 4"
        newproducts = P.getdata(cursor, newproductquery, False)
        # maakt een filter om de met sql gevonden producten uit de MongoDB database te halen
        filters = makefilter(newproducts, exclude=False)
        thefilter = {'$or': filters}
        client = MongoClient()
        db = client.huwebshop
        collection = db.products
        newproducts = M.getitems(collection, thefilter, limit=4)
        displayproducts(newproducts, displayedcolumns, frame, root)
    else:
        handleerror(frame, 'Dit profileid staat niet in de database')


def checkprofileid(profileid, cursor):
    '''Deze functie gaat na of het ingevoerde profileid wel in de database staat'''
    result = P.getdata(cursor, f"select id from profiles where id='{profileid}'")
    return result is not None


def handleerror(frame, text):
    '''Deze funcie maakt een rode text voor wanneer er een error optreedt'''
    label = G.makelabel(frame, 0.05, 0.2, text, ('', 15, 'bold'),
                        'red', background, 'w')


def getprofileinfo(cursor, profileid):
    '''Deze functie haalt informatie op van het aangegeven profiel, zoals de favoriete categorie en de
    producten die als bekeken zijn door dit profiel'''
    bestcategory = P.getdata(cursor, f"select bestcategory from bestcategories where profileid='{profileid}'")
    alreadyviewed = P.getdata(cursor, f"select prodid from profiles_previously_viewed where profid='{profileid}'",
                              False)
    return bestcategory[0], alreadyviewed


def makefilter(products, query=False, exclude=True):
    '''Deze functie maakt een filter voor sql of de pymongo library voor een groter aantal producten.
    Deze functie kan zowel includeren als excluderen'''
    if query:
        for product in products:
            query += f" and not prodid='{product[0]}'"
        return query
    else:
        filters = []
        if exclude:
            for product in products:
                filters.append({'_id': {'$ne': product[0]}})
        else:
            for product in products:
                filters.append({'_id': product[0]})
        return filters


def displayproducts(products, columns, frame, root):
    '''Deze functie plaatst een rij van producten op het scherm als de recommendations'''
    fulldisplay = lambda x: (lambda: displayfullproduct(x, columns, root))
    number = 0
    for product in products:
        label = G.makelabel(frame, 0.2, 0.2+number*0.2, product['name'], ('', 10), textcolor, background, 'w')
        button = G.makebutton(frame, 0.05, 0.2+number*0.2, 8, 1, 'expand', ('', 8), textcolor, bgbutton, bgbuttonactivated,
                              'w', 'raised')
        button['command'] = fulldisplay(product)
        number += 1
    if not number:
        handleerror(frame, 'Geen recommendations beschikbaar')


def displayfullproduct(product, columns, root):
    '''Deze functie wordt geactiveerd zodra je op het 'expand' knopje drukt. Er wordt dan een nieuw
    scherm gemaakt met uitgebreide informatie over het product'''
    newwindow = G.maketoplevel(root, 800, 400, product['name'], background)
    number = 0
    for column in columns:
        if column == 'selling_price':
            label = G.makelabel(newwindow, 0.05, 0.1 + number * 0.1,
                                column + ': ' + str(product['price'][column]),
                                ('', 10, 'bold'), textcolor, background, 'w')
        elif column in product.keys():
            label = G.makelabel(newwindow, 0.05, 0.1 + number * 0.1, column + ': ' + str(product[column]),
                                ('', 10, 'bold'), textcolor, background, 'w')
            number += 1


if __name__ == '__main__':
    start()

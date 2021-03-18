import GrapicalInterface as G
import PGInteract as P
import MongoInteract as M
from tkinter import *
from pymongo import MongoClient

background = '#42b0f5'
textcolor = 'black'
bgbutton = 'white'
bgbuttonactivated = 'gray'

def start():
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
    P.closeconnection(connection, cursor)


def submit(cursor, button1, button2, entry, submitbutton, frame, root):
    if button1['relief'] == 'sunken' or button2['relief'] == 'sunken':
        frame.destroy()
        frame = G.makeframe(root, BOTTOM, background, 1, BOTH, 's')
        submitbutton['command'] = lambda: submit(cursor, button1, button2, entry, submitbutton, frame, root)
        title = G.makelabel(frame, 0.05, 0.1, 'Recommendations:', ('', 15, 'bold'), textcolor, background, 'w')
        if button1['relief'] == 'sunken':
            contentfilter(entry.get(), cursor, frame, root)
        else:
            collabfilter(entry.get(), cursor)


def setupconnection():
    connection = P.databaseconnect('BusinessRules', 'postgres', 'broodje123')
    cursor = P.makecursor(connection)
    return connection, cursor


def contentfilter(profileid, cursor, frame, root):
    bestcategory = P.getdata(cursor, f"select bestcategory from bestcategories where profileid='{profileid}'")
    alreadyviewed = P.getdata(cursor, f"select prodid from profiles_previously_viewed where profid='{profileid}'", False)
    filters = []
    for product in alreadyviewed:
        filters.append({'_id': {'$ne': product[0]}})
    columns = ('_id', 'name', 'brand', 'type', 'category', 'selling_price')
    client = MongoClient()
    db = client.huwebshop
    collection = db.products
    filter = {'$and': [{'category': bestcategory[0]}]+filters}
    newproducts = M.getitems(collection, filter, limit=4)
    displayproducts(newproducts, columns, frame, root)


def collabfilter(profileid, cursor):
    pass


def displayproducts(products, columns, frame, root):
    fulldisplay = lambda x: (lambda: displayfullproduct(x, columns, root))
    number = 0
    for product in products:
        label = G.makelabel(frame, 0.2, 0.2+number*0.2, product['name'], ('', 10), textcolor, background, 'w')
        button = G.makebutton(frame, 0.05, 0.2+number*0.2, 8, 1, 'expand', ('', 8), textcolor, bgbutton, bgbuttonactivated,
                              'w', 'raised')
        button['command'] = fulldisplay(product)
        number += 1


def displayfullproduct(product, columns, root):
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

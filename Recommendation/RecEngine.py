import GrapicalInterface as G
import PGInteract as P
from tkinter import *


def start():
    background = '#42b0f5'
    bgbutton = 'white'
    bgbuttonactivated = 'gray'
    root = G.makewindow(500, 700, 'Recommendations', background)
    generalframe = G.makeframe(root, TOP, background, 1, BOTH, 'n')
    productsframe = G.makeframe(root, BOTTOM, background, 1, BOTH, 's')
    G.makelabel(generalframe, 0.02, 0.24, 'Filtering:', ('', 15), 'black', background, 'w')
    contentbutton = G.makebutton(generalframe, 0.2, 0.24, 12, 2, 'Content', ('', 10, 'bold'),
                                 'black', bgbuttonactivated, bgbutton, 'w', 'sunken')
    contentbutton['command'] = lambda: G.switchbutton(contentbutton, collaborativebutton, bgbutton, bgbuttonactivated)
    collaborativebutton = G.makebutton(generalframe, 0.45, 0.24, 12, 2, 'Collaborative', ('', 10, 'bold'),
                                       'black', bgbutton, bgbuttonactivated, 'w', 'raised')
    collaborativebutton['command'] = lambda: G.switchbutton(collaborativebutton, contentbutton, bgbutton,
                                                            bgbuttonactivated)
    G.makelabel(generalframe, 0.02, 0.1, 'Profileid:', ('', 15, 'bold'), 'black', background, 'w')
    profileentry = G.makeentry(generalframe, 0.2, 0.1, 30, ('', 10), 'black', 'white', 'w')
    submitbutton = G.makebutton(generalframe, 0.7, 0.24, 6, 1, 'Change', ('', 8),
                                'black', bgbutton, bgbuttonactivated, 'w', 'raised')
    connection, cursor = setupconnection()
    submitbutton['command'] = lambda: submit(cursor, contentbutton, collaborativebutton, profileentry)
    root.mainloop()
    P.closeconnection(connection, cursor)


def submit(cursor, button1, button2, entry):
    if button1['relief'] == 'sunken':
        contentfilter(entry.get(), cursor)
    elif button2['relief'] == 'sunken':
        collabfilter(entry.get(), cursor)


def setupconnection():
    connection = P.databaseconnect('BusinessRules', 'postgres', 'broodje123')
    cursor = P.makecursor(connection)
    return connection, cursor


def contentfilter(profileid, cursor):
    newproductsquery = f"select id, name, brand, type, category, sellingprice from products where category is not null " \
                       f"except select id, name, brand, type, category, sellingprice from profiles_previously_viewed " \
                       f"inner join products on prodid=id where profid='{profileid}' limit 4"
    newproducts = P.getdata(cursor, newproductsquery, False)
    print(newproducts)


def collabfilter(profileid, cursor):
    pass


if __name__ == '__main__':
    start()

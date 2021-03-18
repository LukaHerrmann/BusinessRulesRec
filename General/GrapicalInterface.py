from tkinter import *


def makewindow(windowwidth, windowheight, windowtitle, bgcolor):
    '''Deze functie maakt een scherm met meegegeven afmetingen en plaatst deze in het midden van het scherm
    en returnt deze voor verder gebruik'''
    root = Tk()
    # De breedte en hoogte van het scherm ophalen
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    # De voorafgaande informatie gebruiken om de interface in het midden van het scherm te plaatsen
    x_coordinate = int((screenwidth / 2) - (windowwidth / 2))
    y_coordinate = int((screenheight / 2) - (windowheight / 2))
    root.geometry('{}x{}+{}+{}'.format(windowwidth, windowheight, x_coordinate, y_coordinate))
    root.configure(bg=bgcolor)
    root.title(windowtitle)
    root.resizable(False, False)
    return root


def makelabel(root, x, y, text, font, textcolor, bgcolor, anchor):
    '''Deze functie maakt een stukje text op basis van de meegegeven variabelen en returnt deze voor
    verder gebruik'''
    label = Label(root,
                  text=text,
                  font=font,
                  fg=textcolor,
                  bg=bgcolor)
    label.place(relx=x, rely=y, anchor=anchor)
    return label


def makebutton(root, x, y, width, height, text, font, textcolor, bgcolor, activebackground, anchor, relief):
    '''Deze functie maakt een knop op basis van de meegegeven variabelen en returnt deze voor verder
    gebruik'''
    button = Button(root,
                    text=text,
                    font=font,
                    width=width,
                    height=height,
                    relief=relief,
                    fg=textcolor,
                    bg=bgcolor,
                    activebackground=activebackground)
    button.place(relx=x, rely=y, anchor=anchor)
    return button


def switchbutton(clickedbutton, otherbutton, bgcolor, bgcoloractivated):
    '''Deze functie zorgt ervoor dat er bij twee knoppen er altijd maar één knop ingedrukt is. Beide knoppen
    mogen wel oningedrukt zijn'''
    togglebutton(clickedbutton, bgcolor, bgcoloractivated)
    if otherbutton['relief'] == 'sunken':
        togglebutton(otherbutton, bgcolor, bgcoloractivated)


def togglebutton(button, bgcolor, bgcoloractivated):
    '''Deze knop verandert de staat van de meegegeven knop. Als de meegegeven knop ingedrukt is zal deze
    opgelaten worden en als de meegegeven knop opgelaten is zal deze ingedrukt blijven'''
    if button['relief'] == 'raised':
        button['relief'] = 'sunken'
        button['bg'] = bgcoloractivated
        button['activebackground'] = bgcolor
    else:
        button['relief'] = 'raised'
        button['bg'] = bgcolor
        button['activebackground'] = bgcoloractivated


def makeentry(root, x, y, width, font, textcolor, bgcolor, anchor):
    '''Deze functie maakt een invoerveld op basis van de meegegeven variabelen
    en returnt deze voor verder gebruik'''
    entry = Entry(root,
                  font=font,
                  fg=textcolor,
                  bg=bgcolor,
                  width=width)
    entry.place(relx=x, rely=y, anchor=anchor)
    return entry


def makeframe(root, side, bgcolor, expand, fill, anchor):
    '''Deze functie maakt een frame op basis van de meegegeven variabelen en
    returnt deze voor verder gebruik'''
    frame = Frame(root,
                  bg=bgcolor)
    frame.pack(side=side, fill=fill, expand=expand, anchor=anchor)
    return frame


def maketoplevel(root, windowwidth, windowheight, windowtitle, bgcolor):
    '''Deze functie maakt een nieuw scherm bovenop een al bestaand scherm op basis van meegegeven
    afmetingen en returnt deze voor verder gebruik'''
    subwindow = Toplevel(root)
    # De breedte en hoogte van het scherm ophalen
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    # De voorafgaande informatie gebruiken om de interface in het midden van het scherm te plaatsen
    x_coordinate = int((screenwidth / 2) - (windowwidth / 2))
    y_coordinate = int((screenheight / 2) - (windowheight / 2))
    subwindow.geometry('{}x{}+{}+{}'.format(windowwidth, windowheight, x_coordinate, y_coordinate))
    subwindow.configure(bg=bgcolor)
    subwindow.title(windowtitle)
    subwindow.resizable(False, False)
    return subwindow

from tkinter import *


def makewindow(windowwidth, windowheight, windowtitle, bgcolor):
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
    label = Label(root,
                  text=text,
                  font=font,
                  fg=textcolor,
                  bg=bgcolor)
    label.place(relx=x, rely=y, anchor=anchor)
    return label


def makebutton(root, x, y, width, height, text, font, textcolor, bgcolor, activebackground, anchor, relief):
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
    togglebutton(clickedbutton, bgcolor, bgcoloractivated)
    if otherbutton['relief'] == 'sunken':
        togglebutton(otherbutton, bgcolor, bgcoloractivated)


def togglebutton(button, bgcolor, bgcoloractivated):
    if button['relief'] == 'raised':
        button['relief'] = 'sunken'
        button['bg'] = bgcoloractivated
        button['activebackground'] = bgcolor
    else:
        button['relief'] = 'raised'
        button['bg'] = bgcolor
        button['activebackground'] = bgcoloractivated


def makeentry(root, x, y, width, font, textcolor, bgcolor, anchor):
    entry = Entry(root,
                  font=font,
                  fg=textcolor,
                  bg=bgcolor,
                  width=width)
    entry.place(relx=x, rely=y, anchor=anchor)
    return entry


def makeframe(root,side, bgcolor, expand, fill, anchor):
    frame = Frame(root,
                  bg=bgcolor)
    frame.pack(side=side, fill=fill, expand=expand, anchor=anchor)
    return frame

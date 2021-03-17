import GrapicalInterface as G
from functools import partial


def start():
    background = '#42b0f5'
    bgbutton = 'white'
    bgbuttonactivated = 'gray'
    root = G.makewindow(500, 700, 'Recommendations', background)
    G.makelabel(root, 0.02, 0.12, 'Filtering:', ('', 15), 'black', background, 'w')
    contentbutton = G.makebutton(root, 0.2, 0.12, 12, 2, 'Content', ('', 10, 'bold'),
                                 'black', bgbuttonactivated, bgbutton, 'w', 'sunken')
    contentbutton['command'] = lambda: G.switchbutton(contentbutton, collaborativebutton, bgbutton, bgbuttonactivated)
    collaborativebutton = G.makebutton(root, 0.45, 0.12, 12, 2, 'Collaborative', ('', 10, 'bold'),
                                       'black', bgbutton, bgbuttonactivated, 'w', 'raised')
    collaborativebutton['command'] = lambda: G.switchbutton(collaborativebutton, contentbutton,bgbutton, bgbuttonactivated)
    G.makelabel(root, 0.02, 0.05, 'Profileid:', ('', 15, 'bold'), 'black', background, 'w')
    profileentry = G.makeentry(root, 0.2, 0.05, 30, ('', 10), 'black', 'white', 'w')
    profilebutton = G.makebutton(root, 0.65, 0.05, 6, 1, 'Submit', ('',8),
                                 'black', bgbutton, bgbuttonactivated, 'w', 'raised')
    root.mainloop()


def contentfilter():
    pass


def collabfilter():
    pass



if __name__ == '__main__':
    start()
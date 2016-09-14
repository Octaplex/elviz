from wx import Panel, BoxSizer, VERTICAL
from visual import window, display

class Elviz:

    def __init__(self, wide, high, title='Elviz'):
        self.window = window(menus=False, title=title)
        self.scene = display(width=wide, height=high)
        


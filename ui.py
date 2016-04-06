from wx import Panel, BoxSizer, VERTICAL
from visual import window, display

class Elviz:

    def __init__(self, title='Elviz'):
        self.window = window(menus=False, title=title)
        self.scene = display(window=self.window, width=self.window.width, height=self.window.height)

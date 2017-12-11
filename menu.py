from market import *
from repo import *
from plate import *
from chef import *
from patron import *

# select
# display
# control/redirect states
class Input(object):
    def __init__(self):
        self.title = None

    @staticmethod 
    def _format_title(title):
        banner = "*"*len(title)*2 + "\n"
        banner += title.center(len(title)*2) + "\n"
        banner += "*"*len(title)*2 +"\n\n"
        return banner

    def get(self,prompt=None,title=None):
        if title == None:
            if prompt == None:
                return raw_input()
            else:
                return raw_input(prompt)
        else:
            if prompt == None:
                banner = Input._format_title(title) 
                return raw_input(banner)
            else:
                banner = Input._format_title(title) 
                return raw_input(banner+ prompt)

class Menu(object):
    def __init__(self,title=None,update_function=None):
       self.title = title
       self.update_function = update_function
       self.submenu = None




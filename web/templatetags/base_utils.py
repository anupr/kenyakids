from django.template import Library, Node
from kenyakids.web.views import menu_items

#sample taken form ubernostrums blog

register = Library()

#creates the menu. is it worth the effort to pass the page name?
class MenuNode(Node):
    def __init__(self):
        self.menu_items = menu_items

    def render(self, context):
        l = self.menu_items
        context['menu'] = l
        return ""

def get_menu(parser, token):
    return MenuNode()
get_menu = register.tag(get_menu)

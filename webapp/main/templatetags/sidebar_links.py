from django import template

register = template.Library();

@register.simple_tag
def get_links():
    return [
        
    #     {
    #     'name': 'Home',
    #     'href': '/',
    #     'icon': 'fa-house',
    # },
     
      {
        'name': 'Categories',
        'href': '/contact',
        'icon': 'fa-layer-group',
    },{
        'name': 'Sale',
        'href': '/contact',
        'icon': 'fa-percent',
    }, {
        'name': 'Contact',
        'href': '/contact',
        'icon': 'fa-envelope',
    }, {
        'name': 'Cart',
        'href': '/cart',
        'icon': 'fas fa-shopping-basket',
    }]
from django import template

register = template.Library()

@register.simple_tag
def get_links():
    return [
        {
            'name': 'Categories',
            'icon': 'fa-layer-group',
            'children': [
                {'name': 'Laptopy i komputery', 'href': '/categories/laptops-computers'},
                {'name': 'Smartfony i smartwatche', 'href': '/categories/smartphones-smartwatches'},
                {'name': 'Gaming i streaming', 'href': '/categories/gaming-streaming'},
                {'name': 'Podzespoły komputerowe', 'href': '/categories/computer-components'},
                {'name': 'Urządzenia peryferyjne', 'href': '/categories/peripherals'},
            ]
        },
        {
            'name': 'Search',
            'href': '/search',
            'icon': 'fa-search',
        },
        {
            'name': 'Contact',
            'href': '/contact',
            'icon': 'fa-envelope',
        },
        {
            'name': 'Cart',
            'href': '/cart',
            'icon': 'fas fa-shopping-basket',
        }
        # {
        #     'name': 'category-name',
        #     'href': '/page-link',
        #     'icon': 'icon-name',
        #     'children': [] for dropdown links in needed
        # },
    ]
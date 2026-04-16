from django import template

register = template.Library()

@register.simple_tag
def get_links():
    return [
        {
            'name': 'Kategorie',
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
            'name': 'Szukaj',
            'href': '/search',
            'icon': 'fa-search',
        },
        {
            'name': 'Kontakt',
            'href': '/contact',
            'icon': 'fa-envelope',
        },
        {
            'name': 'Koszyk',
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
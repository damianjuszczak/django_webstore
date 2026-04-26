import csv
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from main.models import Product, Category, Manufacturer

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Ścieżka do pliku CSV')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']

        try:
            with open(csv_file_path, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    
                    category_name = row.get('category', '').strip()
                    category, _ = Category.objects.get_or_create(
                        name=category_name,
                        defaults={'slug': slugify(category_name)}
                    )

                    manufacturer_name = row.get('manufacturer', '').strip()
                    if not manufacturer_name:
                        manufacturer_name = row['name'].split()[0]
                    
                    manufacturer, _ = Manufacturer.objects.get_or_create(
                        name=manufacturer_name
                    )

                    specs = {}
                    if row.get('ram'): specs['RAM'] = row['ram']
                    if row.get('cpu'): specs['Procesor (CPU)'] = row['cpu']
                    if row.get('gpu'): specs['Karta Graficzna (GPU)'] = row['gpu']
                    if row.get('screen'): specs['Ekran'] = row['screen']
                    if row.get('battery'): specs['Bateria'] = row['battery']

                    product_name = row['name'].strip()
                    base_slug = slugify(product_name)
                    slug = base_slug
                    counter = 1
                    
                    while Product.objects.filter(slug=slug).exists():
                        slug = f"{base_slug}-{counter}"
                        counter += 1

                    Product.objects.create(
                        name=product_name,
                        slug=slug,
                        category=category,
                        manufacturer=manufacturer,
                        description=row.get('description', ''),
                        price=row.get('price', 0),
                        stock=row.get('stock', 0),
                        technical_specs=specs,
                        is_available=True
                    )
                    
                    # Wypisujemy na zielono w terminalu, że się udało
                    self.stdout.write(self.style.SUCCESS(f'Dodano: {product_name}'))
                    
            self.stdout.write(self.style.SUCCESS('Pomyślnie zaimportowano.'))
            
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Błąd: Plik {csv_file_path} nie istnieje.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Błąd podczas importu: {str(e)}'))
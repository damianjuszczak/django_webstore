import requests
import urllib.parse
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from main.models import Product, ProductImage

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

        for product in Product.objects.all():
            print(f" {product.name}")
            
            for i in range(3):
                prompt = f"{product.name} studio photography {i}"  #space change to %20
                safe_prompt = urllib.parse.quote(prompt)
                
                url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=800&height=600&nologo=true"
                
                response = requests.get(url, headers=headers)
                
                if response.status_code == 200: #save only when status 200 = ok
                    new_image = ProductImage(product=product, main_photo=(i == 0))
                    file_name = f"{product.slug}_{i}.jpg"
                    
                    new_image.image.save(file_name, ContentFile(response.content))
                    print(f"zdj {i+1}")
                else:
                    print(f"Błąd serwera (Kod {response.status_code})")
                    
        print("\nWszystkie zdjęcia zostały pomyślnie pobrane")
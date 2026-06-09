#  Sklep internetowy (outofstock)




W pełni funkcjonalna aplikacja e-commerce stworzona w oparciu o framework Django. Projekt demonstruje mechanizmy obsługi sklepu internetowego, w tym płatności, zarządzanie dostawami oraz kontami użytkowników.

---

## ⚫ Główne funkcjonalności
*  **Katalog i wyszukiwarka:** Przeglądanie produktów, szczegółowe specyfikacje techniczne, dynamiczne kategorie i galerie zdjęć.
*  **Koszyk i zamówienia:** Pełen proces zakupowy (checkout) z możliwością wyboru dostawy.
*  **Punkty odbioru (Furgonetka API):** Integracja z zewnętrznym API pozwalająca na wybór paczkomatów i punktów odbioru na mapie.
*  **Płatności online:** Bezpieczne procesowanie płatności za pomocą bramki **Stripe**.
*  **Profile użytkowników:** Rejestracja, logowanie, historia zamówień oraz zarządzanie adresami.
*  **Lista życzeń (Wishlist):** Zapisywanie ulubionych produktów na później.
*  **Moduł CMS:** Dynamiczny slider na stronie głównej (Hero Slides) oraz obsługa zapytań z formularza kontaktowego.

---

## ⚫ Zastosowane technologie
* **Język i Framework:** ![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-6.0.3-092E20.svg)
![PostgreSQL(https://neon.com/)](https://img.shields.io/badge/PostgreSQL-Neon-336791.svg)
* **Baza danych:** PostgreSQL (środowisko chmurowe Neon)
* **Integracje:** Stripe API (`stripe==15.2.0`), Furgonetka API
* **Zarządzanie środowiskiem:** `python-dotenv` (bezpieczne klucze środowiskowe)
* **Media:** `Pillow` (przetwarzanie i zapis obrazów)

---

## ⚫ Instrukcja instalacji (Krok po kroku)

### 1. Wymagania systemowe
* **Python:** Wersja ```3.10``` lub nowsza.
* **Git:** najnowsza stabilna wersja.
* Uprawnienia administratora na komputerze (wymagane do edycji pliku systemowego `hosts` oraz nasłuchiwania na porcie 80).


##
instalacja pythona z poziomu wiersza polecen: (lub manualna [pobierz plik instalacyjny python](https://www.python.org/ftp/python/3.14.5/python-3.14.5-amd64.exe))
> ⚠️ **WAŻNE:**
przed instalacją zaznacz opcje: **Add python.exe to PATH**
```bash
curl -o python_installer.exe https://www.python.org/ftp/python/3.14.5/python-3.14.5-amd64.exe
```
```bash
python_installer.exe
```
uruchamiamy wiersz poleceń ponownie i sprawdzamy czy python został poprawnie zainstalowany
```bash
python --version
```
komunikat: ```Python 3.xx.x``` oznacza poprawną instalacje 

---
instalacja git z poziomu wiersza polecen:  (lub manualna [pobierz plik instalacyjny git](https://github.com/git-for-windows/git/releases/download/v2.54.0.windows.1/Git-2.54.0-64-bit.exe))
```bash
curl -L --ssl-no-revoke -o git_installer.exe https://github.com/git-for-windows/git/releases/download/v2.54.0.windows.1/Git-2.54.0-64-bit.exe
```
```bash
git_installer.exe
```
>jesli nie wiemy, które opcje wybrać podczas instalacji, można zostać przy domyślnych(rekomendowanych)

uruchamiamy wiersz poleceń ponownie i sprawdzamy czy git został poprawnie zainstalowany
```bash
git --version
```
komunikat: ```git version 2.xx.x``` oznacza poprawną instalacje 

### 2. Pobranie projektu i utworzenie środowiska
Sklonuj repozytorium i przejdź do folderu z projektem:
```bash
git clone https://github.com/damianjuszczak/django_webstore
cd django_webstore
```
folder z repozytorium zostanie pobrany do lokalizacji, w której aktualnie jesteś w wierszu poleceń 
> w tym przypadku ```C:\Users\username```

---

Utwórz i aktywuj wirtualne środowisko (zalecane):

```bash
python -m venv venv
venv\Scripts\activate
```


### 3. Instalacja zależności
Wszystkie niezbędne biblioteki zostały zdefiniowane w pliku `requirements.txt`. Zainstaluj je komendą:
```bash
pip install -r webapp/requirements.txt
```

### 4. Konfiguracja domeny lokalnej
> ⚠️ **WAŻNE:** Ze względu na ograniczenia integracji z API (mapy punktów odbioru), aplikacja **musi** być uruchamiana pod domeną `showcase.test`, a nie standardowym `localhost`.

Musisz zmapować tę domenę w swoim systemie na adres lokalny `127.0.0.1`:
1. Uruchom **Notatnik** (lub inny edytor tekstu) jako **Administrator**.
2. Otwórz plik `hosts` znajdujący się pod adresem:
   `C:\Windows\System32\drivers\etc\hosts`
3. Na samym dole pliku dopisz następującą linijkę:
   ```text
   127.0.0.1 showcase.test
   ```
4. Zapisz plik.

### 5. Zmienne środowiskowe (.env)
Przejdź do folderu `webapp` i utwórz plik tekstowy. Wklej do niego poniższą konfigurację:
```env
SECRET_KEY=
DATABASE_URL=
FURGONETKA_API_KEY=
STRIPE_PUBLIC_KEY=
STRIPE_SECRET_KEY=
```
*uzupełnij brakujące klucze udostępnione przez autorów*

zapisz, następnie w górnej części folderu, w którym się znajdujesz, w zakladce **widok** włącz pokazywanie rozszerzen nazw plikow:

windows 11

windows 10

zmień nazwę pliku tekstowego na ```.env``` i zapisz

### 6. Migracje bazy danych
Zastosuj strukturę bazy danych:
```bash
cd webapp
python manage.py migrate
```


### 8. Uruchomienie serwera aplikacji
> ⚠️ Serwer musi zostać uruchomiony na porcie **80**, aby domena zadziałała bez wpisywania portu w przeglądarce.

Uruchom projekt poleceniem:
```bash
python manage.py runserver 80
```

 Sklep jest teraz dostępny w przeglądarce pod adresem:
**http://showcase.test**


---

## ⚫ Struktura projektu


```text
django_webstore/
│
├── webapp/                         # Główny katalog roboczy Django
│   ├── manage.py                   # Główny skrypt zarządzający projektem
│   ├── requirements.txt            # Lista zależności projektowych
│   ├── .env                        # (Należy utworzyć) Plik konfiguracyjny
│   ├── db.sqlite3                  # (Opcjonalnie) Lokalna baza danych
│   │
│   ├── webapp/                     # Główne ustawienia projektu
│   │   ├── settings.py             # Konfiguracja Django
│   │   ├── urls.py                 # Główny routing aplikacji
│   │   └── wsgi.py / asgi.py
│   │
│   ├── main/                       # Logika biznesowa e-commerce
│   │   ├── models.py               # Definicje schematów bazy danych
│   │   ├── views.py                # Widoki i kontrolery (procesy zakupowe)
│   │   ├── urls.py                 # Routing aplikacji 'main'
│   │   ├── cart.py                 # Logika koszyka zakupowego
│   │   ├── admin.py                # Rejestracja modeli w panelu admina
│   │   │
│   │   ├── templates/main/         # Szablony HTML
│   │   │   ├── index.html          # Strona główna
│   │   │   ├── checkout.html       # Kasa / finalizacja zamówienia
│   │   │   ├── account/            # Szablony profili i logowania
│   │   │   └── layout/             # Elementy wspólne (navbar, footer)
│   │   │
│   │   ├── static/main/            # Pliki statyczne
│   │   │   ├── css/                # Arkusze stylów (main.css)
│   │   │   ├── js/                 # Skrypty frontendowe (np. obsługa API)
│   │   │   └── img/                # Grafiki i logotypy interfejsu
│   │   │
│   │   └── management/commands/    # Autorskie skrypty CLI
│   │       ├── import_products.py  # Importowanie danych testowych
│   │       └── generate_ai_images.py # Generowanie zdjęć produktów przy pomocy Ai
│   │
│   └── media/                      # Pliki wgrane przez użytkowników
│       ├── products/gallery/       # Zdjęcia produktów
│       └── hero_slides/            # Obrazy do slidera na stronie głównej
│
└── README.md                       # Dokumentacja projektu
```
# Système de surveillance des prix pour Books Online

Cette documentation permet d'exécuter un code qui va surveiller les prix sur [Books Online](http://books.toscrape.com/).

## Installer Python3

```code
#Installation sous Linux
sudo apt install python3
```

## Créer un environnement virtuel nommé env

```code
sudo apt install python3.10-venv
python3 -m venv env
source env/bin/activate
```

## Installer les dépendances à partir du fichier requirements.txt

Le fichier `requirements.txt` contient toutes les dépendances nécessaires à l'exécution des scripts.

```code
pip3 install -r requirements.txt
```

## Extraire les informations d'une page d'un bouquin

Le script `scraping_p1.py` permet de visiter une page d'un bouquin spécifiée sur le site [Books Online](http://books.toscrape.com/), d'extraire les informations essentielles ci-dessous, puis de les écrire dans un fichier CSV avec des en-têtes de colonnes appropriées.

- product_page_url
- universal_ product_code (upc)
- title
- price_including_tax
- price_excluding_tax
- number_available
- product_description
- category
- review_rating
- image_url

```code
# Afficher l'aide du script
python scraping_p1.py --help
```

```text
usage: scraping_p1.py [-h] url

Ce script visite une page produit spécifiée sur le site "http://books.toscrape.com", extrait les informations essentielles, puis les écrit dans un fichier CSV avec des en-têtes de colonnes appropriées.

positional arguments:
  url         URL de la page produit

options:
  -h, --help  show this help message and exit
```

```code
# Exécuter le script scraping_p1.py avec les paramètres associés
python scraping_p1.py <url_page_produit>
```

**Exemple:**

```code
python scraping_p1.py http://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html
```

Le fichier de sortie se trouve dans `book_data_p1.csv`.

## Récupérer toutes les données nécessaires pour toute une catégorie d'ouvrages

Le script `scraping_p2.py` va parcourir plusieurs pages de bouquins d'une catégorie d'ouvrage afin de récupérer les informations précédemment citées.

```code
# Afficher l'aide du script
python scraping_p2.py --help
```

```text
usage: scraping_p2.py [-h] url

Ce script visite une catégorie de livres spécifiée sur le site
"http://books.toscrape.com", extrait les informations essentielles de chaque livre, puis les
écrit dans un fichier CSV avec des en-têtes de colonnes appropriées.

positional arguments:
  url         URL de la page catégorie de livres. Exemple: http://books.toscra
              pe.com/catalogue/category/books/mystery_3/index.html

options:
  -h, --help  show this help message and exit
```

```code
# Exécuter le script scraping_p2.py avec les paramètres associés
python scraping_p2.py <url_page_categorie>
```

```code
python scraping_p2.py http://books.toscrape.com/catalogue/category/books/mystery_3/index.html
```

Les données des livres de la catégorie donnée sont écrites dans `category_books_data.csv`.

## Extraire toutes les catégories de livres disponibles ainsi que toutes les informations produit de tous les livres

Le script `scraping_p3.py` va extraire toutes les catégories de livres disponibles sur le site [Books Online](http://books.toscrape.com/), puis extrait les informations produit de tous les livres appartenant à toutes les différentes catégories.

Ce script permet aussi de télécharger et d'enregistrer le fichier image de chaque page produit consulté. Mais il y a une option `--no-images` qui permet de désactiver le téléchargement d'images si c'est souhaité.

```code
# Afficher l'aide du script
python scraping_p3.py --help
```

```text
usage: scraping_p3.py [-h] [--no-images]

Scraping des données de livres de toutes les catégories du site
http://books.toscrape.com/ avec option de téléchargement d'images

options:
  -h, --help   show this help message and exit
  --no-images  Désactiver le téléchargement d'images
```

```code
# Exécuter le script scraping_p3.py tout en téléchargeant les images de chaque produit
python scraping_p3.py

# Exécuter le script scraping_p3.py sans télécharger les images de chaque produit
python scraping_p3.py --no-images
```

Les données des livres de chaque catégorie sont enregistrées dans le dossier `results_p3` sous forme de fichiers CSV. Il y a 50 fichiers, donc 50 catégories au total.
Si l'option `--no-images` n'est pas mentionnée, alors les images de chaque produit et de chaque catégorie seront enregitrées dans le dossier `results_p4/images` sous forme de JPG. Il s'agit de 1000 images en tout.

Vous pouvez ouvrir tous les fichiers CSV sur Excel en spécifiant le délimiteur ','.

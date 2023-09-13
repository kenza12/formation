import argparse
import requests
from bs4 import BeautifulSoup
import csv
from scraping_p2 import scrape_category_books
import os
import asyncio
import aiohttp


"""
Description : Ce script va extraire toutes les catégories de livres disponibles sur le site "http://books.toscrape.com/", puis extrait les informations produit de tous les livres appartenant à toutes les différentes catégories.

Il va également télécharger et enregistrer le fichier image de chaque page produit consulté. Mais il y a une option "--no-images" qui permet de désactiver le téléchargement d'images si c'est souhaité.

Version : 1.0.0

Auteur : Kenza BAZI-KABBAJ

Date : 07/09/2023


    Input:
        URL(string): URL des livres en ligne : http://books.toscrape.com/
        --no-images(Booléan) : Désactiver le téléchargement d'images

    Output:
        results_p3/*.csv : fichiers CSV contenant les informations essentielles de tous les bouquins de toutes les catégories données.
        results_p4/images/<category_name>/*.jpg (optionnel) : fichiers JPG de tous les bouquins de toutes les catégories données.
"""

# URL de base du site web à scraper
base_url = "http://books.toscrape.com/"

# Dossiers de destination pour les fichiers CSV et les images téléchargées
results_folder_3 = "results_p3"
results_folder_4= "results_p4"


async def download_image(session, image_url, image_path):
    """_summary_:  Télécharge et enregistre une image depuis une URL.

    Args:
        session (Objet): Session de type aiohttp.ClientSession pour effectuer les requêtes HTTP asynchrones.
        image_url (str): L'URL de l'image à télécharger.
        image_path (str): Le chemin de destination où l'image sera enregistrée localement.
    """
    async with session.get(image_url) as response:
        if response.status == 200:
            with open(image_path, 'wb') as image_file:
                image_file.write(await response.read())
                print(f"L'image {image_path} a été téléchargée avec succès.")
        else:
            print(f"Échec du téléchargement de l'image {image_path} depuis {image_url}")

async def download_product_images_async(data, category_name):
    """_summary_ : Télécharge et enregistre les images des produits de la catégorie donnée.

    Args:
        data (list[dict]): Une liste de dictionnaires contenant les données des produits, y compris les URL des images.
        category_name (str): Le nom de la catégorie actuellement traitée.
    """
    image_folder = os.path.join(results_folder_4, "images", category_name)
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for book_data in data:
            image_url = book_data["image_url"]
            image_name = book_data["universal_product_code"] + ".jpg"  # Nommez l'image en utilisant le code produit universel
            image_path = os.path.join(image_folder, image_name)
            tasks.append(download_image(session, image_url, image_path))

        await asyncio.gather(*tasks)


def scrape_all_category_books(base_url, results_folder_3, download_images=True):
    """_summary_ : Extrait les données de livres de toutes les catégories du site web.

    Args:
        base_url (str): L'URL de base du site web à partir duquel les catégories de livres sont extraites.
        results_folder_3 (str): Le dossier de destination où les fichiers CSV seront enregistrés.
        download_images (bool, optional): Un paramètre optionnel qui détermine si le téléchargement des images doit être activé ou désactivé. Defaults to True.
    """
    if not os.path.exists(results_folder_3):
        os.makedirs(results_folder_3)
    response = requests.get(base_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Trouver tous les liens de catégories de livres dans le menu de navigation
        category_links = soup.find('ul', class_='nav').findAll('a')
        
        for category_link in category_links:
            category_url = os.path.join(base_url, category_link['href'])
            
            # Extraire le nom de la catégorie à partir de l'URL
            category_name = category_url.split('/')[-2].split("_")[0]

            # Exclure la catégorie "Books"
            if category_name.lower() == "books":
                continue
            
            # Appeler la fonction pour extraire les données de la catégorie
            category_books_data = scrape_category_books(category_url)

            if category_books_data:
                # Écrivez les données dans un fichier CSV distinct pour chaque catégorie
                csv_filename = os.path.join(results_folder_3, f"{category_name}_books_data.csv")
                with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = category_books_data[0].keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
                    writer.writeheader()
                    for book_data in category_books_data:
                        writer.writerow(book_data)

                print(f"Les données des livres de la catégorie {category_name} ont été écrites dans {csv_filename}")
                if download_images:  # Vérification de l'option pour télécharger les images
                    # Appeler la fonction pour télécharger et enregistrer les images
                    asyncio.run(download_product_images_async(category_books_data, category_name))

            else:
                print(f"Aucune donnée de livre n'a été extraite pour la catégorie {category_name}")

    else:
        print(f"La requête a échoué avec le code {response.status_code} pour la page d'accueil")

def main():
    parser = argparse.ArgumentParser(description="Scraping des données de livres de toutes les catégories du site http://books.toscrape.com/ avec option de téléchargement d'images")
    parser.add_argument("--no-images", dest="download_images", action="store_false", help="Désactiver le téléchargement d'images")
    args = parser.parse_args()

    # Appeler la fonction principale pour extraire les données
    scrape_all_category_books(base_url, results_folder_3, download_images=args.download_images)

if __name__ == "__main__":
    main()
import requests
from bs4 import BeautifulSoup
import csv
from scraping_p1 import extract_product_info
import os
import argparse


"""
Description : Ce script visite une page d'une catégorie spécifiée sur le site "http://books.toscrape.com",
               extrait les informations essentielles, puis les écrit dans un fichier CSV avec des
               en-têtes de colonnes appropriées.

Version : 1.0.0

Auteur : Kenza BAZI-KABBAJ

Date : 07/09/2023


    Input:
        URL(string): URL de la page de la catégorie des bouquins

    Output:
        category_books_data.csv : fichier CSV contenant les informations essentielles de tous les bouquins d'une catégorie donnée.
"""

# URL de la page de catégorie de livres
base_url = "http://books.toscrape.com/catalogue/category/books/mystery_3/page-1.html"

def scrape_category_books(category_url):
    """_summary_ : fonction qui va parcourir plusieurs pages de bouquins d'une catégorie d'ouvrage afin de récupérer certaines informations.

    Args:
        category_url (_type_): URL de la page web de la catégorie spécifiée

    Returns:
        _list_: Une liste de dictionnaire qui contient les informations de tous les livres d'une catégorie donnée.
    """

    all_books_data = []
    while True:
        response = requests.get(category_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            h3_elements = soup.findAll('h3')
            for h3_element in h3_elements:
                link = h3_element.find('a')
                product_url = link['href']           
                product_data = extract_product_info(os.path.join(category_url.rsplit('/', 4)[0], product_url.split('/', 3)[3]))
                all_books_data.append(product_data)

            # Trouver le lien de la page suivante s'il existe
            next_page = soup.find('li', class_='next')
            if next_page:
                next_page_link = next_page.find('a')
                if next_page_link:
                    next_page_url = os.path.join(os.path.split(category_url)[0], next_page_link['href'])
                    category_url = next_page_url
                else:
                    break  # Il n'y a plus de pages à parcourir
            else:
                break  # Il n'y a plus de pages à parcourir
        else:
            print("La requête a échoué avec le code :", response.status_code)
            break
    
    return all_books_data

def main():
    # Configuration de argparse
    parser = argparse.ArgumentParser(description='Ce script visite une catégorie de livres spécifiée sur le site "http://books.toscrape.com", extrait les informations essentielles de chaque livre, puis les écrit dans un fichier CSV avec des en-têtes de colonnes appropriées.')
    parser.add_argument("url", help="URL de la page catégorie de livres. Exemple: http://books.toscrape.com/catalogue/category/books/mystery_3/index.html")
    args = parser.parse_args()

    # URL de la page de la catégorie des bouquins
    base_url = args.url

    category_books_data = scrape_category_books(base_url)

    if category_books_data:
        # Écrivez les données dans un fichier CSV
        with open('category_books_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = category_books_data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for book_data in category_books_data:
                writer.writerow(book_data)

        print("Les données des livres de la catégorie ont été écrites dans category_books_data.csv.")
    else:
        print("Aucune donnée de livre n'a été extraite.")

if __name__ == "__main__":
    main()
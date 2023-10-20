import os
import csv
from .book_scraper import BookScraper
from .data_handling import DataHandler

class CategoryScraper:
    def __init__(self, category_url):
        """
        Initialise une instance de CategoryScraper avec une URL de page de catégorie.

        Args:
            category_url (str): URL de la page de la catégorie des bouquins.
        """
        self.category_url = category_url

    def scrape_category_books(self, csv_filename=None):
        """
        Extrait les informations essentielles de tous les bouquins d'une catégorie donnée et les écrit dans un fichier CSV.

        Args:
            csv_filename (str): Le nom du fichier CSV où les données seront enregistrées. Si None, les données ne seront pas écrites dans un fichier.

        Returns:
            list[dict]: Une liste de dictionnaires contenant les informations de tous les livres de la catégorie.
        """
        all_books_data = []
        while True:
            # Connexion et récupération de la page
            soup = DataHandler(self.category_url).connect_to_beautiful_soup()
            # Traitement des données de la catégorie
            all_books_data.extend(DataHandler(self.category_url).process_category_data(soup))

            next_page = soup.find('li', class_='next')

            if next_page:
                next_page_link = next_page.find('a')

                if next_page_link:
                    next_page_url = os.path.join(os.path.split(self.category_url)[0], next_page_link['href'])
                    print(f"Next page URL: {next_page_url}")
                    self.category_url = next_page_url
                else:
                    break  # Il n'y a plus de pages à parcourir
            else:
                break
            print("Processed a page.")

        # Écrire les données dans un fichier CSV si un nom de fichier est spécifié
        category_name = (self.category_url.rsplit('/', 2)[1]).rsplit("_", 1)[0] + ".csv"
        self.save_results(all_books_data, category_name)

        return all_books_data

    def save_results(self, data, filename):
        DataHandler(self.category_url).write_to_csv(data, filename)
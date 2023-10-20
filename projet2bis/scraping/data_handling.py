import csv
import logging
import re
import os
import requests
from bs4 import BeautifulSoup

class DataHandler:
    def __init__(self, url):
        self.url = url

    def connect_to_beautiful_soup(self, url=None):
        """
        Connect to the specified URL and parse it with BeautifulSoup.

        Args:
            url (str): URL to connect to. If None, the URL from the constructor will be used.

        Returns:
            BeautifulSoup: Parsed HTML content.
        """
        if url is None:
            url = self.url

        try:
            response = requests.get(url)
            response.raise_for_status()
            page = response.content
            soup = BeautifulSoup(page, 'html.parser')
            return soup
        except requests.exceptions.RequestException as e:
            logging.error(f"Request error: {e}")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return None

    def process_book_data(self, soup):
        """
        Process book data from the BeautifulSoup object.

        Args:
            soup (BeautifulSoup): BeautifulSoup object containing page content.

        Returns:
            dict: Dictionary containing book data.
        """

        book_data = {
            'product_page_url': self.url,
            'universal_product_code': self.extract_value(soup, 'td', 1),
            'title': self.extract_value(soup, 'h1', 1),
            'price_including_tax': self.extract_value(soup, 'td', 4),
            'price_excluding_tax': self.extract_value(soup, 'td', 3),
            'number_available': self.extract_number(soup, 'td', 6),
            'product_description': self.extract_description(soup),
            'category': self.extract_category(soup),
            'review_rating': self.extract_rating(soup),
            'image_url': self.extract_image_url(soup)
        }
        return book_data

    def extract_value(self, soup, tag_name, position):
        elements = soup.find_all(tag_name)
        if len(elements) >= position:
            return elements[position - 1].text
        return None

    def extract_number(self, soup, tag_name, position):
        element = self.extract_value(soup, tag_name, position)
        return int(re.search(r'\d+', element).group()) if element else None

    def extract_description(self, soup):
        meta_description = soup.find("meta", {"name": "description"})
        return meta_description["content"].strip() if meta_description else None

    def extract_category(self, soup):
        breadcrumb = soup.find("ul", class_="breadcrumb")
        return breadcrumb.find_all("li")[-2].find("a").text if breadcrumb else None

    def extract_rating(self, soup):
        rating_class = soup.find('p', class_='star-rating')['class'][1]
        rating_mapping = {
            'One': 1,
            'Two': 2,
            'Three': 3,
            'Four': 4,
            'Five': 5
        }
        return rating_mapping.get(rating_class, None)

    def extract_image_url(self, soup):
        image_element = soup.find('article', class_='product_page').find("div").find("img")
        return self.url.rsplit('/', 2)[0] + '/' + image_element.get("src") if image_element else None

    def write_to_csv(self, data, filename):
        try:
            output_folder = 'outputs'
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            
            output_path = os.path.join(output_folder, filename)

            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                if isinstance(data, list) and data:
                    fieldnames = data[0].keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
                    writer.writeheader()
                    for item in data:
                        writer.writerow(item)
                elif isinstance(data, dict):
                    fieldnames = data.keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
                    writer.writeheader()
                    writer.writerow(data)
                else:
                    raise ValueError("Data must be a dictionary or a list of dictionaries.")
            logging.info(f"Data written to CSV file {filename} successfully")
        except Exception as e:
            logging.error(f"An error occurred while writing to the CSV file {filename}: {e}")

    def process_category_data(self, soup):

        """
        Process category data from the BeautifulSoup object.

        Args:
            soup (BeautifulSoup): BeautifulSoup object containing page content.

        Returns:
            list[dict]: List of dictionaries containing book data for the category.
        """
        all_books_data = []
        h3_elements = soup.findAll('h3')
        for h3_element in h3_elements:
            link = h3_element.find('a')
            product_url = link['href']

            book_page_url = os.path.join(self.url.rsplit('/', 4)[0], product_url.split('/', 3)[3])
            book_page = self.connect_to_beautiful_soup(book_page_url)

            product_data = self.process_book_data(book_page)
            all_books_data.append(product_data)

        return all_books_data
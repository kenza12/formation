import logging
from .data_handling import DataHandler
import os

class BookScraper:
    def __init__(self, url):
        self.url = url

    def scrape_book_data(self):
        """
        Extract book data from the specified URL.

        Returns:
            dict: Dictionary containing book data.
        """
        try:
            soup = DataHandler(self.url).connect_to_beautiful_soup()

            if soup is not None:
                book_data = DataHandler(self.url).process_book_data(soup)

                if book_data:
                    # save results in CSV
                    self.save_results(book_data, self.url)
                    logging.info("Book data extracted and saved successfully")
                    return book_data
                else:
                    logging.error("Failed to extract book data")
                    return None
            else:
                return None
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return None
    
    def save_results(self, book_data, url):
        """
        Save book data to a CSV file.

        Args:
            book_data (dict): The book data to be saved.
            csv_filename (str): The filename of the CSV file.
        """

        filename = os.path.splitext(url)[0]
        filename = (filename.rsplit('/', 2)[1]).rsplit("_", 1)[0]
        filename = f"{filename}.csv"

        DataHandler(self.url).write_to_csv(book_data, filename)

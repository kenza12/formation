from scraping.book_scraper import BookScraper
from scraping.category_scraper import CategoryScraper
from args import parse_arguments
import logging
import os

def main():
    # Configuration du logger global
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(filename)s - %(levelname)s - %(lineno)d - %(message)s"
    )
    args = parse_arguments()

    if args.book_url:
        book_scraper = BookScraper(args.book_url)
        book_data = book_scraper.scrape_book_data()
    elif args.category_url:
        category_scraper = CategoryScraper(args.category_url)
        category_books_data = category_scraper.scrape_category_books()
    elif args.all_category_url:
        category_scraper = CategoryScraper(args.all_category_url)
        all_category_books_data = category_scraper.scrape_all_category_books()
    else:
        logging.error("Please provide a book URL or a category URL.")

if __name__ == '__main__':
    main()

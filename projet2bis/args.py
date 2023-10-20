import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Web Scraping Tool for Books')
    parser.add_argument('--book_url', type=str, help='URL of a book page')
    parser.add_argument('--category_url', type=str, help='URL of a category page')
    args = parser.parse_args()
    return args

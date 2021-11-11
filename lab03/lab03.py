from bs4 import BeautifulSoup
from sys import argv
from os import path
import requests
import json


# Function to scraping 'The Way of Kings' from polish site - lubimyczytac.pl
def book_scraping(filename: str):

    url = 'https://lubimyczytac.pl/ksiazka/4896952/droga-krolow'
    response = requests.get(url)

    # Was the query successful
    if response.status_code != requests.codes.ok:
        print('Something has gone wrong!')
    else:
        soup = BeautifulSoup(response.text, 'lxml')

        # author
        author = soup.find('a', class_='link-name').text.strip()
        # title
        title = soup.find(
            'h1', class_='book__title').text.strip()
        # cycle
        cycle = soup.find(
            'span', class_='d-none d-sm-block mt-1').a.text.strip()
        # category
        category = soup.find(
            'a', class_='book__category d-sm-block d-none').text.strip()
        # pages
        pages = soup.find(
            'span', class_='d-sm-inline-block book-pages book__pages pr-2 mr-2 pr-sm-3 mr-sm-3').text.strip().split()[0]
        # description
        description = soup.find(
            'div', class_='collapse-content').text.strip()  # book description

        # Create dictionary
        keys = ['Autor', 'Tytuł', 'Cykl', 'Kategoria', 'Strony', 'Opis']
        values = [author, title, cycle, category, pages, description]
        dictionary = dict(zip(keys, values))

        # Save dictionary to .json file with indent
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(dictionary, file, ensure_ascii=False, indent=4)
        print(f'Saved information to file \'{filename}\'')


# MAIN
if __name__ == '__main__':

    # simple protection
    try:
        filename = argv[1]
    except IndexError:
        print(f'Usage: {path.basename(__file__)} <filename.json>')
        exit(1)

    book_scraping(filename)

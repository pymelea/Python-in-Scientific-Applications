from multiprocessing.pool import ThreadPool
from bs4 import BeautifulSoup
import requests
import os
import wget
import time


# Directories names
seq_dir = 'seq'
multi_dir = 'multi'


# Function to find urls from www
def find_urls(url: str):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    links = []
    # Save urls to png files
    for a in soup.find_all('a', href=True):
        if a['href'][a['href'].rfind('.')+1:] in ['jpeg', 'png', 'jpg']:
            links.append('http://www.if.pw.edu.pl/~mrow/dyd/wdprir/'+str(a['href']))
        
    return links


# Function to save images with one process
def download_sequence(links: list):
    for link in links:
        print("downloading: ", link)
        # assumes that the last segment after the / represents the file name
        # if url is abc/xyz/file.txt, the file name will be file.txt
        file_name_start_pos = link.rfind("/") + 1
        file_name = link[file_name_start_pos:]
        wget.download(link, f'{seq_dir}/{file_name}')


# Function to save images with multiprocessing
def download_multi(link: str):
    print("downloading: ", link)
    file_name_start_pos = link.rfind("/") + 1
    file_name = link[file_name_start_pos:]
    wget.download(link, f'{multi_dir}/{file_name}')


# Function to create directory
def create_dir(dir_name: str):
    path = os.getcwd()
    path = os.path.join(path, dir_name)
    try:
        os.mkdir(path)
    except:
        pass

# MAIN
if __name__ == '__main__':

    # Create directories
    create_dir(seq_dir)
    create_dir(multi_dir)

    # Find urls from www
    url = 'http://www.if.pw.edu.pl/~mrow/dyd/wdprir/'
    links = find_urls(url)

    # Sequence 
    start = time.time()
    download_sequence(links)
    end = time.time()
    print(f'\nSequence download time: {end - start} s')

    # Multiprocessing
    start = time.time()
    results = ThreadPool(10).imap_unordered(download_multi, links)
    for r in results:
        print(r)
    end = time.time()
    print(f'\nMultiprocessing download time: {end - start} s')
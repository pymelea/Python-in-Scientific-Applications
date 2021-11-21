from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
import sys
import json
import os
import wget


# Function to scrape DevianArt with selenium and download images to directory
def scrape_and_save(search_name: str, filename: str):

    # Set webdriver for Chrome
    driver_path = 'C:/Programy/chromedriver.exe'
    driver_service = Service(driver_path)
    driver = webdriver.Chrome(service=driver_service)

    # Get to DevianArt for pretty pictures
    driver.get('https://www.deviantart.com/')

    # Set input for search and enter
    search = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, '//input[@placeholder="Search & Discover"]')))
    search.clear()
    search.send_keys(search_name)
    search.send_keys(Keys.ENTER)

    # Scroll page and find elements by image
    driver.execute_script('window.scrollTo(0,1000)')
    images = driver.find_elements(By.TAG_NAME, 'img')

    # Get links to images and close driver
    links = [image.get_attribute('src') for image in images]
    driver.close()

    # Only long links are interesting pictures, the others are e.g. avatars
    links = [link for link in links if len(link) > 100]
    # Create ids for each link
    ids = [f'ID{id + 1}' for id in range(len(links))]
    # Create dictionary with ids and links
    dictionary = dict(zip(ids, links))

    # Save dictionary to .json file with indent
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(dictionary, file, ensure_ascii=False, indent=4)
        print(f'Saved information to file \'{filename}\'')

    # Create directory with name search_name
    path = os.getcwd()
    path = os.path.join(path, search_name)
    try:
        os.mkdir(path)
    except:
        pass

    # Save images to directory
    counter = 1
    for link in links:
        save = os.path.join(path, f'{counter}.jpg')
        wget.download(link, save)
        counter += 1


# MAIN
if __name__ == '__main__':

    # simple protection
    try:
        # We can search e.g. 'space', 'mountain' etc.
        search_name = sys.argv[1]
        filename = sys.argv[2]
    except IndexError:
        print(
            f'Usage: {os.path.basename(__file__)} <search_name> <filename.json>')
        exit(1)

    scrape_and_save(search_name, filename)

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

def setup_driver(): 
    #driver = webdriver.Chrome(executable_path="./chromedriver.exe")
    driver = webdriver.Firefox(executable_path="./geckodriver.exe")
    return driver


def write_to_csv(array):
    keys = array[0].keys()
    with open('free_movies_on_youtube.csv','w', newline = '', encoding='utf-8') as output:
        dict_writer = csv.DictWriter(output, keys)
        dict_writer.writeheader()
        dict_writer.writerows(array)


def run():
    main_url = "https://www.youtube.com"
    driver = setup_driver()
    """ Visit main_url """
    driver.get(main_url)
    time.sleep(2)
    """ Click hamburger menu """
    driver.execute_script("document.getElementById('guide-icon').click()")
    time.sleep(1)
    """ Click Movies & Shows """
    driver.execute_script("document.getElementsByClassName('title style-scope ytd-guide-entry-renderer')[8].click()")
    time.sleep(1)
    """Click free to watch"""
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ytd-app/div/ytd-page-manager/ytd-browse[2]/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[2]/div[3]/ytd-shelf-renderer/div[1]/div[1]/div/h2/div[1]/div/a'))).click()
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    driver.quit()
    """ Empty array to hold movie information"""
    movies = []
    for movie in soup.find_all('ytd-grid-movie-renderer',class_='style-scope ytd-grid-renderer'):
        """ Storing individual movie info in a dictionary and appending to the array """
        info = {}
        info['name'] = movie.find('h3',class_="style-scope ytd-grid-movie-renderer").text.strip()
        info['link'] = main_url + movie.find('a', class_="yt-simple-endpoint style-scope ytd-grid-movie-renderer")['href']
        info['duration'] = movie.find('span',class_='style-scope ytd-thumbnail-overlay-time-status-renderer').text.strip()
        movies.append(info)
    write_to_csv(movies)
    

if __name__ == '__main__':
    run()
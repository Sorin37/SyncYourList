import json
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By


def press_accept_button(driver):
    accept_button = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/form[2]/div/div/button')
    accept_button.click()


def get_all_songs(driver):
    contents = driver.find_element(By.ID, 'contents')
    driver.execute_script("window.scrollBy(0,2500)", "")

    previous_size = 0

    songs = []

    while contents.size['height'] != previous_size:
        previous_size = contents.size['height']
        songs = driver.find_elements(By.ID, 'video-title')
        driver.execute_script("window.scrollBy(0,15000)", "")
        time.sleep(2)

    return songs


def write_songs_to_file(songs):
    file = open('./list.txt', 'w', encoding='utf-8')

    for song in songs:
        file.write(song.text)
        file.write('\n')


def get_the_link(driver):
    try:
        file = open('./settings.json')
        settings = json.load(file)

        return settings['link']
    except FileNotFoundError:
        print('ERROR: You need to add a settings.json file to provide the link to the playlist!')
        driver.close()
        input('Press any key to exit.')

        return None


def scrape():
    driver = webdriver.Chrome()

    link = get_the_link(driver)

    if link is None:
        return

    driver.get(link)

    press_accept_button(driver)

    driver.maximize_window()

    songs = get_all_songs(driver)

    write_songs_to_file(songs)


if __name__ == '__main__':
    scrape()

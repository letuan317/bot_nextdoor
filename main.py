import telegram_send
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.webdriver import FirefoxProfile
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import pickle
import urllib
import requests
import json

import os
import os.path
from os import link, path
import sys

import shutil
import time
import datetime


def send_message(message_text):
    telegram_send.send(messages=[message_text])


def send_images(path_images):
    os.system('telegram-send --image '+path_images)


def download_image(url, filename):
    response = requests.get(url)

    file = open("./images/"+filename, "wb")
    file.write(response.content)
    file.close()


class botNextdoor:
    def __init__(self):
        self.email = ''
        self.password = ''
        self.link_freestuff = 'https://nextdoor.com/for_sale_and_free/?init_source=more_menu&is_free=true'
        self.time_sleep = 5
        self.data_linked = []
        self.new_items_link = []

    def main(self):
        self.login()
        # self.new_items_link = self.data_linked
        while(True):
            x = datetime.datetime.now()
            hour = int(x.strftime("%H"))
            if(hour > 6):
                self.get_update()
                self.check_new_item()
                print("Waiting...")
                time.sleep(60)
                self.new_items_link = []
            elif(hour > 5):
                time.sleep(10*60)
            else:
                time.sleep(60*60)

    def start_browser(self):
        print("### Starting browser ...")

        try:
            print("browser01")
            self.driver = webdriver.Firefox()
        except Exception as e:
            try:
                print("browser02")
                binary = FirefoxBinary(
                    "C:\\Program Files\\Mozilla Firefox\\firefox.exe")
                self.driver = webdriver.Firefox(
                    firefox_binary=binary, executable_path=r"C:\\geckodriver.exe")
            except Exception as e:
                try:
                    print("browser03")
                    self.driver = webdriver.Firefox(
                        executable_path='./geckodrivers/geckodriver')
                except Exception as e:
                    try:
                        print("browser04")
                        self.driver = webdriver.Firefox(
                            executable_path='geckodrivers\\geckodriver.exe')
                    except Exception as e:
                        try:
                            self.driver = webdriver.Chrome()
                        except Exception as e:
                            print("!!! ERROR: " + str(e))
                            sys.exit()

        self.driver.set_window_position(0, 0)
        self.driver.set_window_size(800, 1000)

    def login(self):
        self.start_browser()
        self.driver.get(self.link_freestuff)
        check_title = self.driver.title
        print("#Title: "+self.driver.title)
        time.sleep(self.time_sleep)
        count_error = 0
        while True:
            try:
                elem_username = self.driver.find_element_by_id("id_email")
                elem_password = self.driver.find_element_by_id("id_password")

                elem_username.send_keys(self.email)
                elem_password.send_keys(self.password)
                elem_password.send_keys(Keys.RETURN)
                break
            except:
                if(count_error == 5):
                    sys.exit()
                else:
                    time.sleep(self.time_sleep)
                    count_error += 1
                continue

        while(self.driver.title == check_title):
            time.sleep(self.time_sleep)

        print("#Title: "+self.driver.title)
        return True

    def get_update(self):
        try:
            print("*** Get_Update ***")
            self.driver.get(self.link_freestuff)
            time.sleep(self.time_sleep)
            # classified-section-container
            #container = self.driver.find_element_by_id("classified-section-container")

            elems = self.driver.find_elements_by_xpath("//a[@href]")
            for elem in elems:
                temp_link_item = elem.get_attribute("href")

                #print('test: '+temp_link_item)

                # exampe link: https://nextdoor.com/for_sale_and_free/99378231-3d8e-4b1e-8a07-0ac16e0fe17e/?init_source=more_menu
                link_example = 'https://nextdoor.com/for_sale_and_free/a9aa9af9-a14f-4a29-a0d8-464fbe2712df/?init'
                #test_link = "https://nextdoor.com/for_sale_and_free/?init_source=more_menu&is_free=true&topic_ids=77890"
                check_link = "https://nextdoor.com/for_sale_and_free/?init"
                # if(test_link[:len(example_link)-1] != example_link):
                if(len(temp_link_item) > len(link_example)) and (temp_link_item not in self.data_linked):
                    if(temp_link_item[:len(check_link)] == check_link):
                        None
                    else:
                        print("new link: "+temp_link_item)
                        self.new_items_link.append(temp_link_item)
        except Exception as e:
            print(e)

    def check_new_item(self):
        print("#Numbers of new_items: " + str(len(self.new_items_link)))
        if(len(self.new_items_link) > 0):
            self.new_items_link.reverse()
            for item_link in self.new_items_link:
                print("#LINK: " + item_link)

                try:
                    self.driver.get(item_link)
                    time.sleep(self.time_sleep)
                    '''
                    # class = slick-list
                    class_title = self.driver.find_element_by_class_name(
                        "fsf-item-detail-price-title")
                    title = class_title.find_element_by_tag_name('h2').text
                    print("Title: "+str(title))
                    '''
                    container = self.driver.find_element_by_class_name(
                        "slick-list")
                    elems = container.find_elements_by_xpath(
                        "//img[@class='cascaded-image resized-image']")
                    send_message(item_link)
                    # send_message(title)
                    for elem in elems:
                        temp_link_item = elem.get_attribute("src")
                        print("image_link: "+temp_link_item)
                        filename = ''
                        for i in range(len(temp_link_item)-2, 0, -1):
                            if(temp_link_item[i] == "/"):
                                filename = temp_link_item[i +
                                                          1:len(temp_link_item)]
                                break
                        download_image(temp_link_item, filename)
                        send_images("./images/"+filename)

                    self.data_linked.append(item_link)
                except Exception as e:
                    print(e)
                    continue


if __name__ == "__main__":
    bot = botNextdoor()
    bot.main()

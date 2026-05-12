# - coding = utf-8 -
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

from mycookie import loadcookie
from savePage import save_page
from swtichToNewWindow import switchToNewWindow
from internet_now import get_internet_time
from informations.yepay import yepay
from selenium.webdriver.common.by import By
from element import *

from utils import abbrev_to_state_name

from selenium.webdriver.common.action_chains import ActionChains

from driversetting import initDriver
import sys

small = 2

if len(sys.argv) == 2 and sys.argv[1] == 'off':
    driver,actions = initDriver('off')
else:
    driver,actions = initDriver('on')

onzon_url = 'https://www.ozon.ru/'
def void():
    return None

def open_ozon():
    driver.get(onzon_url)
    time.sleep(2)

def search_input(keyword='Кроссовки'):
    search_box = findElementByXPath(driver, "//input[@placeholder='Искать на Ozon']")
    search_box.clear()
    search_box.send_keys(keyword)
    search_box.submit()
    time.sleep(2)

def search_click():
    search_button = findElementByXPath(driver, "//button[@type='submit']")
    search_button.click()
    time.sleep(2)


def walk_items(callback=void):
    items_scroll = findElementByXPath(driver, "//div[@id='contentScrollPaginator']")
    links = items_scroll.find_element(By.XPATH, "//a[@data-widget='search-result-item']")






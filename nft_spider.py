# - coding = utf-8 -

import sys
import time
import pyautogui

from element import (clickElement, clickText, findElement, inputElement, clickTextExact,
                     inputByPlaceholder, clickByTitle, findElements, printElement, clickButtonInGroup,
                     findElementBySelecotr, findInputByPlaceholder, findElementByXPath, findElementsByXPath,
                     findElementByText,inputElementByXpath)

from driversettingWithProfile import initDriver
from utils import parse_safe_number

if len(sys.argv) == 2 and sys.argv[1] == 'off':
    driver,actions = initDriver('off')
else:
    driver,actions = initDriver('on')

from nft_infos import *


nft_home_url = "https://msu.io/"
nft_market_url = "https://msu.io/marketplace/nft?page=1&sort=ExploreSorting_RECENTLY_LISTED"
carac_market_url = "https://msu.io/marketplace/character?page=1&sort=ExploreSorting_RECENTLY_LISTED"

cookie_file = "nft.json"
# service = Service(executable_path=chromedriver_path)
main_window = ""

def login():
    global main_window

    if market_type == "nft":
        driver.get(nft_market_url)
    else:
        driver.get(carac_market_url)


    main_window = driver.current_window_handle

def connectWallet():
    button = findElementByXPath(driver,"/html/body/header/div[2]/button[1]")
    button.click()
    time.sleep(1)
    button = findElementByXPath(driver,"/html/body/div[2]/div[2]/div/div[2]/div/div/button")
    button.click()
    switchWindow()
    loginWallet()
    goBackToMainWinodow()


def switchWindow():

    # WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > )
    time.sleep(10)
    connect_handle = driver.window_handles[-1]
    driver.switch_to.window(connect_handle)

def goBackToMainWinodow():
    driver.switch_to.window(main_window)

def click(offset):
    x,y = offset
    pyautogui.moveTo(x,y)
    pyautogui.click()
    time.sleep(1)

def loginConfirm():
    if login_pause:
        time.sleep(30000)

    click(login_btn_offset)

def signatureConfirm():
    if signature_pause:
        time.sleep(30000)

    click(signature_confirm_offset)
    click(signature_confirm_offset)

def inputPassword():
    if password_pause:
        time.sleep(30000)

    click(password_offset)

    pyautogui.write('benben456', interval=0.08)  # interval adds delay between key presses


def loginWallet():
    time.sleep(3)
    inputPassword()
    time.sleep(1)
    loginConfirm()
    time.sleep(3)
    signatureConfirm()

    # button = findElementByXPath(driver,"/html/body/div[1]/div/div/div/div/button")
    # button.click()
    time.sleep(1)

def clickFirstElementOffer():
    item = findElementByXPath(driver,"//article[1]/div/div[1]/div[1]")
    item.click()

    offer_btn = findElementByXPath(driver,"//button[span[text()='Offers']]")
    price_span = findElementByXPath(driver,"//div/div/div[2]/div[1]/div[1]/div[2]/div/div/span[1]")

    if not price_span:
        driver.back()

    price = parse_safe_number(price_span.text)
    offer = offerPrice(price)

    if offer and offer_btn:
        offer_btn.click()
        time.sleep(1)
        inputElementByXpath(driver,'//input[@inputmode="decimal"]',offer)
        time.sleep(1)

        make_offer_btn = findElementByXPath(driver,'//button[text()="Make offer"]')
        make_offer_btn.click()
        time.sleep(2)
        signatureConfirm()

        close_btn = findElementByXPath(driver,"//button[contains(@class,'close-btn')]")
        close_btn.click()

    driver.back()

    time.sleep(2)


def offerPrice(price):
    if price < range_low or price > range_high:
    # if price < 10000 or price > 500_000:
            return False
    offer = round(price * offer_mutiplier,0)
    offer += 0.999
    return offer


login()
connectWallet()
while True:
    try:
        clickFirstElementOffer()
    except Exception as e:
        login()
        time.sleep(5)

time.sleep(30000)
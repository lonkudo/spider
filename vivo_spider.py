from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

from mycookie import loadcookie
from savePage import save_page
from swtichToNewWindow import switchToNewWindow
from element import clickElement,clickText
from internet_now import get_internet_time


def vivo_spider():
    options = Options()
    options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"  # 启动这个爬虫的基础
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    target_url = "https://shop.vivo.com.cn/"
    cookie_file = "shop.vivo.com.cn_json_1745041492404.json"

    # Create driver with correct Service path
    # service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(options=options)

    count = 0  # 当前窗口数量
    old_hanldes = set()  # 窗口的句柄

    driver.get(target_url)

    loadcookie(driver, cookie_file)

    driver.get(target_url)

    title = driver.title

    old_hanldes.add(driver.current_window_handle)
    count += 1

    clickElement(driver, ".prod-img")

    old_hanldes, count = switchToNewWindow(driver, old_hanldes, count)

    clickText(driver, "iQOO 13")

    now = get_internet_time()

    old_hanldes,count = switchToNewWindow(driver,old_hanldes,count)
    clickElement(driver,"button.v-btn--brand")
    clickElement(driver, ".btn-submit")
    save_page(driver,"paying")

    time.sleep(300)

    driver.quit()



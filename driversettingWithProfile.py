import undetected_chromedriver as uc

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

def initDriver(gui):

    options = uc.ChromeOptions()
    options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"  # 启动这个爬虫的基础
    options.add_argument(
        "--user-data-dir=C:/BotProfile")  # Change path as needed

    options.add_argument("--profile-directory=Bot")  # Or "Profile 1", "Profile 2", etc.


    if gui == 'off':
        options.add_argument('--headless')
    # options.add_argument("start-maximized")

    # # Optional: set a realistic user-agent
    # options.add_argument(
    #     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    #     "AppleWebKit/537.36 (KHTML, like Gecko) "
    #     "Chrome/135.0.0.0 Safari/537.36"
    # )

    driver = uc.Chrome(options=options)


    driver.set_window_position(0, 0)
    driver.set_window_size(1600, 1200)
    actions = ActionChains(driver)

    return (driver,actions)






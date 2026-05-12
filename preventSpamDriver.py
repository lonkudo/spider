import undetected_chromedriver as uc

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

def initDriver(gui):

    options = uc.ChromeOptions()
    options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"  # 启动这个爬虫的基础
    if gui == 'off':
        options.add_argument('--headless')

    options.add_argument('--disable-gpu')

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("start-maximized")

    # Optional: set a realistic user-agent
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/144.0.7559.110 Safari/537.36"
    )
    options.add_argument("--force-device-scale-factor=0.8")

    driver = uc.Chrome(options=options)

    # Optional: spoof WebDriver flag
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """
    })

    # Anti-detection JavaScript spoofing
    driver.execute_cdp_cmd(
        'Page.addScriptToEvaluateOnNewDocument',
        {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                Object.defineProperty(navigator, 'platform', { get: () => 'Win32' });
                Object.defineProperty(navigator, 'userAgentData', {
                    get: () => ({
                        brands: [{brand: "Google Chrome", version: "138"}, {brand: "Chromium", version: "138"}],
                        platform: "Windows"
                    })
                });
            '''
        }
    )

    driver.set_window_position(3000, 0)
    driver.set_window_size(2500, 3000)
    actions = ActionChains(driver)

    return (driver,actions)






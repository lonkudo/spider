import time
import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains


def initDriver(gui):
    # 关键：必须用 uc.ChromeOptions()，不能用原生 Options()
    options = uc.ChromeOptions()

    # 指定你的Chrome路径（保持不变）
    options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

    # 无头模式
    if gui == 'off':
        options.add_argument('--headless=new')  # 新版无头，必须用=new

    # 高版本Chrome必加参数
    options.add_argument('--disable-gpu')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # 浏览器指纹（保持）
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/142.0.7444.134 Safari/537.36"
    )

    options.add_argument("--force-device-scale-factor=0.8")

    # ✅ 核心修复：uc 自带防检测，不要手动执行 execute_cdp_cmd
    driver = uc.Chrome(
        options=options,
        version_main=False,  # 自动匹配Chrome版本
        suppress_welcome_page=True  # 禁止欢迎页，防止窗口崩溃
    )

    time.sleep(1.5)

    # 窗口位置和大小（保持）
    driver.set_window_position(2000, 0)
    driver.set_window_size(4000, 1500)
    actions = ActionChains(driver)

    print('driver 启动成功！')
    return (driver, actions)
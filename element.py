from exceptiongroup import catch
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import re,time

from concurrent.futures import ThreadPoolExecutor,wait,FIRST_COMPLETED

short = 3
middle = 6
long = 30
very_long = 60


def findElement(driver,info):
    match = re.search(r'[.#]',info)
    if match:
        ret = findElementBySelecotr(driver,info)
    else:
        ret = findElementByText(driver,info)
    return ret


def findElementBySelecotr(driver,selector):
    try:
        element = WebDriverWait(driver, short, poll_frequency=0.1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
        return element
    except TimeoutException:
        return False

def findElementByText(driver,text):
    try:
        element = WebDriverWait(driver, short).until(
            EC.presence_of_element_located((
                By.XPATH, f'//*[contains(text(), "{text}")]'
            ))
        )
        return element
    except TimeoutException:
        return False

def findElements(driver, info):
    match = re.search(r'[.#]', info)
    if match:
        ret = findElementsBySelecotr(driver, info)
    else:
        ret = findElementsByText(driver, info)
    return ret

def findElementsBySelecotr(driver,selector):
    try:
        element = WebDriverWait(driver, short, poll_frequency=0.1).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
        )
        return element
    except TimeoutException:
        return False

def findElementsByText(driver,text):
    try:
        element = WebDriverWait(driver, short).until(
            EC.presence_of_all_elements_located((
                By.XPATH, f'//*[contains(text(), "{text}")]'
            ))
        )
        return element
    except TimeoutException:
        return False


def inputElement(driver,selector,text):

    element = WebDriverWait(driver, long , poll_frequency=0.1).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
    )
    element.clear()
    element.click()
    element.send_keys(text)

def inputElementByXpath(driver,xpath,text):
    element = WebDriverWait(driver, long, poll_frequency=0.1).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    element.clear()
    element.click()
    element.send_keys(text)

def clickElement(driver,selector):
    element = WebDriverWait(driver, long, poll_frequency=0.1).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )
    element.click()

def clickText(driver,text):
    # Wait for element by visible partial text
    element = WebDriverWait(driver, long).until(
        EC.element_to_be_clickable((
            By.XPATH, f'//*[contains(text(), "{text}")]'
        ))
    )
    element.click()

def findSubElementByText(driver,parent_element,text):
    print(parent_element.tag_name)
    element = parent_element.find_element(By.XPATH, f'.//*[contains(text(), "{text}")]')
    print(element)
    return element
def findSubElementBySelector(driver,parent_element,text):
    print(parent_element.text)
    element = parent_element.find_element(By.XPATH, f'.//*[contains(text(), "{text}")]')
    return element


def clickTextExact(driver,text):
    element = WebDriverWait(driver, short).until(
        EC.presence_of_element_located((
            By.XPATH, f'//*[normalize-space(text()="{text}")]'
        ))
    )
    element.click()

def findInputByPlaceholder(driver,placehoder):
    xpath = f'//input[@placeholder="{placehoder}"]'
    try:
        element = WebDriverWait(driver, short).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element
    except TimeoutException:
        return False

def findElementByXPath(driver,xpath, timeout=long):
    try:
        element = WebDriverWait(driver,timeout ).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element
    except TimeoutException:
        return False

def findElementByXPathClickable(driver,xpath, timeout=long):
    try:
        element = WebDriverWait(driver,timeout ).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        return element
    except TimeoutException:
        return False

def findElementsByXPath(driver,xpath,timeout=long ):
    try:
        element = WebDriverWait(driver, timeout ).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath))
        )
        return element
    except TimeoutException:
        return False


def inputByPlaceholder(driver,placehoder,text):
    xpath = f'//input[@placeholder="{placehoder}"]'
    element = WebDriverWait(driver, short).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    element.clear()
    element.send_keys(text)

def clickByPlaceholder(driver,placehoder):
    xpath = f'//input[@placeholder="{placehoder}"]'
    element = WebDriverWait(driver, short).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    element.click()

def clickByTitle(driver,title,wait_time=short):
    xpath = f'//*[@title="{title}"]'
    element = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    element.click()


def printElement(element):
    f = open('output.txt', 'a', encoding='utf-8')
    if isinstance(element, list):
        print('---list---',file=f)
        print('[',file=f)
        for item in element:
            try:
                print(item.get_attribute('outerHTML'),',',file=f)
            except Exception:
                print(item,',',file=f)
        print(']',file=f)
        print('---end---',file=f)
    elif isinstance(element, str):
        print('---str---',file=f)
        print(element, file=f)
        print('---end---',file=f)
    elif isinstance(element, dict):
        print('---dict---',file=f)
        print(element, file=f)
        print('---end---',file=f)
    else:
        print('---element---',file=f)
        print(element.get_attribute('outerHTML'), file=f)
        print('---end---', file=f)

    f.close()

def clickButtonInGroup(group,index):
    time.sleep(1)
    buttons = group.find_elements(By.CSS_SELECTOR, 'button')
    buttons[index].click()
    time.sleep(1)



def waitForElement_sync(driver, xpath, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element
    except TimeoutException:
        return None

def waitForResult_sync(driver, succ_xpath, fail_xpath):
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_success = executor.submit(waitForElement_sync, driver, succ_xpath, 10)
        future_failure = executor.submit(waitForElement_sync, driver, fail_xpath, 10)

        done, pending = wait([future_success, future_failure], return_when=FIRST_COMPLETED)

        for future in pending:
            future.cancel()

        result_future = done.pop()
        result_element = result_future.result()

        if result_future == future_success:
            return result_element, True
        else:
            return result_element, False
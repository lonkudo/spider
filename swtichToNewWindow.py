from selenium.webdriver.support.wait import WebDriverWait

def switchToNewWindow(driver,old_handles,count):
    WebDriverWait(driver,10).until(lambda d:len(d.window_handles) > count)

    for handle in driver.window_handles:
        if handle not in old_handles :
            driver.switch_to.window(handle)
            old_handles.add(handle)
            count += 1
            break

    return old_handles,count

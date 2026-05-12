# - coding = utf-8 -
# yepay siper auto recharge

import time
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from mycookie import loadcookie
from selenium.webdriver.common.by import By
from element import *
from selenium.common.exceptions import StaleElementReferenceException
from fb_report import writeReport, writeEverydayReport, writeEverydayAdsetReport ,writeYesterdayReport
from fb_handle_info import changeInfo,getID
from fb_time_range import get_time_range,get_everyday_range,get_start_day_from_time_range
from informations.fb import bm
from informations.fb_bms import bms,rearrange_bms,rearrange_teams

from preventSpamDriver import initDriver
from preventSpam import MouseGlider

from yepay_spider import go_card_spider, get_one_card_info, close_card_info, input_memo,save_card_info,create_one_card,open_card_info

from informations.yepay import yepay
from utils import parse_safe_number
from informations.fb_guard_options import *
import pyautogui



if len(sys.argv) == 2 and sys.argv[1] == 'off':
    driver,actions = initDriver('off')
else:
    driver,actions = initDriver('on')


mimic = MouseGlider(driver)
fb_url = "https://mbasic.facebook.com/"
ads_url = "https://adsmanager.facebook.com"

cookie_file = "fb.json"
# cookie_file = "fb_Toan.json"
# service = Service(executable_path=chromedriver_path)


rows_xpath = "/html/body/div[1]/div/div/div/div/div/span/div/div[1]/div/div[3]/div/div[2]/span/div/div/div/div/div[3]/div[1]/div[2]/div/div/div/div/div[1]/div[3]/span/div/div/div/div/div/div/div/div[3]/div"
# rows_xpath = "/html/body/div[1]/div/div/div/div/div/span/div/div[1]/div/div[3]/div/div[2]/span/div/div/div/div/div[3]/div[1]/div[2]/div/div/div/div/div[1]/div[3]/span/div/div/div/div/div/div/div[1]/div[3]/div"
# rows_xpath = "/html/body/div[1]/div/div/div/div[1]/div/span/div/div[1]/div/div[2]/div/div[2]/span/div/div/div/div/div[3]/div[1]/div[2]/div/div/div/div/div[1]/div[3]/span/div/div/div/div/div/div/div[1]/div[3]/div"


def login():
    driver.get(fb_url)
    loadcookie(driver, cookie_file)
    driver.get(fb_url)

def selectBM(bm_ins):
    element = findElementByXPath(driver,bm_ins.xp.bm)
    mimic.glide_and_click(element)

def go(url):
    driver.get(url)


def guard_script(option_list,range_start,range_end):
    # 最外层是 装饰器 接收的参数
    def decorator(func): # 中间层是装饰器，接收的是 函数
        def wrapper(bm_ins,tr,index):  # 里面是装饰器实现的功能
            option = tr.find_element(By.XPATH, bm_ins.xp.acc_trs_option).text
            if option in option_list and index >= range_start and index < range_end:
                print(index,": ",option, " in")
                ret = func(bm_ins,tr)
            else:
                print(index,": ",option, " pass")
                ret = None
            print(ret)
            return ret
        return wrapper
    return decorator

def walkAccounts(bm_ins,callback=()):
    results = []

    is_all_loaded = False

    while not is_all_loaded:

        trs = findElementsByXPath(driver,bm_ins.xp.acc_trs,very_long)
        last_tr = trs[-1]
        # check last_tr display is not none
        is_all_loaded = last_tr.value_of_css_property("display") != 'none'

        # scroll to the bottom of the page to load all accounts

        scroll_father_element = findElementByXPath(driver,"/html/body/div[1]/div[1]/div/span/div/div[1]/div[2]/div/div/div/div")

        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scroll_father_element)

        time.sleep(3)

    length = len(trs)
    count = length - 1
    # count = 2
    # length = 3

    while count >= 0 :
        # refind tr element each time because when you go in detail ,then the origin trs is gone
        tr = findElementsByXPath(driver,bm_ins.xp.acc_trs)[count]
        name = tr.find_element(By.XPATH, bm_ins.xp.acc_trs_name).text
        print(name)
        results.append(callback(bm_ins,tr,count))
        count -= 1
    print('walk ended')


    # filter out None in results
    results = [result for result in results if result is not None]
    return results



@guard_script(option_list,range_start,range_end)
def gatherAccountInfo(bm_ins,tr):
    id = tr.find_element(By.XPATH, bm_ins.xp.acc_trs_id).text
    name = tr.find_element(By.XPATH, bm_ins.xp.acc_trs_name).text
    status = tr.find_element(By.XPATH, bm_ins.xp.acc_trs_status).text
    balance = tr.find_element(By.XPATH, bm_ins.xp.acc_trs_balance).text
    option = tr.find_element(By.XPATH, bm_ins.xp.acc_trs_option).text
    info = {'id': id, 'name': name, 'status': status, 'balance': balance,'option': option}
    # comment these two line below to boback to previous version
    detail_info = goIntoAccountGetInfo(bm_ins,tr)
    info.update(detail_info)
    print(id)
    return info


@guard_script(option_list,range_start,range_end)
def pay(bm_ins,tr):
    option_element = tr.find_element(By.XPATH, bm_ins.xp.acc_trs_option)
    ret = None
    if option_element.text == "Pay now":
        mimic.glide_and_click(option_element)
        # 这个dom是 不停进行替换的 ，使用 abs path的方式不方便，
        # 按钮都是最后一个
        time.sleep(1)

        title = WebDriverWait(driver, 1000).until(
            EC.presence_of_element_located((By.XPATH, '//span[contains(text(),"Pay current balance")]'))
        )
        # Wait until the "Confirm" button appears in the new DOM
        btns = WebDriverWait(driver, 1000).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@role="button"]'))
        )

        last_btn = btns[-1]
        mimic.glide_and_click(last_btn)

        time.sleep(1)

        title = WebDriverWait(driver, 1000).until(
            EC.presence_of_element_located((By.XPATH, '//*[contains(text(),"Review your payment")]'))
        )
        # Wait until the "Confirm" button appears in the new DOM
        btns = WebDriverWait(driver, 1000).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@role="button"]'))
        )

        last_btn = btns[-1]
        mimic.glide_and_click(last_btn)

        closeSuccess = closePayDialog()
        if not closeSuccess:
            closeDialog()

        time.sleep(1)

    elif option_element.text == "Add funds":
        # get the balance that need to charge
        balance_element = tr.find_element(By.XPATH, bm_ins.xp.acc_trs_balance)
        currrent_balance = parse_safe_number(balance_element.text)
        id =  tr.find_element(By.XPATH, bm_ins.xp.acc_trs_id).text
        account = matchAccount(bm_ins.accounts,id)

        target_balance = account['target']

        # need_balance = round(target_balance - currrent_balance, 2)
        need_balance = 10
        mimic.glide_and_click(option_element)
        # 这个dom是 不停进行替换的 ，使用 abs path的方式不方便，
        # 按钮都是最后一个
        time.sleep(1)

        title = WebDriverWait(driver, 1000).until(
            EC.presence_of_element_located((By.XPATH, '//span[contains(text(),"Add funds")]'))
        )
        # 选择卡片
        img =  WebDriverWait(driver, 1000).until(
            EC.presence_of_element_located((By.XPATH, '//div/img[@aria-hidden="true"]'))
        )

        mimic.glide_and_click(img)

        inputElementByXpath(driver,'//input[@name="amount"]', '\b'* 10 + str(need_balance))


        # Wait until the "Confirm" button appears in the new DOM
        btns = WebDriverWait(driver, 1000).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@role="button"]'))
        )

        last_btn = btns[-1]
        mimic.glide_and_click(last_btn)


        title = WebDriverWait(driver, 1000).until(
            EC.presence_of_element_located((By.XPATH, '//*[contains(text(),"Review your payment")]'))
        )
        # Wait until the "Confirm" button appears in the new DOM
        btns = WebDriverWait(driver, 1000).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@role="button"]'))
        )

        last_btn = btns[-1]
        mimic.glide_and_click(last_btn)

        ret = closeProcesssingDialog()

    return ret


def goBack():
    driver.back()

def goBackByButton():
    back_btn = findElementByXPath(driver,'/html/body/div[1]/div[1]/div/span/div/div[1]/div[2]/div/div/div/div/div/div/div[2]/span/div/div/div[1]/div/div/div/div/div/div[1]/div/div[1]')
    if back_btn:
        mimic.glide_and_click(back_btn)

def closeDialog():
    close_btn = findElementByXPath(driver, '//div[@aria-label="Close"]')
    if close_btn:
        mimic.glide_and_click(close_btn)

def closePayDialog():
    # //div[@role="none"]//*[normalize-space(text())="Pay now" or normalize-space(text())="Done"]
    # if tag type is confirmed then use or in the []
    # if tag type is different then use it this way:
    # // div[ @ role = "none"] // span[normalize - space(text()) = "Pay now"] | // *[normalize - space(text()) = "Done"]

    ret = False
    close_btn = findElementByXPath(driver,'//div[@role="none"]//span[normalize-space(text())="Pay now"] | //*[normalize-space(text())="Done"]')
    if close_btn:
        mimic.glide_and_click(close_btn)
        countDown = 10
        while True:
            time.sleep(1)
            page_fixed_button = findElementByXPath(driver,'//*[normalize-space(text())="Payment methods"]')
            if page_fixed_button.is_displayed() and page_fixed_button.is_enabled():
                ret = True
                break
            countDown -= 1
            if countDown < 0:
                break
    else:
        close_btn = findElementByXPath(driver,'//div[@aria-label="Close"]')
        if close_btn:
            mimic.glide_and_click(close_btn)

    return ret


def closeProcesssingDialog():
    ret = False

    title = findElementByXPath(driver,'//span[contains(text(),"Processing")]')
    close_btn = findElementByXPath(driver,'//div[@aria-label="Close" and @role="button"]')

    if title:
        mimic.glide_and_click(close_btn)
        countDown = 10
        while True:
            time.sleep(1)
            page_fixed_button = findElementByXPath(driver,'//*[normalize-space(text())="Payment methods"]')
            if page_fixed_button.is_displayed() and page_fixed_button.is_enabled():
                ret = True
                break
            countDown -= 1
            if countDown < 0:
                break
    else:
        close_btn = findElementByXPath(driver,'//div[@aria-label="Close"]')
        if close_btn:
            mimic.glide_and_click(close_btn)

    return ret

def goWithCookie(url,cookie_file):
    driver.get(url)
    loadcookie(driver, cookie_file)
    driver.get(url)



def collectInfo():
    filtered_bms = filterScriptBms('collectInfo')

    for item in filtered_bms:
        bm_ins = bm(item)
        go(bm_ins.routes.billing_gate)
        selectBM(bm_ins)

        results = walkAccounts(bm_ins,gatherAccountInfo)
        ret = changeInfo(results)
        printElement(ret)

def payBms():
    filtered_bms = filterScriptBms('payBms')

    for item in filtered_bms:
        bm_ins = bm(item)
        go(bm_ins.routes.billing_gate)
        selectBM(bm_ins)
        walkAccounts(bm_ins,pay)

def report(report_id):
    reports = []
    rows = findElementsByXPath(driver,rows_xpath)
    if not rows: return None
    time.sleep(2)
    rows = findElementsByXPath(driver,rows_xpath)

    if len(rows)== 1:
        row = rows[0]
        try:
            name_cell = row.find_element(By.XPATH,"./div/div/div[1]/div")
        except:
            print('empty')
            return None

    for row in rows:
        msg = []
        name_cell = row.find_element(By.XPATH,"./div/div/div[1]/div")
        if not name_cell.text =='': msg.append(name_cell.text)
        other_cells = row.find_elements(By.XPATH,"./div/div/div[2]/div/div")
        for column_cell in other_cells:
            msg.append(parse_safe_number(column_cell.text))
        reports.append(msg)
        if name_cell.text =='': msg[0] = row.find_element(By.XPATH,"./div/div/div[2]/div/div").text
        msg.append(report_id)

    return reports

def reportEveryday(day_range,report_id):
    day = get_start_day_from_time_range(day_range)
    reports = []
    rows = findElementsByXPath(driver,rows_xpath)
    # rows = findElementsByXPath(driver,"/html/body/div[1]/div/div/div/div/div/span/div/div[1]/div[3]/div/div[2]/span/div/div/div/div/div[3]/div[1]/div[2]/div/div/div/div/div[1]/div[3]/span/div/div/div/div/div/div/div[1]/div[3]/span/div")
    if not rows: return None
    time.sleep(2)

    rows = findElementsByXPath(driver,rows_xpath)


    if len(rows)== 1:
        row = rows[0]

        try:
            name_cell = row.find_element(By.XPATH,"./div/div/div[1]/div")
        except:
            print('empty')
            return None

    for row in rows:
        msg = []
        name_cell = row.find_element(By.XPATH,"./div/div/div[1]/div")
        if not name_cell.text =='': msg.append(name_cell.text)

        other_cells = row.find_elements(By.XPATH,"./div/div/div[2]/div/div")
        # other_cells = row.find_elements(By.XPATH,"./div/div/div[2]/div/span")
        for column_cell in other_cells:
            msg.append(parse_safe_number(column_cell.text))
        msg.append(day)
        reports.append(msg)
        # if name_cell.text =='': msg[0] = row.find_element(By.XPATH,"./div/div/div[2]/div/span").text
        if name_cell.text =='': msg[0] = row.find_element(By.XPATH,"./div/div/div[2]/div/div").text
        msg.append(report_id)

    printElement(reports)

    return reports


def matchAccount(accounts,account_id):

    id = getID(account_id)
    for account in accounts:
        if account['id'] == id:
            return account
    return None


def goReport(bm_id,report_id,report_range):
    # report will be deleted when remove ad account from bm, so check report id
    report_url = f"https://adsmanager.facebook.com/adsmanager/reporting/business_view?business_id={bm_id}&selected_report_id={report_id}&{report_range}&event_source=AUTO_REDIRECT"
    go(report_url)

def goAccountReport(account_id,report_id,report_range):
    report_url = f"https://adsmanager.facebook.com/adsmanager/reporting/view?act={account_id}&ads_manager_write_regions=true&selected_report_id={report_id}&{report_range}&event_source=AUTO_REDIRECT"
    go(report_url)

def goDetails(bm_ins,account):
    details_url = f"https://business.facebook.com/billing_hub/accounts/details?asset_id={account['id']}&business_id={bm_ins['business_id']}"
    go(details_url)

def filterScriptBms(script_name):
    filtered_bms = []
    for bm_ins in bms:
        if script_name in bm_ins['script']:
            filtered_bms.append(bm_ins)
    return filtered_bms

def filterRearrangeBms(script_name):
    filtered_bms = []
    for bm_ins in rearrange_bms:
        if script_name in bm_ins['script']:
            filtered_bms.append(bm_ins)
    return filtered_bms


def getAllReports():
    filtered_bms = filterScriptBms('report')

    bm_reports = []
    for bm_ins in filtered_bms:
        for bm_report in bm_ins['reports']:
            print(bm_ins['business_name'], bm_report['id'])
            try:
                goReport(bm_ins['business_id'],bm_report['id'],get_time_range(bm_report['start'],bm_report['end']))
            except Exception as e:
                goAccountReport(bm_ins['account_id'],bm_report['id'],get_time_range(bm_report['start'],bm_report['end']))
            ret = report(bm_report['id'])
            if ret: bm_reports.append(ret)

    printElement(bm_reports)
    handleReports(bm_reports)

    return bm_reports

def getYesterdayReports():
    filtered_bms = filterScriptBms('report')

    bm_reports = []
    for bm_ins in filtered_bms:
        for bm_report in bm_ins['reports']:

            if not bm_report['end'] == 'now': continue # skip report that is not up to date

            try:
                goReport(bm_ins['business_id'],bm_report['id'],get_time_range('yesterday','yesterday'))
            except Exception as e:
                print(e)
                goAccountReport(bm_ins['account_id'],bm_report['id'],get_time_range('yesterday','yesterday'))
            ret = report(bm_report['id'])
            if ret: bm_reports.append(ret)

    printElement(bm_reports)
    handleYesterdayReports(bm_reports)

    return bm_reports

def handleReports(reports):
    flat_table = [row for sublist in reports for row in sublist]
    # flat_table  的数据是 页面的数据

    # if accounts in bm fit in row in flat_table then it matched
    for bm_ins in rearrange_bms:
        table = []
        table_name = bm_ins['business_name']
        for account in bm_ins['accounts']:
            match_flag = False # 对于 fb_report 还没有数据的处理 自己给一个值

            for row in flat_table:  # 对于fb_report 有数据的账户的处理
                if account['id'] == row[10] and row[-1] in bm_ins['reports']: # row[10] id row[-1] report_id
                    match_flag = True
                    row.pop(-1)
                    table.append(row)

            if not match_flag: # 对于 fb_report 还没有数据的处理 自己给一个值
                row = [account['name'],'-','-','-','-','-','-','-','-','-',account['id'],'-',None]
                table.append(row)

        writeReport(table,bm_ins)
    # writeReport(flat_table)

def handleYesterdayReports(reports):
    flat_table = [row for sublist in reports for row in sublist]
    # flat_table  的数据是 页面的数据

    # if accounts in bm fit in row in flat_table then it matched
    for bm_ins in rearrange_bms:
        table = []
        table_name = bm_ins['business_name']
        for account in bm_ins['accounts']:
            match_flag = False # 对于 fb_report 还没有数据的处理 自己给一个值

            for row in flat_table:  # 对于fb_report 有数据的账户的处理
                print(row, row[-1])
                if account['id'] == row[10] and row[-1] in bm_ins['reports']: # row[10] id row[-1] report_id
                    match_flag = True
                    row.pop(-1)
                    table.append(row)
                    print('matched')
                else:
                    print('not')

            if not match_flag: # 对于 fb_report 还没有数据的处理 自己给一个值
                row = [account['name'],'-','-','-','-','-','-','-','-','-',account['id'],'-',None]
                table.append(row)

        writeYesterdayReport(table,bm_ins,sheet_name=table_name)
    # writeReport(flat_table)

def goDetail(bm_ins,tr):
    id = tr.find_element(By.XPATH, bm_ins.xp.acc_trs_id)
    mimic.glide_and_click(id)

def returnFromDetail():
    # return_btn = findElementByXPath(driver,"/html/body/div[1]/div[1]/div/span/div/div[1]/div[2]/div/div/div/div/div/div/div[2]/span/div/div/div[1]/div/div/div/div/div/div[1]/div/div[1]")
    # mimic.glide_and_click(return_btn)
    # goBack()
    goBackByButton()
    time.sleep(2)

def getAccountInfo():
    info = {}
    spending_limit = findElementByXPath(driver,"//div/div/div[2]/div[1]/div[3]/div/div/div/span/div[1]/span")
    time.sleep(3)
    if spending_limit:
        info['spending_limit'] = spending_limit.text
    else:
        info['threshold'] = 0
        info['spending_limit'] = 0
        info['currency'] = None
        info['card'] = None
        return info


    threshold = findElementByXPath(driver,"//div[3]/div/div/div[2]/div[1]/div/div[2]/div/span")
    currency = findElementByXPath(driver,"//div/div/div[2]/div[1]/div[2]/div/div[3]/div[2]/div")
    card = findElementByXPath(driver,"//div/div/div[2]/div[1]/div[3]/div/div[3]/div/div/div/span")

    if threshold:
        info['threshold'] = threshold.text
    else:
        # if threshold can't read then return directly
        info['threshold'] = 0

    if currency:
        info['currency'] = currency.text
    else:
        info['currency'] = 0

    if card:
        info['card'] = card.text
    else:
        info['card'] = 0

    return info

def goIntoAccountGetInfo(bm_ins,tr):
    goDetail(bm_ins,tr)

    for i in range(5):
        try:
            detail_info = getAccountInfo()
            break
        except StaleElementReferenceException:
            time.sleep(1)

    returnFromDetail()
    return detail_info

def bindBms():
    filtered_bms = filterScriptBms('bindBms')

    go_card_spider()
    for item in filtered_bms:
        bm_ins = bm(item)
        go(bm_ins.routes.billing_gate)
        selectBM(bm_ins)
        walkAccounts(bm_ins,goIntoAccountBindPayment)



@guard_script(option_list,range_start,range_end)
def goIntoAccountBindPayment(bm_ins,tr):
    goDetail(bm_ins, tr)
    bindBussiness()
    returnFromDetail()

def getTimezone():
    sign,zone = tz[0],tz[1:]
    reverse_sign =  '-' if sign == '+' else '+'
    std_zone = '0'+zone if len(zone)== 1 else zone
    timezone = f'Etc/GMT{reverse_sign}{zone} (GMT{sign}{std_zone}:00)'
    return timezone

def bindBussiness():

    time.sleep(middle)

    edit_btn = findElementByXPath(driver,'//div[@role="button" and contains(.,"Edit")]')
    edit_btn.click()

    dialog_title = findElementByXPath(driver,'//span[text()="Tax Information"]')
    time.sleep(middle)

    # check if Business Info already filled

    business_name_input = findElementByXPath(driver,'//input[following-sibling::*[text()="Add a name"]] | //input[preceding-sibling::*[text()="Add a name"]]')
    create_one_card()
    info = get_one_card_info()
    if business_name_input and business_name_input.get_attribute("value") == '':

        # select the country
        country_div = findElementByXPath(driver,'//div[following-sibling::*[text()="Country/region"]]/div | //div[preceding-sibling::*[text()="Country/region"]]/div')
        country_div.click()
        time.sleep(middle)

        option = findElementByXPath(driver,'//div[@role="option" and contains(., "United States of America")]')
        option.click()
        time.sleep(middle)

        # select the currency
        currency_divs = findElementsByXPath(driver,'//div[following-sibling::*[text()="Currency"]]/div | //div[preceding-sibling::*[text()="Currency"]]/div')
        currency_div = currency_divs[-1]
        currency_div.click()
        time.sleep(middle)

        option = findElementByXPath(driver,'//div[@role="option" and contains(., "US Dollars")]')
        option.click()
        time.sleep(middle)

        # select the Time zone
        timezone_div = findElementByXPath(driver,'//div[following-sibling::*[text()="Time zone"]]/div | //div[preceding-sibling::*[text()="Time zone"]]/div')
        timezone_div.click()
        time.sleep(middle)

        option = findElementByXPath(driver,f'//div[@role="option" and contains(., "{getTimezone()}")]')
        option.click()
        time.sleep(middle)



        # input State
        state_input = findElementByXPath(driver,'//input[following-sibling::*[text()="State, province or region"]] | input[preceding-sibling::*[text()="State, province or region"]]',middle)
        if state_input:
            state_input.click()
            state_input.send_keys(info['state'])
            time.sleep(middle)

        # select the state
        state_select = findElementByXPath(driver,'//div[following-sibling::*[text()="State"]]/div | //div[preceding-sibling::*[text()="State"]]/div',middle)
        if state_select:
            state_select.click()
            time.sleep(middle)
            option = findElementByXPath(driver,f'//div[@role="option" and contains(., "{info["state"]}")]')
            option.click()
            time.sleep(middle)

        # select State


        # input Business name
        business_name_input = findElementByXPath(driver,'//input[following-sibling::*[text()="Add a name"]] | //input[preceding-sibling::*[text()="Add a name"]]')
        business_name_input.click()
        business_name_input.send_keys(info['shop_name'])
        time.sleep(middle)

        # input city
        city_input = findElementByXPath(driver,'//input[following-sibling::*[text()="City or town"]] | //input[preceding-sibling::*[text()="City or town"]]')
        city_input.click()
        city_input.send_keys(info['town'])
        time.sleep(middle)

        # # select the country
        # state_div = findElementByXPath(driver,'')
        # state_div.click()
        # time.sleep(2)


        # input Zip code
        zipcode_input = findElementByXPath(driver,'//input[following-sibling::*[text()="ZIP code"]] | //input[preceding-sibling::*[text()="ZIP code"]]')
        zipcode_input.click()
        zipcode_input.send_keys(info['zipcode'])
        time.sleep(middle)

        # input address
        address_input = findElementByXPath(driver,'//input[following-sibling::*[text()="Street address 1"]] | //input[preceding-sibling::*[text()="Street address 1"]]')
        address_input.click()
        address_input.send_keys(info['address'])
        time.sleep(middle)

        save_btn = findElementByXPath(driver,'//div[@role="button" and contains(., "Save")]')
        save_btn.click()
        time.sleep(long)

    # close dialog
    close_btn = findElementByXPath(driver,'//div[@aria-label="Close"]')
    if close_btn:
        close_btn.click()
    time.sleep(middle)

    # click add payment
    add_payment_btn = findElementByXPath(driver,'//div[@role="button" and contains(., "Add payment method")]')
    add_payment_btn.click()
    time.sleep(middle)

    # click next button
    next_btns = findElementsByXPath(driver,'//div[@role="button" and contains(., "Next")]')
    next_btns[-1].click()
    time.sleep(middle)

    # input name on card
    name_input = findElementByXPath(driver,'//input[following-sibling::*[text()="Name on card"]] | //input[preceding-sibling::*[text()="Name on card"]]')
    name_input.click()
    name_input.send_keys(info['name'])
    time.sleep(middle)

    # input card_num
    card_input = findElementByXPath(driver,'//input[following-sibling::*[text()="Card number"]] | //input[preceding-sibling::*[text()="Card number"]]')
    card_input.click()
    card_input.send_keys(info['card_num'])
    time.sleep(middle)

    # input expire_date
    expire_date_input = findElementByXPath(driver,'//input[following-sibling::*[text()="MM/YY"]] | //input[preceding-sibling::*[text()="MM/YY"]]')
    expire_date_input.click()
    expire_date_input.send_keys('\b'*10 + info['expire_date'])
    time.sleep(middle)

    # input cvv
    cvv_input = findElementByXPath(driver,'//input[following-sibling::*[text()="CVV"]] | //input[preceding-sibling::*[text()="CVV"]]')
    cvv_input.click()
    cvv_input.send_keys('\b'*15 + info['cvv'])
    time.sleep(middle)

    save_btn = findElementByXPath(driver,'//div[@role="button" and contains(.,"Save")]')
    save_btn.click()
    time.sleep(long)

    close_btn = findElementByXPath(driver,'//div[@aria-label="Close"]')
    close_btn.click()
    time.sleep(middle)

    # get_one_card_info()
    close_card_info()
    # get_one_card_info()
    # input_memo()
    # save_card_info()


def handleEveryDayReports(reports):
    flat_table = [row for sublist in reports for row in sublist]
    # flat_table  的数据是 页面的数据
    printElement(flat_table)

    # if accounts in bm fit in row in flat_table then it matched
    rearrange_bms = filterRearrangeBms('everydayReport')

    for bm_ins in rearrange_bms:
        table = []
        table_name = bm_ins['business_name']
        for account in bm_ins['accounts']:
            match_flag = False # 对于 fb_report 还没有数据的处理 自己给一个值

            for row in flat_table:  # 对于fb_report 有数据的账户的处理
                print(row)
                if account['id'] == row[10] and row[-1] in bm_ins['reports']: # row[10] id row[-1] report_id
                    match_flag = True
                    # 已充值金额从bm_ins里面拿
                    row.pop(-1)
                    table.append(row)

            if not match_flag: # 对于 fb_report 还没有数据的处理 自己给一个值
                row = [account['name'],'-','-','-','-','-','-','-','-','-',account['id'],'-',None]
                table.append(row)

        printElement(table)
        writeEverydayReport(table,bm_ins,sheet_name=table_name)

def getEveryDayReports():
    bms = filterScriptBms('everydayReport')

    bm_reports = []

    for bm_ins in bms:
        for bm_report in bm_ins['reports']:
            range_list = get_everyday_range(bm_report['start'],bm_report['end'])
            for day_range in range_list:
                print(bm_ins['business_name'],bm_report['id'],day_range)
                goReport(bm_ins['business_id'],bm_report['id'],day_range)
                ret = reportEveryday(day_range,bm_report['id'])
                if ret: bm_reports.append(ret)

    printElement(bm_reports)
    handleEveryDayReports(bm_reports)
    return bm_reports



def handleEveryDayAdsetReports(reports):
    flat_table = [row for sublist in reports for row in sublist]
    # flat_table  的数据是 页面的数据
    for team in rearrange_teams:
        table = []
        for row in flat_table:  # 对于fb_report 有数据的账户的处理
            if row[-1] in team['adset_reports']:  # row[10] id row[-1] report_id
                row.pop(-1)
                print(row)
                table.append(row)

        writeEverydayAdsetReport(table,team['team_name'])

def getEveryDayAdsetReports():
    bms = filterScriptBms('everydayAdsetReport')
    bm_reports = []

    for bm_ins in bms:
        for bm_report in bm_ins['adset_reports']:
            range_list = get_everyday_range(bm_report['start'],bm_report['end'])
            for day_range in range_list:
                goReport(bm_ins['business_id'],bm_report['id'],day_range)

                ret = reportEveryday(day_range,bm_report['id'])
                if ret: bm_reports.append(ret)

    handleEveryDayAdsetReports(bm_reports)
    return bm_reports

def nameAccount():
    bms = filterScriptBms('everydayAdsetReport')
    for bm_ins in bms:
        goAccountSettings(bm_ins['business_id'])


def goAccountSettings(bm_id):
    go(f'https://business.facebook.com/latest/settings/ad_accounts/?business_id={bm_id}')


def walkAccountsInSettings():
    trs = findElementsByXPath(driver,'//table[@aria-label="Business assets"]/tbody/tr')
    for tr in trs:
        mimic(tr)


def greenAds():
    bms = filterScriptBms('greenAds')

    for bm_ins in bms:
        for acc in bm_ins['accounts']:
            goCampaigns(bm_ins['business_id'],acc['id'])
            createCampaign()



def goCampaigns(bm_id,acc_id):
    # go to campaigns page
    go(f'https://adsmanager.facebook.com/adsmanager/manage/campaigns?business_id={bm_id}&act={acc_id}#')
    time.sleep(5)


def createCampaign():
    # create green ads campaign
    create_btn = findElementByXPath(driver,'//div[span[div[div[div[text()="Create"]]]]]')
    mimic.glide_and_click(create_btn)
    time.sleep(3)

    # click Engagement
    engagement_btn = findElementByXPath(driver,'//div[@id="objectiveContainerOUTCOME_ENGAGEMENT"]')
    mimic.glide_and_click(engagement_btn)
    time.sleep(3)

    # click continue
    continue_btn = findElementByXPath(driver,'//div[@data-auto-logging-component-type="GeoButton" and contains(., "Continue")]')
    mimic.glide_and_click(continue_btn)
    time.sleep(3)

    # click Manual engagement campaign
    manual_elements = findElementsByXPath(driver,'//div[div[div[div[text()="Create an engagement campaign from scratch for finer control over all settings."]]]]')
    manual_btn = manual_elements[0]
    mimic.glide_and_click(manual_btn)
    time.sleep(3)

    # click continue
    continue_btn = findElementByXPath(driver,'//div[@data-auto-logging-component-type="GeoButton" and contains(., "Continue")]')
    mimic.glide_and_click(continue_btn)
    time.sleep(5)

    # is Advantage+ Campaign
    title = findElementByXPath(driver,'//div[text()="Advantage+ Campaign Budget"]')
    if title:
        print('in')
        switchs = findElementsByXPath(driver,'//input[@role="switch"]')
        advance_campaign_switch = switchs[1]
        value = advance_campaign_switch.get_attribute('aria-checked')
        if value == 'false':
            print('area-checked is false')
            advance_campaign_switch.click()

        time.sleep(2)
    else:
        print('not in')
        # click budget strategy
        budget_strategy_btn = findElementsByXPath(driver,'//div[div[div[div[span[text()="Budget strategy"]]]]]')[0]
        mimic.glide_and_click(budget_strategy_btn)
        time.sleep(2)

        # click campaign budget
        campaign_budget_btn = findElementByXPath(driver,'//div[div[div[div[text()="Campaign budget"]]]]')
        mimic.glide_and_click(campaign_budget_btn)
        time.sleep(3)

    # input amount

    input = findElementByXPath(driver, '//input[@placeholder="Please enter amount"]')
    input.click()
    input.send_keys('\b'*10 + '100')  # clear input and set amount to 100
    time.sleep(3)



    # click next button
    next_btn = findElementByXPath(driver,'//div[@data-auto-logging-component-type="GeoButton" and contains(., "Next")]')
    mimic.glide_and_click(next_btn)
    time.sleep(5)


    comboBoxes = findElementsByXPath(driver,'//div[@role="combobox"]')


    # select destination
    message_dest_div = findElementByXPath(driver,'//div[text()="Message destinations"]')
    if not message_dest_div:

        dest_box = comboBoxes[0]
        mimic.glide_and_click(dest_box)
        time.sleep(2)

        dest_option = findElementByXPath(driver,'//div[span[text()="Message destinations"]]')
        mimic.glide_and_click(dest_option)
        time.sleep(2)

    # select Page

    page_btn = findElementByXPath(driver,'//div[div[div[div[text()="Facebook Page"]]]]')
    mimic.glide_and_click(page_btn)
    time.sleep(2)

    # select Lucky554
    option_btn = findElementByXPath(driver,'//div[@role="option" and contains(., "Lucky554")]')
    mimic.glide_and_click(option_btn)
    time.sleep(3)

    # select Performance goal
    comboBoxes = findElementsByXPath(driver,'//div[@role="combobox"]')
    dest_box = comboBoxes[-1]
    mimic.glide_and_click(dest_box)
    time.sleep(2)


    # select maximize link click

    # select Lucky554
    option_btn = findElementByXPath(driver,'//div[@role="option" and contains(., "Maximize number of link clicks")]')
    mimic.glide_and_click(option_btn)
    time.sleep(3)

    # click next button
    next_btn = findElementByXPath(driver,'//div[@data-auto-logging-component-type="GeoButton" and contains(., "Next")]')
    mimic.glide_and_click(next_btn)
    time.sleep(5)

    # click Ad setup
    setup_btn = findElementByXPath(driver,'//div[text()="Create ad" or text()="Use existing content" ]')
    mimic.glide_and_click(setup_btn)
    time.sleep(2)


    # select createAd
    option_btn = findElementByXPath(driver,'//div[@role="option" and contains(., "Create ad")]')
    mimic.glide_and_click(option_btn)
    time.sleep(2)

    # click off three select Multi-advertiser Website events Offline events

    selects = findElementsByXPath(driver,'//input[following-sibling::div[div[@role="presentation"]]]')
    for select_box in selects:
        value = select_box.get_attribute("aria-checked")
        if value == "true": select_box.click()
        time.sleep(2)

    # click Setup creative
    setup_creative_btn = findElementByXPath(driver,'//div[span[div[div[div[text()="Set up creative"]]]]]')
    mimic.glide_and_click(setup_creative_btn)
    time.sleep(2)

    # click Image ad
    image_ad_btn = findElementByXPath(driver,'//div[div[text()="Image ad"]]')
    mimic.glide_and_click(image_ad_btn)
    time.sleep(2)

    # click upload button
    upload_btn = findElementByXPath(driver,'//div[@data-auto-logging-component-type="GeoButton" and contains(., "Upload")]')
    mimic.glide_and_click(upload_btn)
    time.sleep(5)

    # select local picture
    keyBoardInput()

    # click first Image
    grids = findElementsByXPath(driver,'//div[@class="ReactVirtualized__Grid__innerScrollContainer"]')
    pic_grid = grids[1]
    first_pic = pic_grid.find_element(By.XPATH,'./div[1]') #xpath start from 1
    mimic.glide_and_click(first_pic)
    time.sleep(2)


    # click next button
    for i in range(5):
        next_btn = findElementByXPath(
            driver,
            '//div[@data-auto-logging-component-type="GeoButton" and (' +
            'contains(normalize-space(.), "Next") or ' +
            'contains(normalize-space(.), "Skip and continue") or ' +
            'contains(normalize-space(.), "Done"))]'
        )
        mimic.glide_and_click(next_btn)
        time.sleep(5)

    # click Publish button
    next_btn = findElementByXPath(driver,'//div[@data-auto-logging-component-type="GeoButton" and contains(., "Publish")]')
    mimic.glide_and_click(next_btn)
    time.sleep(10)


def keyBoardInput():
    pyautogui.typewrite("1.jpg")
    time.sleep(3)
    pyautogui.hotkey("alt","o")

    time.sleep(5)

#
login()
# # # # go_card_spider()
# collectInfo()
# # # # payBms()
getAllReports()
# # getYesterdayReports()

# getEveryDayReports()
# getEveryDayAdsetReports()
# bindBms() # 别忘记改时区
# go_card_spider()
# cards = yepay("cards")
# open_card_info(cards)
# input_memo()
# save_card_info()
# get_one_card_info()
# input_memo()
# save_card_info()

# greenAds()
# reports= [
# [['ALL_IL1_1386691932835759_+7', 48578, 58903, 1.21, 1084, 0.74, 120, 6.67, 20, 40.03, '1386691932835759', 800.69, '', '1586518262475548']] ,
# [['ALL_OL2_1637465567624430_+7', 30256, 35785, 1.18, 854, 0.68, 90, 6.46, 15, 38.79, '1637465567624430', 581.83, '', '1568314657740178'], ['ALL_OL1_902298178897708_+7', 463, 463, 1.0, 9, 0.9, '—', '—', '—', '—', '902298178897708', 8.12, '', '1568314657740178']] ,
# [['AHX_NT9_1524936862083966_+8', 80368, 145572, 1.81, 4055, 0.08, 29, 11.53, 13, 25.71, '1524936862083966', 334.25, '', '1296351442535198']] ,
# [['ALL_NT2_824420523551719_+7', 1281885, 2555222, 1.99, 33801, 0.72, 7627, 3.2, 1472, 16.58, '824420523551719', 24398.94, '', '1300781112092231'], ['ALL_NT3_607892639080942_+7', 5350, 6078, 1.14, 357, 0.62, 42, 5.29, 6, 37.05, '607892639080942', 222.3, '', '1300781112092231']] ,
# [['DONG_NT7_1872742280006230_+7', 47640, 253046, 5.31, 3107, 0.25, 13, 60.92, 5, 158.39, '1872742280006230', 791.94, '', '1300831638753845'], ['DONG_NT6_1860483638172512_+7', 36502, 147415, 4.04, 1395, 0.32, 7, 64.31, 1, 450.18, '1860483638172512', 450.18, '', '1300831638753845']] ,
# [['AHX_LA7_1174162521357165_+8-XIGUA', 120206, 167772, 1.4, 2310, 1.56, 404, 8.92, 248, 14.53, '1174162521357165', 3603.9, '', '1832442804100250'], ['AHX_LA8_1153349779845407_+8-LT', 106041, 149323, 1.41, 1280, 2.12, 151, 17.95, 182, 14.89, '1153349779845407', 2710.33, '', '1832442804100250'], ['AHX_LA5_1128861109232798_+8', 32795, 45445, 1.39, 442, 1.52, 58, 11.55, 24, 27.92, '1128861109232798', 670.08, '', '1832442804100250'], ['AHX_LA6_814295434544670_+8', 681, 702, 1.03, 17, 0.2, '—', '—', '—', '—', '814295434544670', 3.33, '', '1832442804100250']] ,
# [['AHX_LA1_1221561013412370_+8', 219619, 367913, 1.68, 7410, 0.72, 385, 13.82, 578, 9.21, '1221561013412370', 5322.01, '', '1842210649790132']] ,
# [['AHX_HB2_1939673220128344_+8', 45791, 70929, 1.55, 2401, 0.16, 29, 13.48, 13, 30.07, '1939673220128344', 390.96, '', '862711166445852']] ,
# [['BIG_KY2_841331798330458_+7', 718031, 1499879, 2.09, 65283, 0.35, 11050, 2.08, 2055, 11.16, '841331798330458', 22932.58, '', '814300457981875'], ['BIG_KY1_2299318063842854_+7', 274618, 662065, 2.41, 40287, 0.52, 11242, 1.85, 2618, 7.94, '2299318063842854', 20777.28, '', '814300457981875']] ,
# [['ALL_A5_661889550207704_+7', 2595825, 6379353, 2.46, 165855, 0.35, 22127, 2.63, 3071, 18.98, '661889550207704', 58274.95, '', '1859985771258382'], ['BIG_C8_1256488806008345_+7', 3231976, 7546526, 2.33, 49483, 0.95, 7975, 5.89, 2061, 22.77, '1256488806008345', 46933.08, '', '1859985771258382'], ['ALL_C6_1407736730479167_+7', 1055852, 1440263, 1.36, 42870, 0.49, 5640, 3.7, 991, 21.05, '1407736730479167', 20864.92, '', '1859985771258382'], ['NINE_C9_1940730006332009_+7', 438107, 503901, 1.15, 1241, 2.85, '—', '—', 6, 589.21, '1940730006332009', 3535.26, '', '1859985771258382'], ['BIG_A6_735598362184116_+7', 1376, 1633, 1.19, 49, 0.38, 5, 3.68, 2, 9.21, '735598362184116', 18.41, '', '1859985771258382']] ,
# [['ALL_NT1_1375132304189348_+7', 27433, 44842, 1.63, 2049, 0.48, 329, 3.01, 72, 13.74, '1375132304189348', 989.2, '', '25889777367286174']] ,
# ]
# handleReports(reports)


time.sleep(3000)


# - coding = utf-8 -
# yepay siper auto recharge

import sys
import time

from mycookie import loadcookie
from selenium.webdriver.common.by import By
from element import *
from fb_report import writeIt,updateIt
from fb_handle_info import getID
from fb_time_range import get_everyday_range,get_start_day_from_time_range
from informations.fb_bms import bms,rearrange_bms

from preventSpamDriver import initDriver
from preventSpam import MouseGlider

from utils import parse_safe_number

from datetime import datetime,timedelta


if len(sys.argv) == 2 and sys.argv[1] == 'off':
    driver,actions = initDriver('off')
else:
    driver,actions = initDriver('on')
mimic = MouseGlider(driver)
#
# driver = {}
# mimic = {}


fb_url = "https://mbasic.facebook.com/"
ads_url = "https://adsmanager.facebook.com"

cookie_file = "fb.json"
# cookie_file = "fb_Toan.json"
# service = Service(executable_path=chromedriver_path)


no_rows_xpath = "//div[contains(text(),'No data') or contains(text(),'in the future')]"
rows_xpath = "/html/body/div[1]/div/div/div/div[1]/div/span/div/div[1]/div/div[3]/div/div[2]/span/div/div/div/div/div[3]/div[1]/div[2]/div/div/div/div/div[1]/div[3]/span/div/div/div/div/div/div/div[1]/div[3]/span/div/div"

header_rows_xpath = "/html/body/div[1]/div/div/div/div/div/span/div/div[1]/div/div[3]/div/div[2]/span/div/div/div/div/div[3]/div[1]/div[2]/div/div/div/div/div[1]/div[3]/span/div/div/div/div/div/div/div[1]/div[2]/div[2]/div/div"
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

def goWithCookie(url,cookie_file):
    driver.get(url)
    loadcookie(driver, cookie_file)
    driver.get(url)


def getReportHeader():
    time.sleep(1)
    headers = ['Account Name']
    header_rows = findElementsByXPath(driver,header_rows_xpath)
    printElement(header_rows)
    for header_row in header_rows:
        try:
            text_div = header_row.find_element(By.XPATH,".//div[normalize-space(text()) != '']")
            headers.append(text_div.text)
        except Exception:
            pass


    headers.append("memo")
    headers.append("date")
    headers.append("report_id")


    return headers



def reportOneDay(day_range,report_id,header):
    """ get report of one day, from day_range"""

    day = get_start_day_from_time_range(day_range)
    reports = []
    time.sleep(5)
    element, isFound = waitForResult_sync(driver,succ_xpath=rows_xpath,fail_xpath=no_rows_xpath)
    print(day_range," ", isFound)
    if not isFound: return None

    rows = findElementsByXPath(driver,rows_xpath)

    if len(rows)== 1:
        row = rows[0]

        try:
            name_cell = row.find_element(By.XPATH,"./div[1]/div[1]/div[1]")
        except:
            print('empty')
            return None

    for row in rows:
        msg = []
        name_cell = row.find_element(By.XPATH,"./div[1]/div[1]/div[1]")
        if not name_cell.text =='': msg.append(name_cell.text)

        other_cells = row.find_elements(By.XPATH,"./div[1]/div[2]/div[1]/span")
        # other_cells = row.find_elements(By.XPATH,"./div/div/div[2]/div/span")
        for column_cell in other_cells:
            msg.append(parse_safe_number(column_cell.text))
        msg.append(day)
        reports.append(msg)
        # if name_cell.text =='': msg[0] = row.find_element(By.XPATH,"./div/div/div[2]/div/span").text
        if name_cell.text =='': msg[0] = row.find_element(By.XPATH,"./div[1]/div[2]/div[1]/span").text
        msg.append(report_id)


    new_report = []
    for item in reports:
        new_item = {}
        for index,title in enumerate(header):
            new_item[title] = item[index]
        new_report.append(new_item)

    return new_report


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


def handleDayToDayReports(reports,range = "all"):
    flat_table = [row for sublist in reports for row in sublist]
    # flat_table  的数据是 页面的数据
    # printElement(flat_table)
    # if accounts in bm fit in row in flat_table then it matched
    rearrange_bms = filterRearrangeBms('dayTodayReport')


    for bm_ins in rearrange_bms:
        table = []
        for account in bm_ins['accounts']:
            match_flag = False # 对于 fb_report 还没有数据的处理 自己给一个值
            new_row = {}

            for row in flat_table:  # 对于fb_report 有数据的账户的处理
                if account['id'] == row['Account ID'] and row['report_id'] in bm_ins['reports']:
                    match_flag = True
                    # 已充值金额从bm_ins里面拿
                    new_row = {key: row.get(key, "-") for key in bm_ins['header'] if key in row}
                    table.append(new_row)


            if not match_flag: # 对于 fb_report 还没有数据的处理 自己给一个值
                for field_name in bm_ins['header']:
                    new_row[field_name] = "-"
                new_row["Account Name"] = account['name']
                new_row["Account ID"] = account['id']
                new_row["Amount spent"] = account.get('spent','-')
                table.append(new_row)

        if range == "all":
            writeIt(table,bm_ins)
        else:
            updateIt(table,bm_ins)

def genRange(bm_start: str, days):
    """
    days: "all" or an integer (number of days)
    returns YYYY-MM-DD string
    """
    if days == "all":
        return bm_start

    if not isinstance(days, int):
        raise ValueError("days must be 'all' or an integer")

    start = datetime.strptime(bm_start, "%Y-%m-%d")
    range_start = datetime.now() - timedelta(days=days)

    return max(start, range_start).strftime("%Y-%m-%d")


def getDayToDayReports(range: any=2):
    bms = filterScriptBms('dayTodayReport')

    bm_reports = []

    for bm_ins in bms:
        for bm_report in bm_ins['reports']:
            start = genRange(bm_report['start'],range)
            range_list = get_everyday_range(start,bm_report['end'])
            # range_list = get_everyday_range('2026-2-3','2026-2-11')
            flag = False
            header = {}
            for day_range in range_list:
                goReport(bm_ins['business_id'],bm_report['id'],day_range)

                # generate header
                if not flag:
                    flag = True
                    header = getReportHeader()

                ret = reportOneDay(day_range,bm_report['id'],header)
                if ret: bm_reports.append(ret)

    printElement(bm_reports)
    handleDayToDayReports(bm_reports,range)
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


login()
# getDayToDayReports(range='all')
getDayToDayReports(range=2)
#
# reports = [
# [{'Account Name': 'BIG_OL1_902298178897708_+7', 'Reach': 3186, 'Impressions': 3299, 'Frequency': 1.04, 'Link clicks': 102, 'CPC (cost per link click)': 0.31, 'Registrations completed': 1, 'Cost per registration completed': 31.19, 'Purchases': '—', 'Cost per purchase': '—', 'Account ID': '902298178897708', 'Amount spent': 31.19, 'memo': '', 'date': '2026-05-30', 'report_id': '1593655391872771'}] ,
# [{'Account Name': 'BIG_OL1_902298178897708_+7', 'Reach': 8361, 'Impressions': 10526, 'Frequency': 1.26, 'Link clicks': 575, 'CPC (cost per link click)': 0.32, 'Registrations completed': 21, 'Cost per registration completed': 8.73, 'Purchases': '—', 'Cost per purchase': '—', 'Account ID': '902298178897708', 'Amount spent': 183.33, 'memo': '', 'date': '2026-05-31', 'report_id': '1593655391872771'}] ,
# ]
# handleDayToDayReports(reports,'all')
print('all done')

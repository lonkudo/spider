# - coding = utf-8 -
# yepay siper auto recharge
import time

from informations.yepay import yepay
from element import *
from utils import abbrev_to_state_name,chargeSum
from driversetting import initDriver
import sys
import datetime
import pyperclip
import os
import pandas as pd

from autoReply import AutoReply


l_view,l_charge,l_decline,b_charge = False,False,False,False
l_create,l_verify,l_remove,l_memo = False,False,False,False
l_init, l_report,l_debug = False, False, False
l_log = False

from fb_report import yepay_report


g_show = True
g_sum = 0
to_chat = False
chat_name = "巴基斯坦卡台充值2个点"


p1 = sys.argv[1]

if p1 == "sum":
    chargeSum()
    sys.exit(0)
elif p1 == "off":
    driver, actions = initDriver('off')
elif p1 == "on":
    driver, actions = initDriver('on')
elif p1 == "chat":
    driver, actions = initDriver('off')
    to_chat = True
elif p1 == "debug":
    l_debug = True
else:
    print("p1 error, exit")
    sys.exit(0)

p2 = sys.argv[2]
if p2 == "view":l_view = True
elif p2 == "list":l_charge = True
elif p2 == "decline":l_decline = True
elif p2 == "create":l_create = True
elif p2 == "verify":l_verify = True
elif p2 == "charge":b_charge = True
elif p2 == "report":l_report = True
elif p2 == "remove":l_remove = True
elif p2 == "memo":l_memo = True
elif p2 == "init":l_init = True
elif p2 == "log":l_log = True
else: pass

other_params = sys.argv[3:]
text_param = ""
num_param = ""


num_params = []

for p in other_params:
    try:
        num_param = int(p)
        num_params.append(p)
    except Exception:
        text_param = p

if len(num_params) > 1:
    num_param =  num_params


LogFileName = ""
ye = yepay("cards")


def lastTask():
    with open("last_task_yepay", "r") as f:
        f.seek(0)
        content = f.read()
    return content


def cleanBuffer():
    with open("buffer.txt", "w") as f:
        f.write("")

def copyBuffer():
    with open("buffer.txt", "r") as f:
        f.seek(0)
        content = f.read()
        pyperclip.copy(content)

def printToTerminalAndBuffer(msg, end="\n"):
    if g_show:
        print(msg,end=end)
        # if don't exsit buffer.txt create it
        with open("buffer.txt", "a") as f:
            f.write(msg+end)

def login_yepay():
    goIndex()
    isHome = False

    while not isHome:
        login()
        auth()
        isHome = isHomePage()
        if isHome: showYepayBalance()
    print('start\n')


def goIndex():
    driver.get(yepay.routes.login)

def go(route):
    driver.get(route)
    time.sleep(2)

def goCards():
    go(ye.routes)
    time.sleep(5)
    selectCardStatus("正常")
    clickSearch(ye.searchFormIndex)
    time.sleep(2)

def goLogs():
    go(ye.logs)
    time.sleep(2)

def isHomePage():
    ret = findElement(driver, yepay.page.home)
    if ret:
        closeLoginNotice()
    return ret

def showYepayBalance():
    balance_xpath = '/html/body/div[1]/section/section/main/div[2]/div/div[1]/div/div/div[3]/div/div/p'
    balance_ps = findElementsByXPath(driver, balance_xpath)
    available = extractNumberInText(balance_ps[0].text)
    allocated = extractNumberInText(balance_ps[1].text)
    freezing = extractNumberInText(balance_ps[2].text)
    #
    print(f"balance: {available} + {allocated} = {(available+ allocated):.2f}")
    print(f"freeze:  {freezing}")
    Remainings.addRemainings([{"business_name": "卡台", "remaining": round((available+ allocated),2), "time": datetime.datetime.now()}])


def extractNumberInText(text):
    numReg = r'((\d+\.\d+)|\d+)'
    match = re.search(numReg,text)
    if match:
        return float(match.group())
    return 0

def extractCard(text):
    cardReg = r'(?<!\d)(\d{4})(?!\d|\.)'
    match = re.search(cardReg,text)
    if match:
        return match.group()
    elif len(text)>0:
        return "skip"
    else:
        return None

def closeLoginNotice():
    time.sleep(3)

    interact = findElementByXPath(driver, '//span[contains(.,"前往充值")]')
    if interact.is_enabled() and interact.is_displayed():
        return

    btn = findElementByXPath(driver, '//button[contains(.,"确定")]')
    if btn:
        btn.click()

def handleWarning(choice="confirm"):
    warning_dialog = findElementByXPath(driver,'//div[@role="dialog" and @aria-label="警告"]')
    if choice == "confirm":
        warning_dialog.find_element(By.XPATH,'.//button[span[text()="'+'确定'+'"]]').click()
    else:
        warning_dialog.find_element(By.XPATH,'.//button[span[text()="'+'取消'+'"]]').click()
    time.sleep(1)

def login():
    isLogin = findElement(driver,yepay.page.login)
    if isLogin:
        inputElement(driver, ".el-input__inner[type='text']", yepay.account)
        inputElement(driver, ".el-input__inner[type='password']", yepay.password)
        clickElement(driver,"button")
        time.sleep(5)
    return isLogin

def auth():
    isAuth = findElement(driver,yepay.page.auth)
    if isAuth:
        time.sleep(3)
        inputElement(driver, ".el-input__inner[type='text']", yepay.genKey())
        # inputElement(driver, ".el-input__inner[type='text']", yepay.genKey())
        clickElement(driver,"button")
        time.sleep(3)




def search(num):
    inputByPlaceholder(driver,ye.searchPlaceholder,num)
    clickSearch(ye.searchFormIndex)


def tradeStatus(status):
    clickByPlaceholder(driver,'请选择')
    time.sleep(1)
    clickText(driver,'拒付')

def isEmpty():
    element = findElement(driver,ye.empty)
    return element != False

def clickSearch(index):
    time.sleep(1)
    forms = findElements(driver,"div.el-form-item__content")
    time.sleep(1)

    button = forms[index].find_element(By.CSS_SELECTOR,"button")
    button.click()
    time.sleep(2)

def updateBalance():
    clickByTitle(driver,"更新余额",wait_time=10)

def getBalance():
    if ye.type == "cards":
        updateBalance()
    cell = findElement(driver,ye.balanceCell)
    usd = getUSD(cell)
    return usd


def getUSD(cell):
    match = re.search(r'\d+\.\d+',cell.text)
    if match:
        current_balance = float(match.group(0))
        return current_balance


def fillNum(card_info,mode="fill",show_flag=True):
    if show_flag:
        printCardBalance(card_info, ending="    ")


    if card_info['success'] == True:
        printToTerminalAndBuffer("")
        return

    current_balance = getBalance()
    # 如果 当前余额是 1或者 0 就是特殊值
    special_pre = True if current_balance == 1.0 or current_balance == 0 else False


    next_round_need_balance = None
    if mode == "fill":
        target_balance = card_info['target']
        need_balance = round(target_balance - current_balance, 2)
    elif mode == "lock":
        need_balance = round(1-current_balance, 2)
    elif mode == "fix": # mode== fix
        target_balance = card_info['target']
        need_balance = round(target_balance, 2)
        if special_pre :  # 如果卡片余额是 1， 那么要充值的钱-1
            need_balance = round(target_balance - 1, 2)
    else:
        need_balance = 0 # 占位用 防止pycharm报错


    pre_need = need_balance

    # 如果需要的余额小于10美元 则充值10美元 下一轮 提走
    if need_balance < 10 and need_balance > 0:
        next_round_need_balance = need_balance - 10
        need_balance = 10

    if need_balance == 0:
        card_info['success'] = True
        printToTerminalAndBuffer("")
        return
    else:
        if ye.type == 'cards':
            handleCard(need_balance)
        else:
            handleKaduan()


    amount = abs(need_balance)
    submitAmount(amount)

    ret = isSuccess()

    post_balance = getBalance()

    if next_round_need_balance:
        card_info['target'] = next_round_need_balance
        card_info['success'] = False
        post_balance = fillNum(card_info,"fix",False)  # 递归时不展示初始余额

    special_post = True if post_balance == 1.0 else False

    if show_flag: # 在need_balance 变化前展示
        sign = ''
        if  need_balance > 0:
            sign = "+"

        preNum = pre_need
        postNum = post_balance

        if special_pre:
            preNum = shiftAmount(preNum)
        if special_post:
            preNum = shiftAmount(preNum)
            postNum -= 1

        printToTerminalAndBuffer(f"{sign}{preNum} ", end=" ")
        printToTerminalAndBuffer(f"= {postNum:<5}")


    card_info['success'] = ret
    return post_balance

def shiftAmount(amount,shift_abs = 1):
    if amount < 0:
        return amount - shift_abs
    else:
        return amount + shift_abs


def handleCard(need_balance):
    # 点击操作
    clickOperator(1)

    menu_items = getDropdown()

    if need_balance < 0:
        menu_items[1].click()
    else:
        menu_items[0].click()
    # 充值 提现 锁卡
    time.sleep(1)

def handleKaduan():
    # 点击提现
    clickOperator(1)
    time.sleep(1)
    check()
    # 因为勾选以后会出现popover导致无法点击提交 所以点击其他位置让这个遮挡物消失
    actions.move_by_offset(50, 50).click().perform()
    time.sleep(1)

def clickClose():
    elements = findElement(driver,".el-icon.el-dialog__close")
    element = findElement(driver,".el-dialog__headerbtn[@aria-label=\"close\"]")

def isSuccess():
    try:
        amount_input = findInputByPlaceholder(driver,"金额")
        footers = findElements(driver, "div.dialog-footer")
        clickButtonInGroup(footers[ye.submitFooterIndex], 0)
        return False
    except Exception as e:
        return True

def check():
    checkboxContainer = findElement(driver,"服务条款")
    label = checkboxContainer.find_element(By.CSS_SELECTOR,"label")
    label.click()
    time.sleep(1)

def submitAmount(amount):
    # 充值或提现窗口 输入金额
    inputByPlaceholder(driver,"金额",amount)
    footers = findElements(driver,"div.dialog-footer")
    clickButtonInGroup(footers[ye.submitFooterIndex],1)

def void(*args, **kwargs):
    pass

def walkList(data,goFunc = void,pretaskFunc = void, taskFunc = void):
    goFunc()
    pretaskFunc()
    for info in sorted(data,key=lambda x: x['num']):
        if isIgnore(info,'allocate'): continue
        search(info['num'])
        taskFunc(info)
    printToTerminalAndBuffer('')

def totalRecordCount():
    total =  findElementByXPath(driver,'//span[contains(@class, "el-pagination__total")]')
    return int(total.text.split(' ')[1])

def getRecordsCount():
    record_count = totalRecordCount()
    if not record_count: return 0,0

    reasons_map = ["This card has no available t...",
                   "No sufficient funds"]

    trs = findElementsByXPath(driver,"//table[@class='el-table__body']/tbody/tr")
    no_money_count = record_count
    for tr in trs:
        text_div = tr.find_element(By.XPATH, './td[14]/div')
        if text_div.text not in reasons_map:
            no_money_count -= 1

    return record_count, no_money_count

def printCardBalance(info,ending="\n"):
    name = None
    try:
        name = info['name']
    except Exception:
        pass

    record_count = totalRecordCount()

    if record_count:
        current_balance = getBalance()
    else:
        current_balance = 0

    if current_balance == 1.0: # 如果当前卡余额为1，打印为0
        current_balance = 0

    if name:
        printToTerminalAndBuffer(f"{name:<30}{info['num']} {current_balance:<7}", end=ending)
    else:
        printToTerminalAndBuffer(f"{info['num']} {current_balance:<7}", end=ending)

    return current_balance


def sumCardBalance(info,ending="\n"):
    name = None
    try:
        name = info['name']
    except Exception:
        pass

    record_count = totalRecordCount()

    if record_count:
        current_balance = getBalance()
    else:
        current_balance = 0

    if current_balance == 1.0: # 如果当前卡余额为1，打印为0
        current_balance = 0

    if name:
        printToTerminalAndBuffer(f"{name:<30}{info['num']} {current_balance:<7}", end=ending)
    else:
        printToTerminalAndBuffer(f"{info['num']} {current_balance:<7}", end=ending)

    global g_sum
    g_sum += current_balance
    return current_balance

def printCardDeclines(info):
    total_count,no_money_count = getRecordsCount()
    printToTerminalAndBuffer(info['num'], end=" ")
    printToTerminalAndBuffer(f"{total_count:<16}{no_money_count:<5}")

def timeHeader():
    printToTerminalAndBuffer("TIME: " + datetime.datetime.now().strftime("%m-%d %H:%M"))
    printToTerminalAndBuffer("Card Balance")

def declineHeader():
    # print yesterday date
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    printToTerminalAndBuffer("TIME: " + yesterday.strftime("%m-%d"))
    printToTerminalAndBuffer("Card Declines (Insufficient balance)")

def selectTradeStatus(status):
    forms = findElements(driver,"div.el-form-item__content")
    forms[2].click()
    time.sleep(1)
    li = findElementByXPath(driver,f'//li[@class="el-select-dropdown__item" and normalize-space(text())="{status}"]')
    time.sleep(1)
    li.click()
    scrollupDorpdown()

def scrollupDorpdown():
    spans = findElementsByXPath(driver,'//span[@class="el-breadcrumb__inner" and @role="link"]')
    spans[-1].click()
    time.sleep(1)

def declinePretask():
    declineHeader()
    selectTradeStatus('拒付')
    selectTradeTime('昨天')

def selectTradeTime(range):
    forms = findElements(driver,"div.el-form-item__content")
    forms[0].click()
    time.sleep(1)
    button = findElementByXPath(driver,f'//div[contains(@visible, "true")]//button[@class="el-picker-panel__shortcut" and normalize-space(text())="{range}"]')
    button.click()
    time.sleep(1)

def readOneInfo(processInfo=void):
    # read one line of charge record
    f = open("card.txt", "r" )
    line = f.readline()
    f.close()

    if len(line) > 3:
        ret = processInfo(line)
    elif len(line)>0:
        ret = "skip"
    else:
        ret = None
    return ret


def getRecord(record):
    # match record like "1234 +100" or "1234 -50"
    match = re.match(r'(\d{4})\s{0,}([+|-])\s{0,}((\d+\.\d+)|\d+)',record)
    if match:
        card = match.group(1)
        operation = match.group(2)
        amount = float(match.group(3))
        if operation == '-':
            amount = -amount
        return {'num':card, 'target': amount,'success': False}
    else:
        # match record like "1234 +"
        match = re.match(r'(\d{4})\s{0,}([+|-])', record)
        if match:
            card = match.group(1)
            operation = match.group(2)
            search(card)
            if operation == '-':
                amount = getBalance()
                writeTempMsg(str(amount))
                if amount != 1:
                    writeCharge(f"{card} -{amount-1}\n")
            else:
                amount = float(readTempMsg())
                writeCharge(f"{card} +{amount}\n")
            return "skip"
    if len(record)>2: # match messages
        return "skip"
    return None


def getCardInRecord(record):
    # match record like "1234 +100" or "1234 -50"
    match = re.match(r'(\d{4})\s{0,}([+|-])\s{0,}((\d+\.\d+)|\d+)',record)
    if match:
        card = match.group(1)
        operation = match.group(2)
        amount = float(match.group(3))
        if operation == '-':
            amount = -amount
        return {'num':card, 'target': amount,'success': False}
    else:
        # match record like "1234 +"
        match = re.match(r'(\d{4})\s{0,}([+|-])', record)
        if match:
            card = match.group(1)
            return {'num':card, 'target': 0,'success': False}
    if len(record)>2: # match messages
        return "skip"
    return None




def writeTempMsg(msg):
    with open("temp.txt", "w") as f:
        f.write(msg)

def readTempMsg():
    with open("temp.txt", "r") as f:
        msg = f.read()
    return msg

def addNumberInBuffer():
    numReg = r'(\d{4})\s+((\d+\.\d+)|\d+)'
    count = 0
    total = 0
    with open("buffer.txt", "r") as f:
        while True:
            line = f.readline()
            if not line: break
            match = re.match(numReg, line)
            if match:
                num = match.group(2)
                count += 1
                total += float(num)

    if count > 0:
        total = int(total)
        printToTerminalAndBuffer(f"Total:{total},Card Count:{count}")

def listCard(handleInfo=void,processInfo=void):
    go(ye.routes)
    while True:
        info = readOneInfo(processInfo)
        if not info: break # 没有数据了退出循环
        if info =="skip": # 6888 - 这种直接 退出循环
            removeOneInfo()
            continue
        ret = handleInfo(info)
        if ret:
            removeOneInfo()


def chargeHandler(info):
    search(info['num'])
    pre = getBalance()
    post = fillNum(info, mode="fix")
    if pre != post:
        return True



def removeOneInfo():
    f = open("card.txt", "r+" )
    # remove fist line
    lines = f.readlines()
    f.seek(0)
    f.truncate()
    f.writelines(lines[1:])
    f.close()

def writeCharge(info):
    with open("card.txt", "a+") as f:
        # Move to the beginning of the file to check the last character
        f.seek(0, 2)  # Move to the end of the file
        if f.tell() > 0:  # Only check if the file is not empty
            f.seek(f.tell() - 1, 0)  # Move to the last character
            last_char = f.read(1)
            if last_char != "\n":
                f.write("\n")  # Add a newline if the last character is not a newline

        # Write the new content, ensuring it starts with no newline
        f.write(info)


def checkBalance(infos):
    walkList(infos,goFunc=goCards,pretaskFunc=timeHeader,taskFunc=printCardBalance)

def CalcBalance(infos):
    walkList(infos,goFunc=goCards,pretaskFunc=void,taskFunc=sumCardBalance)

def listDecline(infos):
    walkList(infos,goFunc=goLogs,pretaskFunc=declinePretask,taskFunc=printCardDeclines)


def allocate():
    goCards()
    for info in sorted(ye.infos,key=lambda x: x['target']):
        if isIgnore(info,'allocate'): continue
        search(info['num'])
        fillNum(info)

def retrive(ye):
    time.sleep(1)
    go(ye.routes)
    button = findElementByXPath(driver,"/html/body/div[1]/section/section/main/div[2]/div/div[1]/form/div[1]/div/button")
    button.click()
    confirm = findElementByXPath(driver,"//div/div/div[3]/button[2]")
    confirm.click()
    time.sleep(1)

def deleteCard():
    go(ye.routes)
    selectCardStatus("已锁定")
    clickSearch(ye.searchFormIndex)
    while True:
        try:
            handleDelete()
        except Exception as e:
            printToTerminalAndBuffer('done')

def getDropdown():
    # 登录登出这个dropdown 和锁卡的dropdown 有两个
    dropdowns = findElements(driver,"div.el-scrollbar__wrap.el-scrollbar__wrap--hidden-default > ul > ul")
    # printToTerminalAndBuffer(dropdown.get_attribute("outerHTML")) 通过打印出结构发现不是自己要的那个dropdown
    menu_items = dropdowns[1].find_elements(By.CSS_SELECTOR, 'div.el-dropdown-menu__item')
    return menu_items

def lockCard():
    go(ye.routes)
    for info in ye.infos:
        if isIgnore(info): continue
        search(info['num'])
        if isEmpty(): continue
        if checkStatus(wantedStatus="正常"):
            fillNum(info,'lock')
            time.sleep(2)
            handleLock()

        printToTerminalAndBuffer(info['num'],'done')

def isIgnore(info,mode="lock"):
    if mode == "lock":
        isIgnore = info['num'] == None or info['option'] == True
        if isIgnore:
            printToTerminalAndBuffer(f"{info['num']} {info['name']} ignore")
        return isIgnore
    elif mode == "allocate":
        isIgnore = info['num'] == None or info['option'] == False
        if isIgnore:
            printToTerminalAndBuffer(f"{info['num']} {info['name']} ignore")
        return isIgnore


def handleDelete():
    updateBalance()
    clickOperator(1)
    clickDropdownItem(2)
    handleWarning("confirm")
    verifyDepositPwd()
    time.sleep(5)

def clickOperator(index):
    cell = findElement(driver,ye.operatorCell)
    clickButtonInGroup(cell,index)

def clickFirstOperator(index):
    cells = findElements(driver,ye.operatorCell)
    cell = cells[0]
    clickButtonInGroup(cell,index)


def clickDropdownItem(index):
    menu_items = getDropdown()
    menu_items[index].click()
    time.sleep(1)

def messageBoxClick(index):
    message_btns = findElement(driver, "div.el-message-box__btns")
    buttons = message_btns.find_elements(By.CSS_SELECTOR, 'button')
    buttons[index].click()

def handleLock():
    clickOperator(1)
    clickDropdownItem(2)
    handleWarning("confirm")
    verifyDepositPwd()
    time.sleep(1)

def clickVerifyButton():
    button = findElementByXPath(driver,"//button[span[text()='验证']]")
    button.click()
    time.sleep(1)

def verifyDepositPwd():
    inputByPlaceholder(driver,"请输入资金密码", ye.password)
    footers = findElements(driver, "div.dialog-footer")
    clickVerifyButton()

def selectCardStatus(state):
    if state == "无状态":
        clear_status = findElementByXPath(driver,'//label[contains(normalize-space(.), "卡状态")]/following::i[@class="el-icon el-select__caret el-input__icon"][1]')
        clear_status.click()
        return

    status_select = findElementByXPath(driver,'//div[preceding-sibling::label[contains(normalize-space(.), "卡状态")] and @class="el-form-item__content"]')
    status_select.click()
    time.sleep(2)
    selectDropdownItem(state)

def selectDropdownItem(text):
    status_select = findElementByXPath(driver,f'//li[contains(normalize-space(.), "{text}")]')
    status_select.click()


def checkStatus(wantedStatus):
    cell = findElement(driver,ye.statusCell)
    if cell.text == wantedStatus:
        return True
    else:
        return cell.text

def getStatus():
    cell = findElement(driver,ye.statusCell)
    return cell.text

def go_card_spider():
    login_yepay()
    go(ye.routes)


def create_card():
    create_card_button = findElementByXPath(driver,'//button[span[text()="开卡"]]')
    create_card_button.click()
    time.sleep(3)

    # 等到title出来就可以输入
    dialog_title = findElementByXPath(driver,'//span[@class="el-dialog__title" and text()="开卡"]')
    inputByPlaceholder(driver,"开卡金额",10)

    # 选择卡段
    time.sleep(2)
    # kaduan_option = findElementByXPath(driver,'//div[label[span[text()="40041606*(广告-FB-美区)"]]]')
    kaduan_option = findElementByXPath(driver,'//label[span[text()="54493747*免跨境"]]')
    kaduan_option.click()
    time.sleep(1)

    # 等到title出来就可以输入
    ads_option = findElementByXPath(driver,'//span[span[text()="广告业务"]]')
    ads_option.click()


    time.sleep(2)

def close_create_card():
    dialogHandle("开卡","提交")
    time.sleep(5)


def dialogHandle(title,option):

    dialog_title = findElementByXPath(driver,f'//span[@class="el-dialog__title" and text()="{title}"]')
    dialog_div = findElementByXPath(driver,f'//div[@aria-label="{title}"]') # 这个dialog的div

    submit_button = dialog_div.find_element(By.XPATH,f'.//button[span[text()="{option}"]]')
    submit_button.click()

def open_card_info():
    clickFirstOperator(0)
    verifyDepositPwd()

def get_card_info():
    # 等到title出来就可以读取
    dialog_title = findElementByXPath(driver,'//span[@class="el-dialog__title" and text()="卡片信息"]')
    dialog_div = findElementByXPath(driver,'//div[@aria-label="卡片信息"]') # 这个dialog的div
    form_items = dialog_div.find_elements(By.XPATH,".//form/div/div") # 找到

    card_num_index = 1
    cvv_index = 4
    expire_date_index = 6

    card_num = form_items[card_num_index].text
    cvv = form_items[cvv_index].text
    expire_date = form_items[expire_date_index].text

    table = dialog_div.find_element(By.XPATH,".//table[@class='el-table__body']")
    tds = table.find_elements(By.XPATH,".//td")
    first_name = tds[0].text
    last_name = tds[1].text
    state = abbrev_to_state_name(tds[3].text)
    town = tds[4].text
    address = tds[5].text
    zipcode = tds[7].text

    name = first_name + ' ' + last_name
    shop_name = first_name + ' ' + 'SHOP'

    return {'card_num': card_num, 'expire_date': expire_date, 'cvv': cvv, 'name': name, 'state': state, 'town': town,
            'address': address, 'zipcode': zipcode, 'shop_name': shop_name, 'last_four': card_num[-4:]}


def create_one_card():
    create_card()
    time.sleep(3)

def get_one_card_info():
    open_card_info()
    info = get_card_info()
    return info

def input_memo(msg):
    xpath = '//textarea[../../preceding-sibling::label[contains(normalize-space(.), "备注")]]'

    textarea = findElementByXPath(driver, xpath)
    textarea.click()
    textarea.clear()
    textarea.send_keys(msg)

    time.sleep(1)

def save_card_info():
    save_button = findElementByXPath(driver,'//button[contains(.,"保存")]')
    save_button.click()
    time.sleep(5)


def close_card_info():
    close_card_info_btn = findElementByXPath(driver,'//button[preceding-sibling::*[text()="卡片信息"]]')
    close_card_info_btn.click()
    time.sleep(5)


def report_spider():
    print(1)
    goReport()
    print(2)
    readData()

def goReport():
    report_url = "https://qlobalyepay.com/#/report"
    go(report_url)
    time.sleep(2)

def readData():
    # arrange header
    header_keys = []

    headers = findElementsByXPath(driver,'//thead/tr/th')
    for header in headers:
        header_keys.append(header.text)

    table = findElementByXPath(driver,'//table[@class="el-table__body"]/tbody')
    rows = table.find_elements(By.XPATH,".//tr")
    # yesterday row at index 1

    data = []
    for row in rows:
        tds = row.find_elements(By.XPATH, ".//td")

        data_row = {}
        for idx, td in enumerate(tds):
            data_row[header_keys[idx]] = td.text

        data.append(data_row)

    # handle data
    std_data = []
    for item in data:
        std_data.append(splitPair(item))

    for item in std_data:
        print(item)


    # 日期 | 货币 | 充值金额 / 笔数 | 服务费 | 上级划拨 | 提现金额 / 笔数 | 开卡费 | 卡充值手续费 | 跨境手续费 / 笔数 | 取消授权费 / 笔数 | 退款手续费 | 完成金额 /笔数 | 授权金额/占比
    #  0      1          2           3        4           5           6         7                8                9             10           11             12
    # 撤销金额/占比 | 退款金额/占比 | 拒付金额/占比 | 手动扣除金额/笔数 | 授权成功率/笔数 | 撤销笔数/撤销率 | 退款笔数/退款率 | 拒付笔数/拒付率
    #      13            14             15              16             17              18             19              20

    # 日期 | 充值金额 / 笔数 | 服务费 | 取消授权费 / 笔数 | 完成金额 /笔数 | 授权金额/占比 | 撤销金额/占比 | 拒付金额/占比 | 授权成功率/笔数 | 撤销笔数/撤销率 | 拒付笔数/拒付率

    # text = safeTD(td.text)

    yepay_report(std_data)

    time.sleep(200)

def splitPair(pairs):
    # input a pair like {'完成金额\n笔数': '406.8\n51'} {'跨境手续费 / 笔数': '0.00 / 0'}
    # then split it
    newPairs = {}

    for key, value in pairs.items():
        key = key.replace(" / ", "\n")
        value = value.replace(" / ", "\n")

        keys = key.split("\n")
        values = value.split("\n")

        if len(keys) == 1:
            newPairs[keys[0]] = values[0]
        else:
            newPairs[keys[0]] = values[0]
            if keys[0].endswith("笔数"):
                newPairs[keys[1]] = values[1]
            elif keys[0].endswith("金额"):
                newPairs[keys[0][:-2]+keys[1]] = values[1]
            else:
                newPairs[keys[0]+keys[1]] = values[1]

    print(newPairs)

    wanted_keys = ["日期","充值金额","充值笔数","服务费","跨境手续费","跨境手续费笔数","取消授权费","取消授权费笔数","授权金额","撤销金额","退款金额","撤销笔数","退款笔数","拒付笔数",]
    newPairs = {k: v for k, v in newPairs.items() if k in wanted_keys}

    return newPairs


def safeTD(text):
    items = text.split()
    cleaned_items = [item for item in items if item != ""]

    return "/".join(cleaned_items).replace("///","/")

def printAndCopyCardInfo(info):
    """ print card info to terminal and copy to clipboard """
    # {'card_num': '5449374768360478', 'expire_date': '10/28', 'cvv': '265', 'name': 'Martinez Babbage', 'state': 'Georgia', 'town': 'Porterdale', 'address': '1195 Newton Plaza shire', 'zipcode': '11806', 'shop_name': 'Martinez SHOP'}
    # convert to string
    info_str = (f"Card Number:   {info['card_num']}\n"
                f"Last Four:   {info['last_four']}\n"
                f"Expiration Date:   {info['expire_date']}\n"
                f"CVV:   {info['cvv']}\n"
                f"Name:   {info['name']}\n"
                f"Shop Name:   {info['shop_name']}\n"
                f"Street:   {info['address']}\n"
                f"Town:   {info['town']}\n"
                f"State:   {info['state']}\n"
                f"Zipcode:   {info['zipcode']}\n")
    printToTerminalAndBuffer(info_str)
    # copy to clipboard
    pyperclip.copy(info_str)

def createOneCardAndGetInfo(msg):
    global g_show
    goCards()
    create_one_card()
    input_memo(msg)
    close_create_card()
    time.sleep(10)
    goCards()
    open_card_info()
    info = get_card_info()
    close_card_info()
    printAndCopyCardInfo(info)
    g_show = False
    removeCardBalance(info['last_four'])
    return info

def memoCard(num,msg):
    goCards()
    search(num)
    open_card_info()
    input_memo(msg)
    save_card_info()

def initCard(num,msg):
    global g_show
    goCards()
    g_show = False
    removeCardBalance(num)
    g_show = True
    open_card_info()
    input_memo(msg)
    info = get_card_info()
    printAndCopyCardInfo(info)
    save_card_info()
    return info





def removeCardBalance(num):
    writeCharge(f"{num} -\n")
    listCard(handleInfo=chargeHandler, processInfo=getRecord)


def readVerificationCodeFromPage():

    rows_xpath = "/html/body/div[1]/section/section/main/div[2]/div/div/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr"
    rows = findElementsByXPath(driver, rows_xpath)
    time_xpath = ".//td[9]"
    msg_xpath = ".//td[10]"

    verify_codes = []

    for row in rows:
        time = row.find_element(By.XPATH, time_xpath).text
        msg = row.find_element(By.XPATH, msg_xpath).text
        match = re.match(r'METAPAY\*((\w|\d){4})', msg)
        if match:
            code = match.group(1)
            verify_codes.append(f"Time: {time}, Code: {code}")

        match = re.match(r'FACEBK \*((\w|\d){4})', msg)
        if match:
            code = match.group(1)
            verify_codes.append(f"Time: {time}, Code: {code}")


    verification_msg = ""
    if len(verify_codes) == 0:
        verification_msg += "No Code"

    for code in verify_codes:
        verification_msg += code + "\n"

    printToTerminalAndBuffer(verification_msg)
    return verification_msg

def getVerificationCode(num):
    goLogs()
    search(num)
    printToTerminalAndBuffer(f"Card: {num:04d}")
    verification_msg = readVerificationCodeFromPage()
    pyperclip.copy(f"Card: {num:04d}\n" + verification_msg)

def removeCard(num):
    goCards()
    search(num)
    handleLock()
    selectCardStatus("已锁定")
    search(num)
    handleDelete()

def removeOneCard(num):
    search(num)
    ret = getStatus()
    if ret == "已删除":
        print(f"{num} deleted")
        return ret
    elif ret == "正常":
        handleLock()
    handleDelete()
    ret = getStatus()
    if ret == "已删除":
        print(f"{num} deleted")
    time.sleep(2)
    return ret


def listRemoveCard():
    goCards()
    selectCardStatus("无状态")
    listCard(handleInfo=removeOneCard,processInfo=extractCard)

def listChargeCard():
    goCards()
    listCard(handleInfo=chargeHandler, processInfo=getRecord)


def append_client_with_new_num(new_num,business_name):
    """ append to yepay_clients.py """
    # Convert new_num to string (in case it's provided as an integer)
    new_num = str(new_num)

    # Path to the yepay_clients.py file
    file_path = r'./informations/yepay_clients.py'

    try:
        # Open the file and read the content
        with open(file_path, 'r') as f:
            content = f.read()

        # Define the pattern to search for in the content (just before the closing bracket of the last client)
        pattern = "False},\n]"

        # Find the index of the first occurrence of the pattern in the file
        insert_position = content.find(pattern)
        insert_position += len(pattern)-1

        if insert_position == -1:
            print(f"Pattern '{pattern}' not found. Unable to append new record.")
            return

        # Define the new record to append (as a string)
        new_record = f"    {{'target': 50, 'num': '{new_num}', 'option': True, 'success': False, 'records': [], 'business_name': '{business_name}','cleared': False}},\n"

        # Insert the new record at the position found
        new_content = content[:insert_position] + new_record + content[insert_position:]

        # Write the modified content back to the file
        with open(file_path, 'w') as f:
            f.write(new_content)

        print(f"New record with num {new_num} appended successfully.")

    except Exception as e:
        print(f"Error: {e}")

def oneCardInList(num):
    obj = {'target': 50, 'num': num, 'option': True, 'success': False, 'records': [], 'cleared': False}
    return [obj]

def is_ambiguous_match(a, b, max_diff=1):
    if len(a) != len(b):
        return False
    diff = sum(x != y for x, y in zip(a, b))
    if diff == 0: return 0
    elif diff == 1: return 1
    else: return -1

class CardError(Exception):
    pass

def checkCard(num):
    diff_0 = []
    diff_1 = []
    infos = ye.check_infos
    infos.extend(ye.infos)
    for info in infos:
        ret = is_ambiguous_match(num,info['num'])
        if ret == 0:
            diff_0.append(info['num'])
        elif ret == 1:
            diff_1.append(info['num'])
        else:
            pass

    if len(diff_0) > 0:
        pass
    elif len(diff_1) > 0:
        raise CardError(f"Card Number Error: {num}, Possible Cards: {' '.join(diff_1)}")
    else:
        raise CardError(f"Card Number Error: {num}")

def checkCards():
    error_msg = []

    with open("card.txt", "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            info = getCardInRecord(line)
            if info == "skip":
                continue

            try:
                checkCard(info['num'])
            except CardError as e:
                error_msg.append(str(e))  # store message, not exception

    if error_msg:
        printToTerminalAndBuffer("\n".join(error_msg))
        copyBuffer()
        print("fail")
        exit(1)

    print("all good")

def getOnlineDf(range="昨天"):
    goLogs()
    changeLogCondition(range)
    downloadLog()
    df = readLog()
    return df

def getOfflineDf():
    df = readLog()
    return df

def log_spider():
    df = getOnlineDf()
    filtered_df = dfFilterCards(df,ye.check_infos)
    filtered = dfFilterStatus(filtered_df,["PENDING","DECLINED"])

    writeDf(filtered)

def getOneBusinessSpent(business_name):
    cards = getBussinessCards(business_name)
    df = getOfflineDf()
    filtered_df = dfFilterCards(df,cards)
    filtered_pending = dfFilterStatus(filtered_df,["PENDING"])

    filtered_reversed = dfFilterStatus(filtered_df,["REVERSED"])

    info_pending = getDfInfo(filtered_pending)


    info_reversed = getDfInfo(filtered_reversed)
    print("in")

    spent = info_pending['total'] - info_reversed['total']
    print(spent)








def logOneCard(card="0000"):
    # df = getOnlineDf("最近三天")
    df = getOfflineDf()
    filtered_df = dfFilterCards(df,oneCardInList(card))
    print(filtered_df)
    filtered = dfFilterStatus(filtered_df,["PENDING"])

    writeDf(filtered)

def getBussinessCards(business_name=None):
    infos = ye.check_infos
    infos.extend(ye.infos)
    if business_name is None: return infos
    return [info for info in infos if info['business_name'] == business_name]

def getRunningBussiness():
    cards = getBussinessCards()
    business_names = set()
    for card in cards:
        business_names.add(card['business_name'])
    return business_names


def hdfDeclines():
    goLogs()
    changeLogCondition("昨天")
    downloadLog()
    df = readLog()
    filtered_df = dfFilterCards(df,ye.check_infos)
    filtered = dfFilterStatus(filtered_df,["DECLINED"])

    info = getDfInfo(filtered)

    printToTerminalAndBuffer(f"{info['count']} - 10 = {info['count']-10}")
    printToTerminalAndBuffer(f"{info['total']}")
    writeDf(filtered)
    # removeLogFile()

def writeDf(df,name="Log"):
    # write df to excel

    output_folder = "statistics"
    filename = f"{name}.xlsx"
    output_path = os.path.join(output_folder, filename)

    os.makedirs(output_folder, exist_ok=True)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df.to_excel(
            writer,
            sheet_name="REPORT",  # ✅ always specify
            index=False,
            startcol=0  # ✅ correct param
        )


def changeLogCondition(time_range="最近三天" ):
    # time_range options
    # 今天 昨天 本月 最近三天 最近一周 最近一个月 最近三个月 最近六个月
    selectTradeTime(time_range)

def downloadLog():
    # click export button
    export_button = findElementByXPath(driver,'//button[span[text()="导出文件"]]')
    export_button.click()
    time.sleep(10)
    # click confirm button in dialog

def readLog():
    folder = r"C:\Users\ASUS\Downloads"

    # find newest xlsx (ignore temp files)
    xlsx_files = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.endswith(".xlsx") and not f.startswith("~$")
    ]

    if not xlsx_files:
        print("No xlsx files found")
        return []

    newest_file = max(xlsx_files, key=os.path.getmtime)

    global LogFileName
    LogFileName = newest_file
    # read excel to get sheet names
    xl = pd.ExcelFile(newest_file, engine="openpyxl")

    # find matching sheet (ignore appendix / extra text)
    target_sheet = None
    for sheet in xl.sheet_names:
        if sheet != "Sheet1":
            target_sheet = sheet

    #  use WITH to auto-close file
    with pd.ExcelFile(newest_file, engine="openpyxl") as xl:

        # get first sheet that is not Sheet1
        target_sheet = next(
            (s for s in xl.sheet_names if s != "Sheet1"),
            xl.sheet_names[0]   # fallback
        )

        df = pd.read_excel(xl, sheet_name=target_sheet, header=None)


    df = df.dropna(how='all')

    df.columns = [
        '流水号','卡序列号','卡号','类型','交易状态','授权码',
        '交易金额','货币类型','交易时间','商户信息','商户金额',
        '商户币种','商户国家','描述信息'
    ]
    return df

def removeLogFile():
    if os.path.exists(LogFileName):
        os.remove(LogFileName)

def dfFilterCards(df, infos):
    cards = [str(info['num']) for info in infos]   # convert to string
    suffixes = tuple(cards)

    col = df['卡号'].astype(str)
    filtered_df = df[col.str[-4:].isin(suffixes)]

    return filtered_df

def dfFilterStatus(df,status=["PENDING","REVERSED","DECLINED"]):

    if status == "All":
        filtered_df = df
    else:
        filtered_df = df[df['交易状态'].isin(status)]

    return filtered_df

def getDfInfo(df):
    info = {}
    info['count'] = len(df)
    info['total'] = round(df['交易金额'].sum(),2)
    return info

def statusBusiness():
    # df = getOnlineDf("昨天")
    df = getOfflineDf()
    bms = [{'business_name': 'ALL'},{'business_name': 'hdf'}]
    for bm in bms:
        business_cards = getBussinessCards(bm['business_name'])
        filtered_df = dfFilterCards(df,business_cards)
        filtered_pending = dfFilterStatus(filtered_df,["PENDING",])
        info_pending = getDfInfo(filtered_pending)
        filtered_reversed = dfFilterStatus(filtered_df,["REVERSED",])
        info_reversed = getDfInfo(filtered_reversed)

        printToTerminalAndBuffer(f"{bm['business_name']} - Count: {info_pending['count'] - info_reversed['count']}, Total: {info_pending['total']-info_reversed['total']}")

def getRemainingBalanceOfBusiness():
    bms = [{'business_name': 'ALL'},{'business_name': 'hdf'}]
    global g_sum
    remainings = []
    for bm in bms:
        cards = getBussinessCards(bm['business_name'])
        CalcBalance(cards)
        Remainings.addRemainings([{"business_name":bm['business_name'], "remaining": round(g_sum,2), "time":datetime.datetime.now()}])
        g_sum = 0


    Remainings.writeRemainings()
    return remainings

def retriveRemainingCredit():
    names = getRunningBussiness()
    credits = []

    for name in names:
        info =  retriveOneCredit(name)
        if info: credits.append(info)

    writeCredits(credits)


def getBusinessSpent():
    names = getRunningBussiness()
    getOnlineDf("昨天")

    for name in names:
        info =  getOneBusinessSpent(name)



def writeCredits(credits):
    output_folder = "statistics"
    filename = f"Charge.xlsx"
    output_path = os.path.join(output_folder, filename)

    os.makedirs(output_folder, exist_ok=True)
    print(credits)

    df = pd.DataFrame(credits)


    df.rename(columns={
        "business_name": "账户",
        "credit": "剩余额度",
        "time": "更新时间",
    }, inplace=True)

    with pd.ExcelWriter(output_path, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
        df.to_excel(
            writer,
            sheet_name="Sheet1",  # ✅ always specify
            index=False,
            startcol=10,
        )


def retriveOneCredit(file):
    folder = "./statistics"
    filename = f"{folder}/{file}.xlsx"
    if not os.path.exists(filename): return None
    df = pd.read_excel(filename, sheet_name="REPORT")
    deposit = df.iloc[0,10]
    remaining = df.iloc[0,9]
    time = df.iloc[2,10]
    return {"business_name": file, "credit": round((float(deposit)+float(remaining)),2) ,"time": time, }





def readBussinessCreditFromFile():
    pass




class Remainings:
    remainings = []

    @classmethod
    def writeRemainings(cls):
        output_folder = "statistics"
        filename = f"Charge.xlsx"
        output_path = os.path.join(output_folder, filename)

        os.makedirs(output_folder, exist_ok=True)

        df = pd.DataFrame(cls.remainings)

        df["time"] = df["time"].dt.strftime("%m-%d %H:%M")

        df.rename(columns={
            "business_name": "账户",
            "remaining": "卡台剩余",
            "time": "更新时间",
        }, inplace=True)


        with pd.ExcelWriter(output_path, engine="openpyxl",mode="a",if_sheet_exists="overlay") as writer:
            df.to_excel(
                writer,
                sheet_name="Sheet1",  # ✅ always specify
                index=False,
                startcol=7,
            )

    @classmethod
    def addRemainings(cls,remainings):
        cls.remainings.extend(remainings)
        print(cls.remainings)



if __name__ == "__main__":
    cleanBuffer()
    if not l_debug:
        checkCards()
        login_yepay()
    if l_view:
        if not text_param and not num_param:
            checkBalance(ye.check_infos)
        if text_param == "info":
            checkBalance(ye.infos)
        if isinstance(num_param, int):
            info = {'num': num_param,'option': True}
            checkBalance([info,])
        if isinstance(num_param, list):
            infos = [{'num': key,'option': True} for key in num_param]
            checkBalance(infos)

        addNumberInBuffer()
    if l_charge:
        listChargeCard()
    if l_decline:
        ye.searchFormIndex = 8
        listDecline(ye.check_infos)
        addNumberInBuffer()
    if b_charge:
        allocate()
    if l_create:
        info = createOneCardAndGetInfo(text_param)
        num = info['last_four']
        append_client_with_new_num(num,text_param)
    if l_verify:
        ye.searchFormIndex = 8
        getVerificationCode(num_param)
    if l_remove:
        if num_param == "list":
            listRemoveCard()
        else:
            removeCard(num_param)
    if l_memo:
        memoCard(num_param,text_param)
    if l_init:
        initCard(num_param,text_param)

    if l_report:
        report_spider()

    if l_log:
        # hdfDeclines()
        # if num_param:
        #     logOneCard(num_param)
        # else:
        #     log_spider()
        # statusBusiness()
        # remainingBalanceOfBusiness()
        # Remainings.writeRemainings()
        # getBusinessSpent()
        if text_param == "credit":
            retriveRemainingCredit()
        elif text_param == "remaining":
            getRemainingBalanceOfBusiness()
        elif text_param == "decline":
            hdfDeclines()

        if num_param:
            logOneCard(num_param)




    copyBuffer()
    if to_chat:
        pass
        autoReply_instance = AutoReply()
        autoReply_instance.giveHint()
        # autoReply_instance.pasteToChat(chat_name)

    print('\nall done')
    if not l_debug:
        driver.quit()


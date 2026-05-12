import re

from element import printElement
from utils import parse_safe_number

def changeInfo(infos):
    newInfos = []

    for index,info in enumerate(infos):
        new_info = {}
        new_info['target'] = getTargetNumber(parse_safe_number(info['threshold']),parse_safe_number(info['spending_limit']),getOption(info['status'],info['card']))
        new_info['num'] = getCard(info['card'])
        new_info['name'] = info['name']
        new_info['option'] = getOption(info['status'],info['card'])
        new_info['cleared'] = False
        new_info['spending_limit'] = parse_safe_number(info['spending_limit'])
        new_info['id'] = getID(info['id'])
        # new_info['currency'] = info['currency']
        new_info['threshold'] = parse_safe_number(info['threshold'])
        # new_info['index'] = index + 1
        # new_info['status'] = getStatus(info['status'])
        # new_info['balance'] = getBalance(info['balance'])
        new_info['success'] = False # 这个是额外增加来对齐yepay的
        new_info['records'] = []

        newInfos.append(new_info)
    return newInfos

def getTargetNumber(threshold, spending_limit , option):
    if option == False:
        target = 1
    else:
        if spending_limit == 0 :
            target = 0
        else:
            if threshold < 10 :
                target = 15
            elif threshold < 50 :
                target = 150
            # elif threshold < 300 :
            #     target = 150 + threshold * 1.2
            else:
                target = 150 + threshold

    target = int(target)
    return target


def getID(id):
    group = re.match(r'ID: (\d+)',id)
    return group.group(1)

def getStatus(status):
    if status == 'Active':
        return True
    else:
        return False

def getCard(card):
    if not card: return None
    group = re.search(r'\b(\d{4})\b',card)
    if group:
        return group.group(1)
    else:
        return None

def getBalance(balance):
    group = re.search(r'\$(\d+\.\d+)\b',balance)
    if group:
        return group.group(1)
    else:
        return None

def getOption(status, card):
    if status == "Active" and card:
        return True
    else:
        return False

if __name__ == '__main__':
    from informations.test_data import account_infos
    infos = changeInfo(account_infos)
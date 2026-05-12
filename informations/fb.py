class Xpath:

    def __init__(self,info):
        self.bussiness_id = info['business_id']
        self.bm = self.bm()
        self.acc_trs = self.acc_trs()
        self.acc_trs_id = "./td[1]/div/div/div/span/div/div[2]/span[2]"
        self.acc_trs_name = "./td[1]/div/div/div/span/div/div[2]/span[1]"
        self.acc_trs_status = "./td[2]/div/div/span[2]"
        self.acc_trs_card = "./td[3]/div/div/div"
        self.acc_trs_balance = "./td[4]/div/span/div/div"
        self.acc_trs_option = "./td[5]/div/div/div[1]/div/span/div/div/div"
        # xpath前面 加. 应用于已经找到父亲元素的情况 在父亲元素的 路径下 搜索
        self.acc_pay = self.acc_pay()
        self.acc_confirm = self.acc_confirm()


    def acc_confirm(self):
        return "//div[@aira-label='Confirm']"

    def acc_pay(self):
        return "/html/body/div[3]/div[2]/div[1]/div[1]/div/div/div/div/div/div/div/div[1]/div[3]/div/div[1]/span/div/div[1]/div/div[2]/div[2]/div[2]/div/div/div"

    def acc_pay(self):
        return "/html/body/div[3]/div[2]/div[1]/div[1]/div/div/div/div/div/div/div/div[1]/div[3]/div/div[1]/span/div/div[1]/div/div[2]/div[2]/div[2]/div/div/div"

    def acc_trs(self):
        return "/html/body/div[1]/div[1]/div/span/div/div[1]/div[2]/div/div/div/div/div/div/div[2]/span/div/div/div[1]/div/div/div/div/div/div[3]/div/div/div[1]/div[4]/div/div/table/tbody/tr"

    def bm(self,):
        # bm_list = f"/html/body/div[1]/div[1]/div/div[2]/div/div/div/div/span/div/div[3]/table/tbody/tr[2]/td[]"
        # 找的是这个td: f"/html/body/div[1]/div[1]/div/div[2]/div/div/div/div/span/div/div[3]/table/tbody/tr[2]/td[]"
        # [] 里面是条件
        # [a] 查找td的直接孩子a
        # [.//] 查找td的所有下级孩子a
        # [a[contains(@href,‘328139021’)]]
        # [contains(attr,'text')] 就是 在指定的attr里面查找text
        bm = f"/html/body/div[1]/div[1]/div/div[2]/div/div/div/div/div/div[3]/table/tbody/tr[td[a[contains(@href,'business_id={self.bussiness_id}')]]]/td[a[contains(@href,'business_id={self.bussiness_id}')]]/a"
        # bm = f"/html/body/div[1]/div[1]/div/div[2]/div/div/div/div/span/div/div[3]/table/tbody/tr[td[a[contains(@href,'business_id={self.bussiness_id}')]]]/td[a[contains(@href,'business_id={self.bussiness_id}')]]/a"
        return bm

class Routes:
    def __init__(self, info):
        self.fb_url = "https://mbasic.facebook.com"
        self.ads_url = "https://adsmanager.facebook.com"
        self.billing_gate = f"https://business.facebook.com/billing_hub/accounts"
        self.billing_overview_url = f"https://business.facebook.com/billing_hub/accounts?business_id={info['business_id']}&placement=ads_manager&global_scope_id=2347907231899852"


class bm:

    def __init__(self,info):
        self.business_id = info["business_id"]
        self.routes = Routes(info)
        self.xp = Xpath(info)


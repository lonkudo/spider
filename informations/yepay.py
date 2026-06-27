from .authenticator import get_totp_from_input
from .yepay_clients import clients, check_clients
from .yepay_kaduans import kaduans


class Page:
    login = "忘记密码?"
    auth = "安全验证"
    home = "首页"

class Routes:
    base_url = "https://ye-pay.com/#/"
    cards = base_url + "cards"
    login = base_url + "login"
    kaduans = base_url + "products"
    logs = base_url + "log_card_trade"

class yepay:

    account = "567888"
    password = "123dsa123DSA"
    secret = "F6O5CUV3QBCPF5JC5PWJZ6FLWZNKO2CU"
    page = Page()
    routes = Routes()

    @classmethod
    def genKey(cls):
        return get_totp_from_input(cls.secret)

    def __init__(self,type):
        routes = Routes()
        self.empty = "span.el-table__empty-text"

        if type == "cards":
            self.type = "cards"
            self.searchPlaceholder = "卡号(输后四位也能查)"
            self.searchFormIndex = 6
            self.balanceCell = "td.el-table_1_column_7.is-center.el-table__cell"
            self.operatorCell = "td.el-table_1_column_13.is-center.el-table__cell"
            self.infos = clients
            self.check_infos = check_clients
            self.routes = routes.cards
            self.submitFooterIndex = 2
            self.passwordFooterIndex = 7
            self.statusCell = "td.el-table_1_column_8.is-center.el-table__cell"
            self.bindCardSubmitFooterIndex =0
            self.logs = routes.logs

        elif type == "kaduans":
            self.type = "kaduans"
            self.searchPlaceholder = "卡段"
            self.searchFormIndex = -2
            self.balanceCell = "td.el-table_1_column_2.is-center.el-table__cell"
            self.operatorCell = "td.el-table_1_column_11.is-center.el-table__cell"
            self.infos = kaduans
            self.check_infos = []
            self.routes = routes.kaduans
            self.submitFooterIndex = 0
            self.passwordFooterIndex = 7
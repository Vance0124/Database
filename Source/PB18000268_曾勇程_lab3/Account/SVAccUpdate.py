from PyQt5.QtWidgets import QDialog, QMessageBox
from Account.AccountUI.SVAccountUpdate import Ui_SVAccUpdate

from db import *
import re

def ISEmpty(left, right, isString=True):
    if right == '':
        return '1 = 1'
    else:
        return left + ' = ' + IsString(right, isString)


def IsString(value, isString=True):
    if isString:
        return '\'' + value + '\''
    else:
        return value


def StringPre(String):      # 预处理字符串，应对含有特殊字符的输入
    SS = ''
    for c in String:
        if c == '\'' or c == '"' or c == '\\':
            SS += '\\' + c
        else:
            SS += c
    print(SS)
    return SS


class SVAccUpdate(QDialog):
    "A dialog class for Ui_LoginDialog, who can show itself"

    def __init__(self, parent):
        super(SVAccUpdate, self).__init__(parent)
        self.ui = Ui_SVAccUpdate()
        self.ui.setupUi(self)
        self.before = ''    # 用于修改SV_Account
        self.accbefore = ''   # 用于修改Account
        self.query = ''     # 用于修改SV_Account
        self.accquery = ''    # 用于修改Account
        self.tabName_SV = 'SV_account'
        self.tabName = 'Transact'
        self.accountName = 'Account'

        self.ui.pushButton.clicked.connect(self.Update)

        self.parent = parent

    def Update(self):
        balance_be = self.ui.Before_1.text()
        time_open_be = self.ui.Before_2.text()
        time_access_be = self.ui.Before_3.text()
        rate_be = self.ui.Before_4.text()
        currency_be = self.ui.Before_5.text()
        ID_be = self.ui.Before_6.text()

        name_be = self.ui.Before_7.text()
        ID_card_be = self.ui.Before_8.text()

        balance_af = self.ui.After_1.text()
        time_open_af = self.ui.After_2.text()
        time_access_af = self.ui.After_3.text()
        rate_af = self.ui.After_4.text()
        currency_af = self.ui.After_5.text()

        name_af = self.ui.After_7.text()
        ID_card_af = self.ui.After_8.text()

        name_be = StringPre(name_be)  # 预处理，应对特殊字符

        if time_open_be != '':
            open1 = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", time_open_be)
            open2 = re.search(r"(\d{4}.\d{1,2}.\d{1,2})", time_open_be)
            if not open1 and not open2:  # 判断是否有问题
                self.error_input('修改前的开户日期格式不正确!')
                return
            if open1:
                time_open_be = open1.group(0)
            else:
                time_open_be = open2.group(0)

        if time_access_be != '':
            access1 = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", time_access_be)
            access2 = re.search(r"(\d{4}.\d{1,2}.\d{1,2})", time_access_be)
            if not access1 and not access2:  # 判断是否有问题
                self.error_input('修改前最近访问日期格式不正确!')
                return
            if access1:
                time_access_be = access1.group(0)
            else:
                time_access_be = access2.group(0)

        if time_open_af != '':
            open1 = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", time_open_af)
            open2 = re.search(r"(\d{4}.\d{1,2}.\d{1,2})", time_open_af)
            if not open1 and not open2:  # 判断是否有问题
                self.error_input('修改后的开户日期格式不正确!')
                return
            if open1:
                time_open_af = open1.group(0)
            else:
                time_open_af = open2.group(0)

        if time_access_af != '':
            access1 = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", time_access_af)
            access2 = re.search(r"(\d{4}.\d{1,2}.\d{1,2})", time_access_af)
            if not access1 and not access2:  # 判断是否有问题
                self.error_input('修改后最近访问日期格式不正确!')
                return
            if access1:
                time_access_af = access1.group(0)
            else:
                time_access_af = access2.group(0)

        currency_be = StringPre(currency_be)    # 预处理，应对特殊字符

        self.before = ISEmpty('ID', ID_be, False) + ' and ' + ISEmpty('balance', balance_be, False) + ' and ' \
                      + ISEmpty('TIME_open', time_open_be) + ' and ' + ISEmpty('TIME_access', time_access_be) + ' and ' + \
                      ISEmpty('rate', rate_be, False) + ' and ' + ISEmpty('currency', currency_be) + ';'

        self.accbefore = ISEmpty('ID', ID_be, False) + ' and ' + ISEmpty('balance', balance_be, False) + ' and ' \
                         + ISEmpty('TIME_open', time_open_be) + ' and ' + ISEmpty('TIME_access', time_access_be) + ';'
        print("Before: ", self.before)
        print("Account: ", self.accbefore)
        NotEmpty_af = list()    # 用于取 set 的固定格式
        AccNotEmpty_af = list()     # Account 部分
        if balance_af != '':
            NotEmpty_af.append(('balance', balance_af))
            AccNotEmpty_af.append(('balance', balance_af))
        if time_open_af != '':
            NotEmpty_af.append(('TIME_open', time_open_af))
            AccNotEmpty_af.append(('TIME_open', time_open_af))
        if time_access_af != '':
            NotEmpty_af.append(('TIME_access', time_access_af))
            AccNotEmpty_af.append(('TIME_access', time_access_af))
        if rate_af != '':
            NotEmpty_af.append(('rate', rate_af))
        if currency_af != '':
            currency_af = StringPre(currency_af)    # 预处理，应对特殊字符
            NotEmpty_af.append(('currency', currency_af))

        Num_af = len(NotEmpty_af)
        Num_af_Flag = 1  # 标记是否需要修改 SV表
        if Num_af == 0:
            Num_af_Flag = 0
        Str_af = ''         # 修改 SV_Account
        if Num_af_Flag == 1:
            while Num_af != 1:
                item = NotEmpty_af.pop()    # 弹出一个项目
                Num_af -= 1     # 减一
                if item[0] == 'TIME_open' or item[0] == 'TIME_access' or item[0] == 'currency':
                    Str_af += ISEmpty(item[0], item[1]) + ' , '
                else:
                    Str_af += ISEmpty(item[0], item[1], False) + ' , '

            item = NotEmpty_af.pop()  # 弹出一个项目
            Num_af -= 1  # 减一
            if item[0] == 'TIME_open' or item[0] == 'TIME_access' or item[0] == 'currency':
                Str_af += ISEmpty(item[0], item[1]) + ' '
            else:
                Str_af += ISEmpty(item[0], item[1], False) + ' '

        AccFlagNum = 1
        ACCNum_af = len(AccNotEmpty_af)
        ACCStr_af = ''  # 修改 SV_Account
        if ACCNum_af == 0:
            AccFlagNum = 0      # 表示 Account 不需要修改
        else:
            while ACCNum_af != 1:
                item = AccNotEmpty_af.pop()  # 弹出一个项目
                ACCNum_af -= 1  # 减一
                if item[0] == 'TIME_open' or item[0] == 'TIME_access':
                    ACCStr_af += ISEmpty(item[0], item[1]) + ' , '
                else:
                    ACCStr_af += ISEmpty(item[0], item[1], False) + ' , '
            item = AccNotEmpty_af.pop()  # 弹出一个项目
            ACCNum_af -= 1  # 减一
            if item[0] == 'TIME_open' or item[0] == 'TIME_access':
                ACCStr_af += ISEmpty(item[0], item[1]) + ' '
            else:
                ACCStr_af += ISEmpty(item[0], item[1], False) + ' '

        self.accquery = 'update ' + self.accountName + ' set ' + ACCStr_af + ' where ' + self.accbefore
        self.query = 'update ' + self.tabName_SV + ' set ' + Str_af + ' where ' + self.before

        ###################################################################################################################
        acctype = '1'  # 这里开始修改 Transact

        self.before_tran = ISEmpty('name', name_be) + ' and ' + ISEmpty('ID_card', ID_card_be) + ' and ' \
                           + ISEmpty('Type', acctype, False) + ' and ' + ISEmpty('ID', ID_be, False) + ';'

        print("Tran, ", self.before_tran)

        ##################################################################################################修改部分
        NotEmpty_af_tran = list()  # 用于取 set 的固定格式
        if name_af != '':
            name_af = StringPre(name_af)  # 预处理，应对特殊字符
            NotEmpty_af_tran.append(('name', name_af))
        if ID_card_af != '':
            if len(ID_card_af) != 18:
                self.error_input('修改后的客户身份证号输入位数不正确！')
                return
            NotEmpty_af_tran.append(('ID_card', ID_card_af))
        Num_af_tran = len(NotEmpty_af_tran)
        ##################################################################################################
        Tran_Flag = 1
        if Num_af_tran == 0:
            Tran_Flag = 0
        Str_af = ''
        if Tran_Flag == 1:
            while Num_af_tran != 1:
                item = NotEmpty_af_tran.pop()  # 弹出一个项目
                Num_af_tran -= 1  # 减一
                if item[0] == 'name' or item[0] == 'ID_card':
                    Str_af += ISEmpty(item[0], item[1]) + ' , '
                else:
                    Str_af += ISEmpty(item[0], item[1], False) + ' , '

            item = NotEmpty_af_tran.pop()  # 弹出一个项目
            Num_af_tran -= 1  # 减一
            if item[0] == 'name' or item[0] == 'ID_card':
                Str_af += ISEmpty(item[0], item[1]) + ' '
            else:
                Str_af += ISEmpty(item[0], item[1], False) + ' '

        self.query_tran = 'update ' + self.tabName + ' set ' + Str_af + ' where ' + self.before_tran

        reply = QMessageBox.question(self, '确认', "确定执行操作?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return
        self.get_query(self.accquery, self.query, self.query_tran, AccFlagNum, Num_af_Flag, Tran_Flag, False)

        self.close()

    def get_query(self, Q1, Q2, Q3, flag1, flag2, flag3, need_fetch):
        print(Q1)
        print(Q2)
        result = []
        # print(self.db)
        cursor = self.parent.parent.db.cursor()  # 获得数据库游标
        try:
            if flag3:
                cursor.execute(Q3)
            if flag1:  # Account 也需要修改
                cursor.execute(Q1)
            if flag2:
                cursor.execute(Q2)
        except:
            self.error_input('SQL query denied, please check your input!')
            return
        if need_fetch:
            result = cursor.fetchall()
        self.parent.parent.db.commit()
        cursor.close()
        return result

    def error_input(self, err_msg):
        QMessageBox.information(self, "消息", err_msg, QMessageBox.Yes | QMessageBox.No)
        self.close()

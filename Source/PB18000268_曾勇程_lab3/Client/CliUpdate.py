from PyQt5.QtWidgets import QDialog, QMessageBox
from Client.ClientUI.ClientUpdate import Ui_ClientUpdate

from db import *


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


class ClientUpdate(QDialog):
    "A dialog class for Ui_LoginDialog, who can show itself"

    def __init__(self, parent):
        super(ClientUpdate, self).__init__(parent)
        self.ui = Ui_ClientUpdate()
        self.ui.setupUi(self)
        self.before = ''
        self.query = ''
        self.tabName = 'client'

        self.ui.pushButton.clicked.connect(self.Update)

        self.parent = parent

    def Update(self):
        ID_be = self.ui.Before_1.text()
        clerk_ID_be = self.ui.Before_2.text()
        name_be = self.ui.Before_3.text()
        telephone_be = self.ui.Before_4.text()
        address_be = self.ui.Before_5.text()
        clerk_type_be = self.ui.Before_6.text()

        ID_af = self.ui.After_1.text()
        clerk_ID_af = self.ui.After_2.text()
        name_af = self.ui.After_3.text()
        telephone_af = self.ui.After_4.text()
        address_af = self.ui.After_5.text()
        clerk_type_af = self.ui.After_6.text()

        name_be = StringPre(name_be)  # 预处理，应对特殊字符
        address_be = StringPre(address_be)

        self.before = ISEmpty('ID_card', ID_be) + ' and ' \
                      + ISEmpty('cle_ID_card', clerk_ID_be) + ' and ' + ISEmpty('name', name_be) + ' and ' + \
                      ISEmpty('telephone', telephone_be, False) + ' and ' + ISEmpty('address', address_be) \
                      + ' and ' + ISEmpty('clerk_type', clerk_type_be, False) + ';'

        NotEmpty_af = list()    # 用于取 set 的固定格式
        if ID_af != '':
            if len(ID_af) != 18:
                self.error_input('客户身份证号输入位数不正确！')
                return
            NotEmpty_af.append(( 'ID_card', ID_af))
        if clerk_ID_af != '':
            if len(clerk_ID_af) != 18:
                self.error_input('银行职员身份证号输入位数不正确！')
                return
            NotEmpty_af.append(('cle_ID_card', clerk_ID_af))
        if name_af != '':
            name_af = StringPre(name_af)        # 预处理，应对特殊字符
            NotEmpty_af.append(( 'name', name_af))
        if telephone_af != '':
            if len(telephone_af) != 11:
                self.error_input('电话输入位数不正确！')
                return
            NotEmpty_af.append(('telephone', telephone_af))
        if address_af != '':
            address_af = StringPre(address_af)
            NotEmpty_af.append(('address', address_af))
        if clerk_type_af != '':
            if clerk_type_af != '0' and clerk_type_af != '1':
                self.error_input('银行职员类型不正确！')
                return
            NotEmpty_af.append(('clerk_type', clerk_type_af))

        Num_af = len(NotEmpty_af)
        if Num_af == 0:
            return
        Str_af = ''
        while Num_af != 1:
            item = NotEmpty_af.pop()    # 弹出一个项目
            Num_af -= 1     # 减一
            if item[0] == 'ID_card' or item[0] == 'cle_ID_card' or item[0] == 'name' or item[0] == 'address':
                Str_af += ISEmpty(item[0], item[1]) + ' , '
            else:
                Str_af += ISEmpty(item[0], item[1], False) + ' , '

        item = NotEmpty_af.pop()  # 弹出一个项目
        Num_af -= 1  # 减一
        if item[0] == 'ID_card' or item[0] == 'cle_ID_card' or item[0] == 'name' or item[0] == 'address':
            Str_af += ISEmpty(item[0], item[1]) + ' '
        else:
            Str_af += ISEmpty(item[0], item[1], False) + ' '

        self.query = 'update ' + self.tabName + ' set ' + Str_af + ' where ' + self.before

        reply = QMessageBox.question(self, '确认', "确定执行操作?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return
        self.get_query(False)

        self.close()

    def get_query(self, need_fetch):
        print(self.query)
        result = []
        # print(self.db)
        print(self.parent.parent.db)
        cursor = self.parent.parent.db.cursor()  # 获得数据库游标
        try:
            cursor.execute(self.query)
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

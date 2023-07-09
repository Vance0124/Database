from PyQt5.QtWidgets import QDialog, QMessageBox
from Contact.ContactUI.ContactUpdate import Ui_ContactUpdate

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


class ContactUpdate(QDialog):
    "A dialog class for Ui_LoginDialog, who can show itself"

    def __init__(self, parent):
        super(ContactUpdate, self).__init__(parent)
        self.ui = Ui_ContactUpdate()
        self.ui.setupUi(self)
        self.before = ''
        self.query = ''
        self.tabName = 'Contacts'

        self.ui.pushButton.clicked.connect(self.Update)

        self.parent = parent

    def Update(self):
        ID_be = self.ui.Before_1.text()
        name_be = self.ui.Before_2.text()
        telephone_be = self.ui.Before_3.text()
        Email_be = self.ui.Before_4.text()
        relation_be = self.ui.Before_5.text()

        ID_af = self.ui.After_1.text()
        name_af = self.ui.After_2.text()
        telephone_af = self.ui.After_3.text()
        Email_af = self.ui.After_4.text()
        relation_af = self.ui.After_5.text()

        name_be = StringPre(name_be)  # 预处理，应对特殊字符
        Email_be = StringPre(Email_be)
        relation_be = StringPre(relation_be)

        self.before = ISEmpty('ID_card', ID_be) + ' and ' \
                      + ISEmpty('name', name_be) + ' and ' + \
                      ISEmpty('telephone', telephone_be, False) + ' and ' + ISEmpty('Email', Email_be) \
                      + ' and ' + ISEmpty('relation', relation_be) + ';'

        NotEmpty_af = list()    # 用于取 set 的固定格式
        if ID_af != '':
            if len(ID_af) != 18:
                self.error_input('客户身份证号输入位数不正确！')
                return
            NotEmpty_af.append(( 'ID_card', ID_af))
        if name_af != '':
            name_af = StringPre(name_af)  # 预处理，应对特殊字符
            NotEmpty_af.append(( 'name', name_af))
        if telephone_af != '':
            if len(telephone_af) != 11:
                self.error_input('电话输入位数不正确！')
                return
            NotEmpty_af.append(('telephone', telephone_af))
        if Email_af != '':
            Email_af = StringPre(Email_af)
            if '@' not in Email_af:  # Email 格式错误
                self.error_input('Email格式不正确！')
                return
            NotEmpty_af.append(('Email', Email_af))
        if relation_af != '':
            relation_af = StringPre(relation_af)
            NotEmpty_af.append(('relation', relation_af))

        Num_af = len(NotEmpty_af)
        if Num_af == 0:
            return
        Str_af = ''
        while Num_af != 1:
            item = NotEmpty_af.pop()    # 弹出一个项目
            Num_af -= 1     # 减一
            if item[0] == 'ID_card' or item[0] == 'name' or item[0] == 'Email' or item[0] == 'relation':
                Str_af += ISEmpty(item[0], item[1]) + ' , '
            else:
                Str_af += ISEmpty(item[0], item[1], False) + ' , '

        item = NotEmpty_af.pop()  # 弹出一个项目
        Num_af -= 1  # 减一
        if item[0] == 'ID_card' or item[0] == 'name' or item[0] == 'Email' or item[0] == 'relation':
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

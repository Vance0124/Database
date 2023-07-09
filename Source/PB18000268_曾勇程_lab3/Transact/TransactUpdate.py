from PyQt5.QtWidgets import QDialog, QMessageBox
from Transact.TransactUI.TransactUpdate import Ui_TransactUpdate

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


def StringPre(String):  # 预处理字符串，应对含有特殊字符的输入
    SS = ''
    for c in String:
        if c == '\'' or c == '"' or c == '\\':
            SS += '\\' + c
        else:
            SS += c
    print(SS)
    return SS


class TransactUpdate(QDialog):
    "A dialog class for Ui_LoginDialog, who can show itself"

    def __init__(self, parent):
        super(TransactUpdate, self).__init__(parent)
        self.ui = Ui_TransactUpdate()
        self.ui.setupUi(self)
        self.before = ''
        self.query = ''
        self.tabName = 'Transact'

        self.ui.pushButton.clicked.connect(self.Update)

        self.parent = parent

    def Update(self):
        name_be = self.ui.Before_1.text()
        ID_card_be = self.ui.Before_2.text()
        acctype_be = self.ui.Before_3.text()
        accID_be = self.ui.Before_4.text()

        name_af = self.ui.After_1.text()
        ID_card_af = self.ui.After_2.text()
        acctype_af = self.ui.After_3.text()
        accID_af = self.ui.After_4.text()

        name_be = StringPre(name_be)  # 预处理，应对特殊字符

        self.before = ISEmpty('name', name_be) + ' and ' + ISEmpty('ID_card', ID_card_be) + ' and ' \
                      + ISEmpty('Type', acctype_be, False) + ' and ' + ISEmpty('ID', accID_be, False) + ';'

        NotEmpty_af = list()  # 用于取 set 的固定格式
        if name_af != '':
            name_af = StringPre(name_af)  # 预处理，应对特殊字符
            NotEmpty_af.append(('name', name_af))
        if ID_card_af != '':
            if len(ID_card_af) != 18:
                self.error_input('修改后的客户身份证号输入位数不正确！')
                return
            NotEmpty_af.append(('ID_card', ID_card_af))
        if acctype_af != '':
            NotEmpty_af.append(('Type', acctype_af))
        if accID_af != '':
            NotEmpty_af.append(('ID', accID_af))

        Num_af = len(NotEmpty_af)
        if Num_af == 0:
            return
        Str_af = ''
        while Num_af != 1:
            item = NotEmpty_af.pop()  # 弹出一个项目
            Num_af -= 1  # 减一
            if item[0] == 'name' or item[0] == 'ID_card':
                Str_af += ISEmpty(item[0], item[1]) + ' , '
            else:
                Str_af += ISEmpty(item[0], item[1], False) + ' , '

        item = NotEmpty_af.pop()  # 弹出一个项目
        Num_af -= 1  # 减一
        if item[0] == 'name' or item[0] == 'ID_card':
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

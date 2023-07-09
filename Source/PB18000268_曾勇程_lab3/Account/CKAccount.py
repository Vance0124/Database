from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView
from PyQt5 import QtCore
from Account.AccountUI.CKAccountInf import Ui_CKAccount
from Account.CKAccUpdate import CKAccUpdate
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


def StringPre(String):  # 预处理字符串，应对含有特殊字符的输入
    SS = ''
    for c in String:
        if c == '\'' or c == '"' or c == '\\':
            SS += '\\' + c
        else:
            SS += c
    return SS


class CKAccount(QDialog):
    "A dialog class for Ui_LoginDialog, who can show itself"

    def __init__(self, parent):
        super(CKAccount, self).__init__(parent)
        self.tabName_CK = 'CK_account'
        self.tabName_Tran = 'Transact'
        self.accountName = 'Account'
        self.ui = Ui_CKAccount()
        self.ui.setupUi(self)
        self.ui.table.setColumnCount(8)  # 不设置不显示这些列
        self.ui.table.setHorizontalHeaderLabels(
            ['ID', 'balance', 'TIME_open', 'TIME_access', 'overdraft', '支行名字', '所属客户身份证', '账户类型'])
        self.ui.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 设置表格等宽
        self.ui.table.horizontalHeader().setStyleSheet("QHeaderView::section{background:skyblue;}")

        self.ui.pushButton_sw.clicked.connect(self.Display)  # 16:显示
        self.ui.pushButton_add.clicked.connect(self.Add)  # 16:增
        self.ui.pushButton_del.clicked.connect(self.Delete)  # 17：删
        self.ui.pushButton_upda.clicked.connect(self.Update)  # 27：改
        self.ui.pushButton_che.clicked.connect(self.Check)  # 28: 查

        self.parent = parent

    def Display(self):  # 显示
        self.renderTable()

    def Add(self):  # 增
        ID = self.ui.lineEdit_ID.text()
        balance = self.ui.lineEdit_Ba.text()
        time_open = self.ui.lineEdit_DaOP.text()
        TIME_access = self.ui.lineEdit_DaAcc.text()
        overdraft = self.ui.lineEdit_Over.text()
        #######
        name = self.ui.lineEdit_BN.text()
        ID_card = self.ui.lineEdit_ID_card.text()
        acctype = '0'  # 支票账户
        #######

        # 首先进行错误检查
        if ID == '' or balance == '' or time_open == '' or TIME_access == '' or overdraft == '' or name == '' or ID_card == '':
            self.error_input('输入信息不足!')
            return

        if len(ID_card) != 18:
            self.error_input('客户身份证号输入位数不正确！')
            return

        name = StringPre(name)  # 预处理，应对特殊字符

        open1 = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", time_open)
        open2 = re.search(r"(\d{4}.\d{1,2}.\d{1,2})", time_open)
        if not open1 and not open2:  # 判断是否有问题
            self.error_input('开户日期格式不正确!')
            return
        if open1:
            time_open = open1.group(0)
        else:
            time_open = open2.group(0)

        access1 = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", TIME_access)
        access2 = re.search(r"(\d{4}.\d{1,2}.\d{1,2})", TIME_access)
        if not access1 and not access2:  # 判断是否有问题
            self.error_input('最近访问日期格式不正确!')
            return
        if access1:
            TIME_access = access1.group(0)
        else:
            TIME_access = access2.group(0)

        # 插入 SV_Account的记录
        self.query = 'insert into CK_account value(' + IsString(ID, False) + ', ' + IsString(balance,
                                                                                                          False) + ', ' + \
                     IsString(time_open) + ', ' + IsString(TIME_access) + ', ' + IsString(overdraft, False) + ');'

        # 插入 Account的记录
        self.quAcc = 'insert into ' + self.accountName + ' value(' + IsString(ID, False) + ', ' + IsString(balance,
                                                                                                           False) + ', ' + \
                     IsString(time_open) + ', ' + IsString(TIME_access) + ');'

        self.query_tran = 'insert into ' + self.tabName_Tran + ' value(' + IsString(name) + ', ' + \
                          IsString(ID_card) + ', ' + IsString(acctype, False) + ', ' + IsString(ID, False) + ');'
        print("query_tran: ", self.query_tran)
        print(self.query)
        print(self.quAcc)
        flag = 0        # 0 表示插入
        self.get_query(self.quAcc, self.query, self.query_tran, flag, True)
        self.renderTable()

    def Delete(self):  # 增
        # 确认删除
        reply = QMessageBox.question(self, '确认', "确定执行操作?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return

        ID = self.ui.lineEdit_ID.text()
        balance = self.ui.lineEdit_Ba.text()
        time_open = self.ui.lineEdit_DaOP.text()
        TIME_access = self.ui.lineEdit_DaAcc.text()
        overdraft = self.ui.lineEdit_Over.text()

        name = self.ui.lineEdit_BN.text()
        ID_card = self.ui.lineEdit_ID_card.text()
        acctype = '0'  # 支票账户
        #######
        if ID_card != '':
            if len(ID_card) != 18:
                self.error_input('客户身份证号输入位数不正确！')
                return
        if name != '':
            name = StringPre(name)  # 预处理，应对特殊字符

        if time_open != '':
            open1 = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", time_open)
            open2 = re.search(r"(\d{4}.\d{1,2}.\d{1,2})", time_open)
            if not open1 and not open2:  # 判断是否有问题
                self.error_input('开户日期格式不正确!')
                return
            if open1:
                time_open = open1.group(0)
            else:
                time_open = open2.group(0)

        if TIME_access != '':
            access1 = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", TIME_access)
            access2 = re.search(r"(\d{4}.\d{1,2}.\d{1,2})", TIME_access)
            if not access1 and not access2:  # 判断是否有问题
                self.error_input('最近访问日期格式不正确!')
                return
            if access1:
                TIME_access = access1.group(0)
            else:
                TIME_access = access2.group(0)

        # 销毁 SV_Account的记录
        self.query = 'delete from CK_account where ' + ISEmpty('ID', ID, False) + ' and ' \
                     + ISEmpty('balance', balance, False) + ' and ' + ISEmpty('TIME_open', time_open) + \
                     ' and ' + ISEmpty('TIME_access', TIME_access) + ' and ' + ISEmpty('overdraft', overdraft,
                                                                                       False) + ';'

        # 销毁 Account的记录
        self.quAcc = 'delete from ' + self.accountName + ' where ' + ISEmpty('ID', ID, False) + ' and ' \
                     + ISEmpty('balance', balance, False) + ' and ' + ISEmpty('TIME_open', time_open) + \
                     ' and ' + ISEmpty('TIME_access', TIME_access) + ';'

        self.query_tran = 'delete from ' + self.tabName_Tran + ' where ' + ISEmpty('name', name) + ' and ' \
                     + ISEmpty('ID_card', ID_card) + ' and ' + ISEmpty('Type', acctype, False) + ' and ' \
                     + ISEmpty('ID', ID, False) + ';'
        print("query_TRAN  : ", self.query_tran)
        print(self.query)
        print(self.quAcc)
        flag = 1
        self.get_query(self.query, self.quAcc, self.query_tran, flag, True)
        self.renderTable()

    def Update(self):
        upda = CKAccUpdate(self)
        upda.exec_()
        self.renderTable()

    def Check(self):
        ID = self.ui.lineEdit_ID.text()
        balance = self.ui.lineEdit_Ba.text()
        time_open = self.ui.lineEdit_DaOP.text()
        TIME_access = self.ui.lineEdit_DaAcc.text()
        overdraft = self.ui.lineEdit_Over.text()

        name = self.ui.lineEdit_BN.text()
        ID_card = self.ui.lineEdit_ID_card.text()
        acctype = '0'  # 支票账户
        #######
        if ID_card != '':
            if len(ID_card) != 18:
                self.error_input('客户身份证号输入位数不正确！')
                return
        if name != '':
            name = StringPre(name)  # 预处理，应对特殊字符

        if time_open != '':
            open1 = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", time_open)
            open2 = re.search(r"(\d{4}.\d{1,2}.\d{1,2})", time_open)
            if not open1 and not open2:  # 判断是否有问题
                self.error_input('开户日期格式不正确!')
                return
            if open1:
                time_open = open1.group(0)
            else:
                time_open = open2.group(0)

        if TIME_access != '':
            access1 = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", TIME_access)
            access2 = re.search(r"(\d{4}.\d{1,2}.\d{1,2})", TIME_access)
            if not access1 and not access2:  # 判断是否有问题
                self.error_input('最近访问日期格式不正确!')
                return
            if access1:
                TIME_access = access1.group(0)
            else:
                TIME_access = access2.group(0)

        self.query = 'select * from CK_account, Transact where Transact.ID = CK_account.ID and '\
                     + ISEmpty('CK_account.ID', ID, False) + ' and ' + ISEmpty('balance', balance, False) + ' and ' +\
                     ISEmpty('TIME_open', time_open) + ' and ' + ISEmpty('TIME_access', TIME_access) + ' and ' +\
                     ISEmpty('overdraft', overdraft,False) + ' and '+ ISEmpty('name', name) + ' and ' +\
                     ISEmpty('ID_card', ID_card) + ' and ' + ISEmpty('Type', acctype, False) + ';'

        print('dfsdfdsfs: ',self.query)
        items = db_check(self.parent.db, self.query)
        self.CheckShow(items)

    def CheckShow(self, Items):
        self.ui.table.setRowCount(0)
        currentRowCount = self.ui.table.rowCount()

        for record in Items:
            self.ui.table.insertRow(currentRowCount)
            ID = QTableWidgetItem(str(record[0]))
            ID.setTextAlignment(QtCore.Qt.AlignCenter)
            balance = QTableWidgetItem(str(record[1]))
            balance.setTextAlignment(QtCore.Qt.AlignCenter)
            time_open = QTableWidgetItem(str(record[2]))
            time_open.setTextAlignment(QtCore.Qt.AlignCenter)
            TIME_access = QTableWidgetItem(str(record[3]))
            TIME_access.setTextAlignment(QtCore.Qt.AlignCenter)
            overdraft = QTableWidgetItem(str(record[4]))
            overdraft.setTextAlignment(QtCore.Qt.AlignCenter)
            #######################
            name = QTableWidgetItem(str(record[5]))
            name.setTextAlignment(QtCore.Qt.AlignCenter)
            ID_card = QTableWidgetItem(str(record[6]))
            ID_card.setTextAlignment(QtCore.Qt.AlignCenter)
            acctype = QTableWidgetItem(str(record[7]))
            acctype.setTextAlignment(QtCore.Qt.AlignCenter)  # 支票账户

            self.ui.table.setItem(currentRowCount, 0, ID)  # 列1
            self.ui.table.setItem(currentRowCount, 1, balance)  # 列2
            self.ui.table.setItem(currentRowCount, 2, time_open)  # 列3
            self.ui.table.setItem(currentRowCount, 3, TIME_access)  # 列4
            self.ui.table.setItem(currentRowCount, 4, overdraft)  # 列5
            self.ui.table.setItem(currentRowCount, 5, name)  # 列6
            self.ui.table.setItem(currentRowCount, 6, ID_card)  # 列7
            self.ui.table.setItem(currentRowCount, 7, acctype)  # 列8
            currentRowCount += 1
            self.ui.table.setRowCount(currentRowCount)

    def renderTable(self):
        self.ui.table.setRowCount(0)
        query = 'select * from CK_account, Transact where Transact.ID = CK_account.ID;'
        # tab = db_show(self.parent.db, T)
        tab = db_check(self.parent.db, query)
        currentRowCount = self.ui.table.rowCount()

        for record in tab:
            self.ui.table.insertRow(currentRowCount)
            ID = QTableWidgetItem(str(record[0]))
            ID.setTextAlignment(QtCore.Qt.AlignCenter)
            balance = QTableWidgetItem(str(record[1]))
            balance.setTextAlignment(QtCore.Qt.AlignCenter)
            time_open = QTableWidgetItem(str(record[2]))
            time_open.setTextAlignment(QtCore.Qt.AlignCenter)
            TIME_access = QTableWidgetItem(str(record[3]))
            TIME_access.setTextAlignment(QtCore.Qt.AlignCenter)
            overdraft = QTableWidgetItem(str(record[4]))
            overdraft.setTextAlignment(QtCore.Qt.AlignCenter)
            #######################
            name = QTableWidgetItem(str(record[5]))
            name.setTextAlignment(QtCore.Qt.AlignCenter)
            ID_card = QTableWidgetItem(str(record[6]))
            ID_card.setTextAlignment(QtCore.Qt.AlignCenter)
            acctype = QTableWidgetItem(str(record[7]))
            acctype.setTextAlignment(QtCore.Qt.AlignCenter)  # 支票账户

            self.ui.table.setItem(currentRowCount, 0, ID)  # 列1
            self.ui.table.setItem(currentRowCount, 1, balance)  # 列2
            self.ui.table.setItem(currentRowCount, 2, time_open)  # 列3
            self.ui.table.setItem(currentRowCount, 3, TIME_access)  # 列4
            self.ui.table.setItem(currentRowCount, 4, overdraft)  # 列5
            self.ui.table.setItem(currentRowCount, 5, name)  # 列6
            self.ui.table.setItem(currentRowCount, 6, ID_card)  # 列7
            self.ui.table.setItem(currentRowCount, 7, acctype)  # 列8
            currentRowCount += 1
            self.ui.table.setRowCount(currentRowCount)

    def get_query(self, Q1, Q2, Q3, flag, need_fetch):
        # print(self.query)
        result = []
        # print(self.db)
        print("flag:::::: ", flag)
        cursor = self.parent.db.cursor()  ########################
        try:
            if flag == 0:   # add
                cursor.execute(Q1)
                cursor.execute(Q2)
                cursor.execute(Q3)  # Transact
            elif flag == 1:     # delete
                cursor.execute(Q3)  # Transact先清除
                cursor.execute(Q1)
                cursor.execute(Q2)
        except:
            self.error_input('SQL query denied, please check your input!')
            return
        if need_fetch:
            result = cursor.fetchall()
        self.parent.db.commit()
        cursor.close()
        return result

    def error_input(self, err_msg):
        QMessageBox.information(self, "消息", err_msg, QMessageBox.Yes | QMessageBox.No)

        # self.close()
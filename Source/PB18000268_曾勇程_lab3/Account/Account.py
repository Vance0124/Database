from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView
from PyQt5 import QtCore
from Account.AccountUI.AccountInf import Ui_Account
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
    return SS


class Account(QDialog):
    "A dialog class for Ui_LoginDialog, who can show itself"

    def __init__(self, parent):
        super(Account, self).__init__(parent)
        self.tabName = 'Account'
        self.ui = Ui_Account()
        self.ui.setupUi(self)
        self.ui.table.setColumnCount(4)  # 不设置不显示这些列
        self.ui.table.setHorizontalHeaderLabels(['ID', 'balance', 'TIME_open', 'TIME_access'])
        self.ui.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 设置表格等宽
        self.ui.table.horizontalHeader().setStyleSheet("QHeaderView::section{background:skyblue;}")

        self.ui.pushButton_sw.clicked.connect(self.Display)  # 16:显示
        # self.ui.pushButton_add.clicked.connect(self.Add)  # 16:增
        # self.ui.pushButton_del.clicked.connect(self.Delete)  # 17：删
        # self.ui.pushButton_upda.clicked.connect(self.Update)  # 27：改
        self.ui.pushButton_che.clicked.connect(self.Check)  # 28: 查

        self.parent = parent

    def Display(self):  # 显示
        self.renderTable(self.tabName)

    def Check(self):
        ID = self.ui.lineEdit_ID.text()
        balance = self.ui.lineEdit_Ba.text()
        time_open = self.ui.lineEdit_DaOP.text()
        TIME_access = self.ui.lineEdit_DaAcc.text()

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

        self.query = 'select * from ' + self.tabName + ' where ' + ISEmpty('ID', ID, False) + ' and ' \
                     + ISEmpty('balance', balance, False) + ' and ' + ISEmpty('TIME_open', time_open)+ \
                     ' and ' + ISEmpty('TIME_access', TIME_access) + ';'
        # items = db_check(self.parent.db, self.query)
        items = self.get_query(True)
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

            self.ui.table.setItem(currentRowCount, 0, ID)  # 列1
            self.ui.table.setItem(currentRowCount, 1, balance)  # 列2
            self.ui.table.setItem(currentRowCount, 2, time_open)  # 列3
            self.ui.table.setItem(currentRowCount, 3, TIME_access)  # 列4
            currentRowCount += 1
            self.ui.table.setRowCount(currentRowCount)

    def renderTable(self, T):
        self.ui.table.setRowCount(0)
        tab = db_show(self.parent.db, T)
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

            self.ui.table.setItem(currentRowCount, 0, ID)  # 列1
            self.ui.table.setItem(currentRowCount, 1, balance)  # 列2
            self.ui.table.setItem(currentRowCount, 2, time_open)  # 列3
            self.ui.table.setItem(currentRowCount, 3, TIME_access)  # 列4
            currentRowCount += 1
            self.ui.table.setRowCount(currentRowCount)

    def get_query(self, need_fetch):
        result = []
        # print(self.db)
        cursor = self.parent.db.cursor()  ########################
        try:
            cursor.execute(self.query)
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
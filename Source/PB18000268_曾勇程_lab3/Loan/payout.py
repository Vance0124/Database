from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView
from PyQt5 import QtCore
from Loan.LoanUI.payoutInf import Ui_payout
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


class payout(QDialog):
    "A dialog class for Ui_LoginDialog, who can show itself"

    def __init__(self, parent):
        super(payout, self).__init__(parent)
        self.tabName = 'payout'
        self.ui = Ui_payout()
        self.ui.setupUi(self)
        self.ui.table.setColumnCount(4)  # 不设置不显示这些列
        self.ui.table.setHorizontalHeaderLabels(['支行名字', '贷款号', '支付日期', '支付金额'])
        self.ui.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 设置表格等宽
        self.ui.table.horizontalHeader().setStyleSheet("QHeaderView::section{background:skyblue;}")

        self.ui.pushButton_sw.clicked.connect(self.Display)  # 16:显示
        self.ui.pushButton_add.clicked.connect(self.Add)  # 16:增
        self.ui.pushButton_del.clicked.connect(self.Delete)  # 17：删
        self.ui.pushButton_che.clicked.connect(self.Check)  # 28: 查

        self.parent = parent

    def Display(self):  # 显示
        self.renderTable(self.tabName)

    def Add(self):  # 增
        name = self.ui.lineEdit_BN.text()
        ID = self.ui.lineEdit_ID.text()
        paydate = self.ui.lineEdit_date.text()
        money = self.ui.lineEdit_money.text()
        if ID == '' or name == '' or money == '' or paydate == '':
            self.error_input('输入信息不足!')
            return

        name = StringPre(name)  # 预处理，应对特殊字符

        open1 = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", paydate)
        open2 = re.search(r"(\d{4}.\d{1,2}.\d{1,2})", paydate)
        if not open1 and not open2:  # 判断是否有问题
            self.error_input('付款日期格式不正确!')
            return
        if open1:
            paydate = open1.group(0)
        else:
            paydate = open2.group(0)
        self.query = "select money_loan from Loans where " + ISEmpty('name', name) + ' and ' \
                     + ISEmpty('ID_loan', ID, False) + ';'  # 统计特定贷款总共需要支付多少钱

        record = db_check(self.parent.db, self.query)

        if len(record) == 0:
            self.error_input('没有相关的贷款!')
            return

        total_money = record[0]  # 该贷款单总共需要付的前

        self.query = "select money_pay from payout where " + ISEmpty('name', name) + ' and ' \
                     + ISEmpty('ID_loan', ID, False) + ';'  # 统计特定贷款已经支付了多少钱
        pay = db_total_money(self.parent.db, self.query)
        willpay = pay + float(money)  # 将要付的钱
        if willpay > total_money[0]:
            self.error_input("发放的金额已经超过该贷款总金额，最多还需发放 " + str(total_money[0] - pay) + " 元！")
            return

        self.query = 'insert into ' + self.tabName + ' value(' + IsString(name) + ', ' + \
                     IsString(ID, False) + ', ' + IsString(paydate) + ', ' + IsString(money, False) + ');'
        self.get_query(True)
        self.renderTable(self.tabName)

    def Delete(self):  # 删
        # 确认删除
        reply = QMessageBox.question(self, '确认', "确定执行操作?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return

        name = self.ui.lineEdit_BN.text()
        ID = self.ui.lineEdit_ID.text()
        paydate = self.ui.lineEdit_date.text()
        money = self.ui.lineEdit_money.text()

        if paydate != '':
            open1 = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", paydate)
            open2 = re.search(r"(\d{4}.\d{1,2}.\d{1,2})", paydate)
            if not open1 and not open2:  # 判断是否有问题
                self.error_input('付款日期格式不正确!')
                return
            if open1:
                paydate = open1.group(0)
            else:
                paydate = open2.group(0)

        name = StringPre(name)  # 预处理，应对特殊字符

        self.query = 'delete from ' + self.tabName + ' where ' + ISEmpty('name', name) + ' and ' \
                     + ISEmpty('ID_loan', ID, False) + ' and ' + ISEmpty('TIME_pay', paydate) + ' and ' \
                     + ISEmpty('money_pay', money, False) + ';'
        self.get_query(True)
        self.renderTable(self.tabName)

    def Check(self):
        name = self.ui.lineEdit_BN.text()
        ID = self.ui.lineEdit_ID.text()
        paydate = self.ui.lineEdit_date.text()
        money = self.ui.lineEdit_money.text()

        if paydate != '':
            open1 = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", paydate)
            open2 = re.search(r"(\d{4}.\d{1,2}.\d{1,2})", paydate)
            if not open1 and not open2:  # 判断是否有问题
                self.error_input('付款日期格式不正确!')
                return
            if open1:
                paydate = open1.group(0)
            else:
                paydate = open2.group(0)

        name = StringPre(name)  # 预处理，应对特殊字符

        self.query = 'select * from ' + self.tabName + ' where ' + ISEmpty('name', name) + ' and ' \
                     + ISEmpty('ID_loan', ID, False) + ' and ' + ISEmpty('TIME_pay', paydate) + ' and ' \
                     + ISEmpty('money_pay', money, False) + ';'
        items = self.get_query(True)
        self.CheckShow(items)

    def CheckShow(self, Items):
        self.ui.table.setRowCount(0)
        currentRowCount = self.ui.table.rowCount()

        for record in Items:
            self.ui.table.insertRow(currentRowCount)
            name = QTableWidgetItem(str(record[0]))  # 支行名字
            name.setTextAlignment(QtCore.Qt.AlignCenter)
            ID = QTableWidgetItem(str(record[1]))  # 贷款号
            ID.setTextAlignment(QtCore.Qt.AlignCenter)
            paydate = QTableWidgetItem(str(record[2]))
            paydate.setTextAlignment(QtCore.Qt.AlignCenter)
            money = QTableWidgetItem(str(record[3]))
            money.setTextAlignment(QtCore.Qt.AlignCenter)

            self.ui.table.setItem(currentRowCount, 0, name)  # 列1
            self.ui.table.setItem(currentRowCount, 1, ID)  # 列2
            self.ui.table.setItem(currentRowCount, 2, paydate)  # 列3
            self.ui.table.setItem(currentRowCount, 3, money)  # 列4
            currentRowCount += 1
            self.ui.table.setRowCount(currentRowCount)

    def renderTable(self, T):
        self.ui.table.setRowCount(0)
        tab = db_show(self.parent.db, T)
        currentRowCount = self.ui.table.rowCount()

        for record in tab:
            self.ui.table.insertRow(currentRowCount)
            name = QTableWidgetItem(str(record[0]))  # 支行名字
            name.setTextAlignment(QtCore.Qt.AlignCenter)
            ID = QTableWidgetItem(str(record[1]))  # 贷款号
            ID.setTextAlignment(QtCore.Qt.AlignCenter)
            paydate = QTableWidgetItem(str(record[2]))
            paydate.setTextAlignment(QtCore.Qt.AlignCenter)
            money = QTableWidgetItem(str(record[3]))
            money.setTextAlignment(QtCore.Qt.AlignCenter)

            self.ui.table.setItem(currentRowCount, 0, name)  # 列1
            self.ui.table.setItem(currentRowCount, 1, ID)  # 列2
            self.ui.table.setItem(currentRowCount, 2, paydate)  # 列3
            self.ui.table.setItem(currentRowCount, 3, money)  # 列4
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

        # self.close()

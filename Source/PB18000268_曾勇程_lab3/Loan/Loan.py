from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView
from PyQt5 import QtCore
from Loan.LoanUI.LoanInf import Ui_Loan
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


class Loan(QDialog):
    "A dialog class for Ui_LoginDialog, who can show itself"

    def __init__(self, parent):
        super(Loan, self).__init__(parent)
        self.tabName_L = 'Loans'
        self.tabName = 'Hold_C_L'
        self.ui = Ui_Loan()
        self.ui.setupUi(self)
        self.ui.table.setColumnCount(6)  # 不设置不显示这些列
        self.ui.table.setHorizontalHeaderLabels(['支行名字', '贷款号', '贷款金额', '开户日期', '状态', '客户身份证号'])
        self.ui.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 设置表格等宽
        self.ui.table.horizontalHeader().setStyleSheet("QHeaderView::section{background:skyblue;}")

        self.ui.pushButton_sw.clicked.connect(self.Display)  # 16:显示
        self.ui.pushButton_add.clicked.connect(self.Add)  # 16:增
        self.ui.pushButton_del.clicked.connect(self.Delete)  # 17：删
        self.ui.pushButton_che.clicked.connect(self.Check)  # 28: 查

        self.parent = parent

    def Display(self):  # 显示
        self.renderTable()

    def Add(self):  # 增
        name = self.ui.lineEdit_BN.text()
        ID = self.ui.lineEdit_ID.text()
        money = self.ui.lineEdit_money.text()
        time_open = self.ui.lineEdit_date.text()
        if ID == '' or name == '' or money == '':
            self.error_input('输入信息不足!')
            return

        ID_card = self.ui.lineEdit_ID_card.text()
        if ID_card == '':
            self.error_input('输入信息不足!')
            return

        ID_card = StringPre(ID_card)

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

        name = StringPre(name)  # 预处理，应对特殊字符

        self.query = 'insert into ' + self.tabName_L + ' value(' + IsString(name) + ', ' + \
                     IsString(ID, False) + ', ' + IsString(money, False) + ', ' + IsString(time_open) + ');'

        self.query_hold = 'insert into ' + self.tabName + ' value(' + IsString(name) + ', ' + \
                     IsString(ID, False) + ', ' + IsString(ID_card) + ');'

        print("query: ", self.query)
        print(self.query_hold)
        self.get_query_add(self.query, self.query_hold, True)
        self.renderTable()

    def Delete(self):  # 删，一次只能删除一条贷款记录
        # 确认删除
        name = self.ui.lineEdit_BN.text()
        ID = self.ui.lineEdit_ID.text()
        money = self.ui.lineEdit_money.text()
        time_open = self.ui.lineEdit_date.text()

        ID_card = self.ui.lineEdit_ID_card.text()

        ID_card = StringPre(ID_card)

        if name == '':
            self.error_input('未指定要删除的贷款的分行名称!')
            return

        if ID == '':
            self.error_input('未指定要删除的贷款的贷款号!')
            return

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

        reply = QMessageBox.question(self, '确认', "确定执行操作?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return

        name = StringPre(name)  # 预处理，应对特殊字符

        self.query = "select money_loan from Loans where " + ISEmpty('name', name) + ' and ' \
                     + ISEmpty('ID_loan', ID, False) + ';'  # 统计特定贷款总共需要支付多少钱

        record = db_check(self.parent.db, self.query)

        if len(record) == 0:
            self.error_input('没有相关的贷款!')
            return

        total_money = record[0][0]  # 该贷款单总共需要付的前, record里的每个元素为 tuple 类型

        self.query = "select money_pay from payout where " + ISEmpty('name', name) + ' and ' \
                     + ISEmpty('ID_loan', ID) + ';'  # 统计特定贷款已经支付了多少钱.

        pay = db_total_money(self.parent.db, self.query)

        if 0 < pay < total_money:  # 还未发完
            self.error_input('此贷款正在发放中,不允许删除!')
            return

        self.query_pay = 'delete from payout where ' + ISEmpty('name', name) + ' and ' + ISEmpty('ID_loan', ID, False) + ';'

        self.query = 'delete from ' + self.tabName_L + ' where ' + ISEmpty('name', name) + ' and ' \
                         + ISEmpty('ID_loan', ID, False) + ' and ' + ISEmpty('money_loan', money, False) +\
                         ' and ' + ISEmpty('TIME_open', time_open) + ';'

        self.query_hold = 'delete from ' + self.tabName + ' where ' + ISEmpty('name', name) + ' and ' \
                     + ISEmpty('ID_loan', ID, False) + ' and ' + ISEmpty('ID_card', ID_card) + ';'

        self.get_query_delete(self.query_pay, self.query, self.query_hold, pay, total_money, True)
        self.renderTable()

    def Check(self):
        name = self.ui.lineEdit_BN.text()
        ID = self.ui.lineEdit_ID.text()
        money = self.ui.lineEdit_money.text()
        time_open = self.ui.lineEdit_date.text()

        ID_card = self.ui.lineEdit_ID_card.text()

        ID_card = StringPre(ID_card)

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

        name = StringPre(name)  # 预处理，应对特殊字符

        self.query = 'select * from ' + self.tabName_L + ', ' + self.tabName + ' where Loans.name = Hold_C_L.name and Loans.ID_loan = Hold_C_L.ID_loan and '\
                     + ISEmpty('Loans.name', name) + ' and ' \
                     + ISEmpty('Loans.ID_loan', ID, False) + ' and ' + ISEmpty('money_loan', money, False) +\
                     ' and ' + ISEmpty('TIME_open', time_open) +  ' and ' + ISEmpty('ID_card', ID_card) + ';'
        print("query: ", self.query)
        items = db_check(self.parent.db, self.query)
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
            money = QTableWidgetItem(str(record[2]))
            money.setTextAlignment(QtCore.Qt.AlignCenter)
            time_open = QTableWidgetItem(str(record[3]))
            time_open.setTextAlignment(QtCore.Qt.AlignCenter)

            ID_card = QTableWidgetItem(str(record[6]))
            ID_card.setTextAlignment(QtCore.Qt.AlignCenter)

            self.query = "select money_pay from payout where " + ISEmpty('name', record[0]) + ' and ' \
                         + 'ID_loan = ' + str(record[1]) + ';'  # 统计特定贷款已经支付了多少钱.

            pay = db_total_money(self.parent.db, self.query)

            if pay == 0:  # 已发为0
                state = '未开始发放'
            elif pay < record[2]:  # 还未发完
                state = '发放中'
            else:
                state = '已全部发放'

            stateitem = QTableWidgetItem(state)
            stateitem.setTextAlignment(QtCore.Qt.AlignCenter)

            self.ui.table.setItem(currentRowCount, 0, name)  # 列1
            self.ui.table.setItem(currentRowCount, 1, ID)  # 列2
            self.ui.table.setItem(currentRowCount, 2, money)  # 列3
            self.ui.table.setItem(currentRowCount, 3, time_open)  # 列4
            self.ui.table.setItem(currentRowCount, 4, stateitem)  # 列5
            self.ui.table.setItem(currentRowCount, 5, ID_card)  # 列6
            currentRowCount += 1
            self.ui.table.setRowCount(currentRowCount)

    def renderTable(self):
        self.ui.table.setRowCount(0)
        query = 'select * from ' + self.tabName_L + ', ' + self.tabName +' where Loans.name = Hold_C_L.name and Loans.ID_loan = Hold_C_L.ID_loan;'
        print(query)
        # tab = db_show(self.parent.db, T)
        tab = db_check(self.parent.db, query)
        currentRowCount = self.ui.table.rowCount()

        for record in tab:
            print(record)
            self.ui.table.insertRow(currentRowCount)
            name = QTableWidgetItem(str(record[0]))  # 支行名字
            name.setTextAlignment(QtCore.Qt.AlignCenter)
            ID = QTableWidgetItem(str(record[1]))  # 贷款号
            ID.setTextAlignment(QtCore.Qt.AlignCenter)
            money = QTableWidgetItem(str(record[2]))
            money.setTextAlignment(QtCore.Qt.AlignCenter)
            time_open = QTableWidgetItem(str(record[3]))
            time_open.setTextAlignment(QtCore.Qt.AlignCenter)

            ID_card = QTableWidgetItem(str(record[6]))
            ID_card.setTextAlignment(QtCore.Qt.AlignCenter)

            self.query = "select money_pay from payout where " + ISEmpty('name', record[0]) + ' and ' \
                         + 'ID_loan = ' + str(record[1]) + ';'  # 统计特定贷款已经支付了多少钱.
            pay = db_total_money(self.parent.db, self.query)

            if pay == 0:        # 已发为0
                state = '未开始发放'
            elif pay < record[2]:    # 还未发完
                state = '发放中'
            else:
                state = '已全部发放'

            stateitem = QTableWidgetItem(state)
            stateitem.setTextAlignment(QtCore.Qt.AlignCenter)

            self.ui.table.setItem(currentRowCount, 0, name)  # 列1
            self.ui.table.setItem(currentRowCount, 1, ID)  # 列2
            self.ui.table.setItem(currentRowCount, 2, money)  # 列3
            self.ui.table.setItem(currentRowCount, 3, time_open)  # 列4
            self.ui.table.setItem(currentRowCount, 4, stateitem)  # 列5
            self.ui.table.setItem(currentRowCount, 5, ID_card)  # 列6
            currentRowCount += 1
            self.ui.table.setRowCount(currentRowCount)

    def get_query_add(self, Q1, Q2, need_fetch):
        result = []
        # print(self.db)
        cursor = self.parent.db.cursor()  ########################
        try:
            cursor.execute(Q1)
            cursor.execute(Q2)  # Hold
        except:
            self.error_input('SQL query denied, please check your input!')
            return
        if need_fetch:
            result = cursor.fetchall()
        self.parent.db.commit()
        cursor.close()
        return result

    def get_query_delete(self, Q1, Q2, Q3, pay, total, need_fetch):
        result = []
        # print(self.db)
        cursor = self.parent.db.cursor()  ########################
        try:
            if pay >= total:
                cursor.execute(Q1)  # 清除支付情况
            cursor.execute(Q3)      # Hold
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

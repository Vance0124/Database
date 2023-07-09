from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView
from PyQt5 import QtCore
from Count.CountUI.LoancountInf import Ui_Loancount
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
    return SS


class Loancount(QDialog):
    "A dialog class for Ui_LoginDialog, who can show itself"

    def __init__(self, parent):
        super(Loancount, self).__init__(parent)
        # self.tabName = 'Contacts'
        self.ui = Ui_Loancount()
        self.ui.setupUi(self)
        self.ui.table.setColumnCount(3)  # 不设置不显示这些列
        self.ui.table.setHorizontalHeaderLabels(['分行名称', '用户数', '贷款总金额'])
        self.ui.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 设置表格等宽
        self.ui.table.horizontalHeader().setStyleSheet("QHeaderView::section{background:skyblue;}")

        self.ui.pushButton_che.clicked.connect(self.Check)  # 28: 查

        self.parent = parent

    def Display(self):  # 显示所有
        self.renderTable(self.tabName)

    def Check(self):
        timelow = self.ui.dateEdit_1.date().toString("yyyy/MM/dd")  # 时间下限
        timeup = self.ui.dateEdit_2.date().toString("yyyy/MM/dd")   # 时间上限
        time_interval = 'Loans.TIME_open >= str_to_date(' + IsString(timelow) + ', ' + IsString('%Y/%m/%d') + ')' \
                        + ' and Loans.TIME_open <= str_to_date(' + IsString(timeup) + ', ' + IsString('%Y/%m/%d') + ')'
        self.query = 'select bank.name,  COUNT(*), SUM(money_loan) from bank, Loans, Hold_C_L ' \
                     'where bank.name = Loans.name and bank.name = Hold_C_L.name and Loans.ID_loan = Hold_C_L.ID_loan'\
                     + ' and ' + time_interval + ' group by bank.name;'
        query_result = self.get_query(True)
        self.CheckShow(query_result)

    def CheckShow(self, Items):
        self.ui.table.setRowCount(0)
        currentRowCount = self.ui.table.rowCount()

        for record in Items:
            self.ui.table.insertRow(currentRowCount)
            name = QTableWidgetItem(str(record[0]))
            name.setTextAlignment(QtCore.Qt.AlignCenter)
            people = QTableWidgetItem(str(record[1]))
            people.setTextAlignment(QtCore.Qt.AlignCenter)
            money = QTableWidgetItem(str(record[2]))
            money.setTextAlignment(QtCore.Qt.AlignCenter)

            self.ui.table.setItem(currentRowCount, 0, name)  # 列1
            self.ui.table.setItem(currentRowCount, 1, people)  # 列2
            self.ui.table.setItem(currentRowCount, 2, money)  # 列3
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
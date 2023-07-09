from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView
from PyQt5 import QtCore
from Hold.HoldUI.HoldInf import Ui_Hold
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
    return SS


class Hold(QDialog):
    "A dialog class for Ui_LoginDialog, who can show itself"

    def __init__(self, parent):
        super(Hold, self).__init__(parent)
        self.tabName = 'Hold_C_L'
        self.ui = Ui_Hold()
        self.ui.setupUi(self)
        self.ui.table.setColumnCount(3)  # 不设置不显示这些列
        self.ui.table.setHorizontalHeaderLabels(['支行名字', '贷款号', '客户身份证号'])
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
        ID_card = self.ui.lineEdit_ID_card.text()
        if ID == '' or name == '' or ID_card == '':
            self.error_input('输入信息不足!')
            return

        name = StringPre(name)  # 预处理，应对特殊字符
        ID_card = StringPre(ID_card)

        self.query = 'insert into ' + self.tabName + ' value(' + IsString(name) + ', ' + \
                     IsString(ID, False) + ', ' + IsString(ID_card) + ');'
        print("query: ", self.query)
        self.get_query(True)
        self.renderTable(self.tabName)

    def Delete(self):  # 删，一次只能删除一条贷款记录
        # 确认删除
        name = self.ui.lineEdit_BN.text()
        ID = self.ui.lineEdit_ID.text()
        ID_card = self.ui.lineEdit_ID_card.text()

        reply = QMessageBox.question(self, '确认', "确定执行操作?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return

        name = StringPre(name)  # 预处理，应对特殊字符
        ID_card = StringPre(ID_card)

        self.query = 'delete from ' + self.tabName + ' where ' + ISEmpty('name', name) + ' and ' \
                     + ISEmpty('ID_loan', ID, False) + ' and ' + ISEmpty('ID_card', ID_card) + ';'
        self.get_query(True)
        self.renderTable(self.tabName)

    def Check(self):
        name = self.ui.lineEdit_BN.text()
        ID = self.ui.lineEdit_ID.text()
        ID_card = self.ui.lineEdit_ID_card.text()

        name = StringPre(name)  # 预处理，应对特殊字符

        self.query = 'select * from ' + self.tabName + ' where ' + ISEmpty('name', name) + ' and ' \
                     + ISEmpty('ID_loan', ID, False) + ' and ' + ISEmpty('ID_card', ID_card) + ';'
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
            ID_card = QTableWidgetItem(str(record[2]))
            ID_card.setTextAlignment(QtCore.Qt.AlignCenter)

            self.ui.table.setItem(currentRowCount, 0, name)  # 列1
            self.ui.table.setItem(currentRowCount, 1, ID)  # 列2
            self.ui.table.setItem(currentRowCount, 2, ID_card)  # 列3
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
            ID_card = QTableWidgetItem(str(record[2]))
            ID_card.setTextAlignment(QtCore.Qt.AlignCenter)

            self.ui.table.setItem(currentRowCount, 0, name)  # 列1
            self.ui.table.setItem(currentRowCount, 1, ID)  # 列2
            self.ui.table.setItem(currentRowCount, 2, ID_card)  # 列3
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

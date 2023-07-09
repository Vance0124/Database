from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView
from PyQt5 import QtCore
from Transact.TransactUI.TransactInf import Ui_Transact
from Transact.TransactUpdate import TransactUpdate
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


class Transact(QDialog):
    "A dialog class for Ui_LoginDialog, who can show itself"

    def __init__(self, parent):
        super(Transact, self).__init__(parent)
        self.tabName = 'Transact'
        self.ui = Ui_Transact()
        self.ui.setupUi(self)
        self.ui.table.setColumnCount(4)  # 不设置不显示这些列
        self.ui.table.setHorizontalHeaderLabels(['支行名字', '身份证号', '账户类型', '账户号'])
        self.ui.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 设置表格等宽
        self.ui.table.horizontalHeader().setStyleSheet("QHeaderView::section{background:skyblue;}")

        self.ui.pushButton_sw.clicked.connect(self.Display)  # 16:显示
        self.ui.pushButton_add.clicked.connect(self.Add)  # 16:增
        self.ui.pushButton_del.clicked.connect(self.Delete)  # 17：删
        self.ui.pushButton_upda.clicked.connect(self.Update)  # 27：改
        self.ui.pushButton_che.clicked.connect(self.Check)  # 28: 查

        self.parent = parent

    def Display(self):  # 显示
        self.renderTable(self.tabName)

    def Add(self):  # 增
        name = self.ui.lineEdit_BN.text()
        ID_card = self.ui.lineEdit_ID_card.text()
        acctype = self.ui.lineEdit_type.text()
        accID = self.ui.lineEdit_ID.text()
        if ID_card == '' or name == '' or acctype == '' or accID == '':
            self.error_input('输入信息不足!')
            return
        if len(ID_card) != 18:
            self.error_input('客户身份证号输入位数不正确！')
            return
        if acctype != '0' and acctype != '1':
            self.error_input('账户类型输入不正确！(有效值：0 | 1)')
            return

        name = StringPre(name)  # 预处理，应对特殊字符

        self.query = 'insert into ' + self.tabName + ' value(' + IsString(name) + ', ' + \
                     IsString(ID_card) + ', ' + IsString(acctype, False) + ', ' + IsString(accID, False) + ');'
        print("query: ", self.query)
        self.get_query(True)
        self.renderTable(self.tabName)

    def Delete(self):  # 增
        # 确认删除
        reply = QMessageBox.question(self, '确认', "确定执行操作?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return

        name = self.ui.lineEdit_BN.text()
        ID_card = self.ui.lineEdit_ID_card.text()
        acctype = self.ui.lineEdit_type.text()
        accID = self.ui.lineEdit_ID.text()

        name = StringPre(name)  # 预处理，应对特殊字符
        self.query = 'delete from ' + self.tabName + ' where ' + ISEmpty('name', name) + ' and '\
                     + ISEmpty('ID_card', ID_card) + ' and ' + ISEmpty('Type', acctype, False) + ' and ' \
                     + ISEmpty('ID', accID, False) + ';'
        print("query  : ", self.query)
        self.get_query(True)
        self.renderTable(self.tabName)

    def Update(self):
        upda = TransactUpdate(self)
        upda.exec_()
        self.renderTable(self.tabName)

    def Check(self):
        name = self.ui.lineEdit_BN.text()
        ID_card = self.ui.lineEdit_ID_card.text()
        acctype = self.ui.lineEdit_type.text()
        accID = self.ui.lineEdit_ID.text()

        name = StringPre(name)  # 预处理，应对特殊字符

        self.query = 'select * from ' + self.tabName + ' where ' + ISEmpty('name', name) + ' and '\
                     + ISEmpty('ID_card', ID_card) + ' and ' + ISEmpty('Type', acctype, False) + ' and ' \
                     + ISEmpty('ID', accID, False) + ';'
        print("query: ", self.query)
        items = db_check(self.parent.db, self.query)
        self.CheckShow(items)

    def CheckShow(self, Items):
        self.ui.table.setRowCount(0)
        currentRowCount = self.ui.table.rowCount()

        for record in Items:
            self.ui.table.insertRow(currentRowCount)
            name = QTableWidgetItem(str(record[0]))
            name.setTextAlignment(QtCore.Qt.AlignCenter)
            ID_card = QTableWidgetItem(str(record[1]))
            ID_card.setTextAlignment(QtCore.Qt.AlignCenter)
            acctype = QTableWidgetItem(str(record[2]))
            acctype.setTextAlignment(QtCore.Qt.AlignCenter)
            accID = QTableWidgetItem(str(record[3]))
            accID.setTextAlignment(QtCore.Qt.AlignCenter)

            self.ui.table.setItem(currentRowCount, 0, name)  # 列1
            self.ui.table.setItem(currentRowCount, 1, ID_card)  # 列2
            self.ui.table.setItem(currentRowCount, 2, acctype)  # 列3
            self.ui.table.setItem(currentRowCount, 3, accID)  # 列4
            currentRowCount += 1
            self.ui.table.setRowCount(currentRowCount)

    def renderTable(self, T):
        self.ui.table.setRowCount(0)
        tab = db_show(self.parent.db, T)
        currentRowCount = self.ui.table.rowCount()

        for record in tab:
            self.ui.table.insertRow(currentRowCount)
            name = QTableWidgetItem(str(record[0]))
            name.setTextAlignment(QtCore.Qt.AlignCenter)
            ID_card = QTableWidgetItem(str(record[1]))
            ID_card.setTextAlignment(QtCore.Qt.AlignCenter)
            acctype = QTableWidgetItem(str(record[2]))
            acctype.setTextAlignment(QtCore.Qt.AlignCenter)
            accID = QTableWidgetItem(str(record[3]))
            accID.setTextAlignment(QtCore.Qt.AlignCenter)

            self.ui.table.setItem(currentRowCount, 0, name)  # 列1
            self.ui.table.setItem(currentRowCount, 1, ID_card)  # 列2
            self.ui.table.setItem(currentRowCount, 2, acctype)  # 列3
            self.ui.table.setItem(currentRowCount, 3, accID)  # 列4
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
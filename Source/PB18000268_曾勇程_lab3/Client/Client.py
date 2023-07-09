from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView
from PyQt5 import QtCore
from Client.ClientUI.ClientInf import Ui_ClientChange
from Client.CliUpdate import ClientUpdate
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


class ClientChange(QDialog):
    "A dialog class for Ui_LoginDialog, who can show itself"

    def __init__(self, parent):
        super(ClientChange, self).__init__(parent)
        self.tabName = 'client'
        self.ui = Ui_ClientChange()
        self.ui.setupUi(self)
        self.ui.table.setColumnCount(6)  # 不设置不显示这些列
        self.ui.table.setHorizontalHeaderLabels(['ID', 'Clerk ID', 'name', 'telephone', 'address', 'Clerk Type'])
        self.ui.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 设置表格等宽
        self.ui.table.horizontalHeader().setStyleSheet("QHeaderView::section{background:skyblue;}")

        self.ui.pushButton.clicked.connect(self.Display)  # 16:增
        self.ui.pushButton_16.clicked.connect(self.Add)  # 16:增
        self.ui.pushButton_17.clicked.connect(self.Delete)  # 17：删
        self.ui.pushButton_27.clicked.connect(self.Update)  # 27：改
        self.ui.pushButton_28.clicked.connect(self.Check)  # 28: 查

        self.parent = parent

    def Display(self):  # 显示
        self.renderTable(self.tabName)

    def Add(self):  # 增
        ID = self.ui.lineEdit_10.text()
        clerk_ID = self.ui.lineEdit_16.text()
        name = self.ui.lineEdit_12.text()
        telephone = self.ui.lineEdit_11.text()
        address = self.ui.lineEdit_15.text()
        clerk_type = self.ui.lineEdit_14.text()
        # 首先进行错误检查
        if ID == '' or clerk_ID == '' or name == '' or telephone == '' or address == '' or clerk_type == '':
            self.error_input('输入信息不足!')
            return
        if len(ID) != 18:
            self.error_input('客户身份证号输入位数不正确！')
            return
        if len(clerk_ID) != 18:
            self.error_input('银行职员身份证号输入位数不正确！')
            return
        if len(telephone) != 11:
            self.error_input('电话输入位数不正确！')
            return
        if clerk_type != '0' and clerk_type != '1':
            self.error_input('银行职员类型不正确！')
            return

        name = StringPre(name)  # 预处理，应对特殊字符
        address = StringPre(address)

        self.query = 'insert into ' + self.tabName + ' value(' + IsString(ID) + ', ' + IsString(clerk_ID) + ', ' + \
                     IsString(name) + ', ' + IsString(telephone, False) + ', ' + IsString(address) + ', ' \
                     + IsString(clerk_type, False) + ');'
        print(self.query)
        self.get_query(True)
        self.renderTable(self.tabName)

    def Delete(self):  # 增
        # 确认删除
        reply = QMessageBox.question(self, '确认', "确定执行操作?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return

        ID = self.ui.lineEdit_10.text()
        clerk_ID = self.ui.lineEdit_16.text()
        name = self.ui.lineEdit_12.text()
        telephone = self.ui.lineEdit_11.text()
        address = self.ui.lineEdit_15.text()
        clerk_type = self.ui.lineEdit_14.text()

        name = StringPre(name)  # 预处理，应对特殊字符
        address = StringPre(address)

        self.query = 'delete from ' + self.tabName + ' where ' + ISEmpty('ID_card', ID) + ' and ' \
                     + ISEmpty('cle_ID_card', clerk_ID) + ' and ' + ISEmpty('name', name) + ' and ' + \
                     ISEmpty('telephone', telephone, False) + ' and ' + ISEmpty('address', address) \
                     + ' and ' + ISEmpty('clerk_type', clerk_type, False) + ';'
        self.get_query(True)
        self.renderTable(self.tabName)

    def Update(self):
        upda = ClientUpdate(self)
        upda.exec_()
        self.renderTable(self.tabName)

    def Check(self):
        ID = self.ui.lineEdit_10.text()
        clerk_ID = self.ui.lineEdit_16.text()
        name = self.ui.lineEdit_12.text()
        telephone = self.ui.lineEdit_11.text()
        address = self.ui.lineEdit_15.text()
        clerk_type = self.ui.lineEdit_14.text()

        name = StringPre(name)  # 预处理，应对特殊字符
        address = StringPre(address)

        self.query = 'select * from ' + self.tabName + ' where ' + ISEmpty('ID_card', ID) + ' and ' \
                     + ISEmpty('cle_ID_card', clerk_ID) + ' and ' + ISEmpty('name', name) + ' and ' + \
                     ISEmpty('telephone', telephone, False) + ' and ' + ISEmpty('address', address) \
                     + ' and ' + ISEmpty('clerk_type', clerk_type, False) + ';'
        print(self.query)
        items = db_check(self.parent.db, self.query)
        self.CheckShow(items)

    def CheckShow(self, Items):
        self.ui.table.setRowCount(0)
        currentRowCount = self.ui.table.rowCount()

        for record in Items:
            self.ui.table.insertRow(currentRowCount)
            ID = QTableWidgetItem(str(record[0]))
            ID.setTextAlignment(QtCore.Qt.AlignCenter)
            cle_ID = QTableWidgetItem(str(record[1]))
            cle_ID.setTextAlignment(QtCore.Qt.AlignCenter)
            name = QTableWidgetItem(str(record[2]))
            name.setTextAlignment(QtCore.Qt.AlignCenter)
            tele = QTableWidgetItem(str(record[3]))
            tele.setTextAlignment(QtCore.Qt.AlignCenter)
            address = QTableWidgetItem(str(record[4]))
            address.setTextAlignment(QtCore.Qt.AlignCenter)
            type = QTableWidgetItem(str(record[5]))
            type.setTextAlignment(QtCore.Qt.AlignCenter)

            self.ui.table.setItem(currentRowCount, 0, ID)  # 列1
            self.ui.table.setItem(currentRowCount, 1, cle_ID)  # 列2
            self.ui.table.setItem(currentRowCount, 2, name)  # 列3
            self.ui.table.setItem(currentRowCount, 3, tele)  # 列4
            self.ui.table.setItem(currentRowCount, 4, address)  # 列5
            self.ui.table.setItem(currentRowCount, 5, type)  # 列6
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
            cle_ID = QTableWidgetItem(str(record[1]))
            cle_ID.setTextAlignment(QtCore.Qt.AlignCenter)
            name = QTableWidgetItem(str(record[2]))
            name.setTextAlignment(QtCore.Qt.AlignCenter)
            tele = QTableWidgetItem(str(record[3]))
            tele.setTextAlignment(QtCore.Qt.AlignCenter)
            address = QTableWidgetItem(str(record[4]))
            address.setTextAlignment(QtCore.Qt.AlignCenter)
            type = QTableWidgetItem(str(record[5]))
            type.setTextAlignment(QtCore.Qt.AlignCenter)

            self.ui.table.setItem(currentRowCount, 0, ID)  # 列1
            self.ui.table.setItem(currentRowCount, 1, cle_ID)  # 列2
            self.ui.table.setItem(currentRowCount, 2, name)  # 列3
            self.ui.table.setItem(currentRowCount, 3, tele)  # 列4
            self.ui.table.setItem(currentRowCount, 4, address)  # 列5
            self.ui.table.setItem(currentRowCount, 5, type)  # 列6
            currentRowCount += 1
            self.ui.table.setRowCount(currentRowCount)

    def get_query(self, need_fetch):
        # print(self.query)
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

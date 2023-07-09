from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView
from PyQt5 import QtCore
from Contact.ContactUI.ContactInf import Ui_Contact
from Contact.ConUpdate import ContactUpdate
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


class Contact(QDialog):
    "A dialog class for Ui_LoginDialog, who can show itself"

    def __init__(self, parent):
        super(Contact, self).__init__(parent)
        self.tabName = 'Contacts'
        self.ui = Ui_Contact()
        self.ui.setupUi(self)
        self.ui.table.setColumnCount(5)  # 不设置不显示这些列
        self.ui.table.setHorizontalHeaderLabels(['ID_card', 'name', 'telephone', 'Email', 'relation'])
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
        ID = self.ui.lineEdit_ID.text()
        name = self.ui.lineEdit_Name.text()
        telephone = self.ui.lineEdit_Tele.text()
        Email = self.ui.lineEdit_Ema.text()
        relation = self.ui.lineEdit_Rel.text()
        if ID == '' or name == '' or telephone == '' or Email == '' or relation == '':
            self.error_input('输入信息不足!')
            return
        if len(ID) != 18:
            self.error_input('客户身份证号输入位数不正确！')
            return
        if len(telephone) != 11:
            self.error_input('电话输入位数不正确！')
            return
        if '@' not in Email:    # Email 格式错误
            self.error_input('Email格式不正确！')
            return

        name = StringPre(name)  # 预处理，应对特殊字符
        Email = StringPre(Email)
        relation = StringPre(relation)

        self.query = 'insert into ' + self.tabName + ' value(' + IsString(ID) + ', ' + \
                     IsString(name) + ', ' + IsString(telephone, False) + ', ' + IsString(Email) + ', ' \
                     + IsString(relation) + ');'
        print("query: ", self.query)
        self.get_query(True)
        self.renderTable(self.tabName)

    def Delete(self):  # 增
        # 确认删除
        reply = QMessageBox.question(self, '确认', "确定执行操作?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return

        ID = self.ui.lineEdit_ID.text()
        name = self.ui.lineEdit_Name.text()
        telephone = self.ui.lineEdit_Tele.text()
        Email = self.ui.lineEdit_Ema.text()
        relation = self.ui.lineEdit_Rel.text()

        name = StringPre(name)  # 预处理，应对特殊字符
        Email = StringPre(Email)
        relation = StringPre(relation)

        self.query = 'delete from ' + self.tabName + ' where ' + ISEmpty('ID_card', ID) + ' and ' \
                     + ISEmpty('name', name) + ' and ' + \
                     ISEmpty('telephone', telephone, False) + ' and ' + ISEmpty('Email', Email) \
                     + ' and ' + ISEmpty('relation', relation) + ';'
        print("query: ", self.query)
        self.get_query(True)
        self.renderTable(self.tabName)

    def Update(self):
        upda = ContactUpdate(self)
        upda.exec_()
        self.renderTable(self.tabName)

    def Check(self):
        ID = self.ui.lineEdit_ID.text()
        name = self.ui.lineEdit_Name.text()
        telephone = self.ui.lineEdit_Tele.text()
        Email = self.ui.lineEdit_Ema.text()
        relation = self.ui.lineEdit_Rel.text()

        name = StringPre(name)  # 预处理，应对特殊字符
        Email = StringPre(Email)
        relation = StringPre(relation)

        self.query = 'select * from ' + self.tabName + ' where ' + ISEmpty('ID_card', ID) + ' and ' \
                     + ISEmpty('name', name) + ' and ' + \
                     ISEmpty('telephone', telephone, False) + ' and ' + ISEmpty('Email', Email) \
                     + ' and ' + ISEmpty('relation', relation) + ';'
        print("query: ", self.query)
        items = self.get_query(True)
        self.CheckShow(items)

    def CheckShow(self, Items):
        self.ui.table.setRowCount(0)
        currentRowCount = self.ui.table.rowCount()

        for record in Items:
            self.ui.table.insertRow(currentRowCount)
            ID = QTableWidgetItem(str(record[0]))
            ID.setTextAlignment(QtCore.Qt.AlignCenter)
            name = QTableWidgetItem(str(record[1]))
            name.setTextAlignment(QtCore.Qt.AlignCenter)
            tele = QTableWidgetItem(str(record[2]))
            tele.setTextAlignment(QtCore.Qt.AlignCenter)
            Email = QTableWidgetItem(str(record[3]))
            Email.setTextAlignment(QtCore.Qt.AlignCenter)
            relation = QTableWidgetItem(str(record[4]))
            relation.setTextAlignment(QtCore.Qt.AlignCenter)

            self.ui.table.setItem(currentRowCount, 0, ID)  # 列1
            self.ui.table.setItem(currentRowCount, 1, name)  # 列2
            self.ui.table.setItem(currentRowCount, 2, tele)  # 列3
            self.ui.table.setItem(currentRowCount, 3, Email)  # 列4
            self.ui.table.setItem(currentRowCount, 4, relation)  # 列5
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
            name = QTableWidgetItem(str(record[1]))
            name.setTextAlignment(QtCore.Qt.AlignCenter)
            tele = QTableWidgetItem(str(record[2]))
            tele.setTextAlignment(QtCore.Qt.AlignCenter)
            Email = QTableWidgetItem(str(record[3]))
            Email.setTextAlignment(QtCore.Qt.AlignCenter)
            relation = QTableWidgetItem(str(record[4]))
            relation.setTextAlignment(QtCore.Qt.AlignCenter)

            self.ui.table.setItem(currentRowCount, 0, ID)  # 列1
            self.ui.table.setItem(currentRowCount, 1, name)  # 列2
            self.ui.table.setItem(currentRowCount, 2, tele)  # 列3
            self.ui.table.setItem(currentRowCount, 3, Email)  # 列4
            self.ui.table.setItem(currentRowCount, 4, relation)  # 列5
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
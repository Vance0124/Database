from PyQt5.QtWidgets import QApplication 
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView
from PyQt5 import QtCore
from UI.ui_table import Ui_TablePage
from login import LoginDialog
from db import *
#########################################################
from Client.Client import ClientChange      # 客户
from Contact.Contact import Contact         # 联系人
from Account.SVAccount import SVAccount     # 储蓄账户
from Account.CKAccount import CKAccount     # 支票账户
from Account.Account import Account         # 账户汇总
from Transact.Transact import Transact      # 账户所属信息
from Loan.Loan import Loan                  # 贷款信息
from Loan.payout import payout              # 支付情况
from Hold.Hold import Hold                  # 贷款持有信息
from Count.SVcount import SVcount as SV           # 储蓄类业务统计
from Count.Loancount import Loancount as LOA          # 贷款类业务统计

debug = True

class MainWindow(QMainWindow):
    " The Entrance of the Main window"
    def __init__(self):
        super().__init__()
        # 主窗口需要有一个UI界面，我们使用TablePage作为主窗口显示的UI界面
        self.ui = Ui_TablePage()
        self.ui.setupUi(self)

        # 初始化配置
        self.initLayout()
        self.initBinding()
        
        self.show()

        if debug:
            self.db = db_login("lyp1234", "1234", "127.0.0.1", "lab2")
            self.dbname = "lab2"
            self.ui.ClearBtn.setEnabled(True)
            self.ui.SearchBtn.setEnabled(True)
        else:
            self.db = None
            self.dbname = ''

    def initLayout(self):
        # 设置主窗口UI界面的初始布局
        # self.ui.ClearBtn.setEnabled(False)
        # self.ui.SearchBtn.setEnabled(False)
        # self.ui.Connect2.setEnabled(False)
        # self.ui.ConAccount.setEnabled(False)
        # self.ui.MLoan.setEnabled(False)
        # self.ui.count.setEnabled(False)
        # self.ui.title.setText("All Tables for Database - ")
        self.ui.table.setColumnCount(2)     # 不设置不显示这些列
        self.ui.table.setHorizontalHeaderLabels(['Table Name', 'Row Count'])
        self.ui.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #设置表格等宽
        self.ui.table.horizontalHeader().setStyleSheet("QHeaderView::section{background:skyblue;}")
    
    def initBinding(self):
        # 将主界面按钮点击动作绑定到函数
        self.ui.ClearBtn.clicked.connect(self.clearTable)

        self.ui.SearchBtn.clicked.connect(self.renderTable)

        # 将菜单点击动作绑定到函数
        self.ui.actionLogin.triggered.connect(self.Login)

        self.ui.actionLogout.triggered.connect(self.LogOut)

        self.ui.Client.triggered.connect(self.ClientCh)      # 顾客
        self.ui.Contacts.triggered.connect(self.Contacts)     # 顾客的联系人
        self.ui.SVAcc.triggered.connect(self.SVAccClick)    # 储蓄账户
        self.ui.CKAcc.triggered.connect(self.CKAccClick)    # 支票账户
        self.ui.Acc.triggered.connect(self.AccClick)        # 账户汇总
        # self.ui.Tran.triggered.connect(self.TranClick)      # 账户所属信息
        self.ui.Loan.triggered.connect(self.LoanClick)      # 贷款信息
        self.ui.pay.triggered.connect(self.PayClick)       # 贷款信息
        self.ui.hold.triggered.connect(self.HoldClick)       # 贷款持有信息
        self.ui.SVcount.triggered.connect(self.SVcountClick)    # 储蓄类业务
        self.ui.Loancount.triggered.connect(self.LoancountClick)    # 贷款类业务

    # all the function to bind with
    def clearTable(self):
        self.ui.table.setRowCount(0)

    def renderTable(self):
        self.ui.table.setRowCount(0)

        tabs = db_showtable(self.db)

        currentRowCount = self.ui.table.rowCount()
        # print(currentRowCount)
        for tab in tabs:
            self.ui.table.insertRow(currentRowCount)
            item0 = QTableWidgetItem(str(tab[0]))
            item0.setTextAlignment(QtCore.Qt.AlignCenter)
            item1 = QTableWidgetItem(str(tab[1]))
            item1.setTextAlignment(QtCore.Qt.AlignCenter)

            self.ui.table.setItem(currentRowCount, 0, item0) #列1
            self.ui.table.setItem(currentRowCount, 1, item1) #列2
            currentRowCount += 1
            self.ui.table.setRowCount(currentRowCount)

    def Login(self):
        dialog = LoginDialog(self)
        dialog.exec_()

        if self.db != None:
            self.ui.ClearBtn.setEnabled(True)
            self.ui.SearchBtn.setEnabled(True)
            self.ui.Connect2.setEnabled(True)
            self.ui.ConAccount.setEnabled(True)
            self.ui.MLoan.setEnabled(True)
            self.ui.count.setEnabled(True)
            # self.ui.title.setText("All Tables for Database - " + self.dbname)
            self.renderTable()

    def LogOut(self):
        db_close(self.db)
        self.db = None
        self.dbname = ''
        self.ui.ClearBtn.setEnabled(False)
        self.ui.SearchBtn.setEnabled(False)
        self.clearTable()
###################################################################3

    def ClientCh(self):
        cli = ClientChange(self)
        cli.exec_()

    def Contacts(self):
        con = Contact(self)
        con.exec_()

    def SVAccClick(self):
        SVAcc = SVAccount(self)
        SVAcc.exec_()

    def CKAccClick(self):
        CKAcc = CKAccount(self)
        CKAcc.exec_()

    def AccClick(self):
        Acc = Account(self)
        Acc.exec_()

    def TranClick(self):
        Tran = Transact(self)
        Tran.exec_()

    def LoanClick(self):
        L = Loan(self)
        L.exec_()

    def PayClick(self):
        pay = payout(self)
        pay.exec_()

    def HoldClick(self):
        hold = Hold(self)
        hold.exec_()

    def SVcountClick(self):
        s = SV(self)
        s.exec_()

    def LoancountClick(self):
        L = LOA(self)
        L.exec_()

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    
    w = MainWindow()

    sys.exit(app.exec_())
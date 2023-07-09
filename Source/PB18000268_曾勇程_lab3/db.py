import MySQLdb
from MySQLdb._exceptions import OperationalError


def db_login(user, passwd, server_addr, dbname):
    try:
        db = MySQLdb.connect(server_addr, user, passwd, dbname, charset = "utf8")
    except OperationalError:
        db = None

    return db


def db_showtable(db):
    cursor = db.cursor()

    cursor.execute("show tables")
    tabs = cursor.fetchall()    # 获取所有记录
    res = list()

    for tab in tabs:
        cursor.execute("select count(*) from " + tab[0])
        row_cnt = cursor.fetchone()

        res.append((tab[0], row_cnt[0]))
    cursor.close()

    return res


def db_show(db, T):       # 显示一个表
    cursor = db.cursor()
    cursor.execute("select * from " + T)
    row = cursor.fetchall()
    cursor.close()
    # print(row)
    return row


def db_check(db, query):        # 仅做查询用，不能用于修改数据库，修改数据库请用 get_query函数
    cursor = db.cursor()
    cursor.execute(query)
    row = cursor.fetchall()
    cursor.close()
    return row


def db_total_money(db, query):    # 用于查询支付情况中指定贷款发放了多少钱
    cursor = db.cursor()
    cursor.execute(query)
    row = cursor.fetchall()
    cursor.close()
    money = 0
    for i in row:       # i 是元组类型
        money += i[0]
    # print(row)
    return money


def db_close(db):
    if db is not None:
        db.close()

if __name__ == "__main__":
    db = db_login("lyp1234", "1234", "127.0.0.1", "test")

    tabs = db_showtable(db)

    db_close(db)
import pymysql


def get_list(sql):
    conn = pymysql.connect(host='localhost',
                           port=3306,
                           user='root',
                           password='root',
                           db='edu_adm_sys',
                           charset='GBK'
                           )
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def modify(sql):
    conn = pymysql.connect(host='localhost',
                           port=3306,
                           user='root',
                           password='root',
                           db='edu_adm_sys',
                           charset='GBK'
                           )
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


def create(sql):
    conn = pymysql.connect(host='localhost',
                           port=3306,
                           user='root',
                           password='root',
                           db='edu_adm_sys',
                           charset='GBK'
                           )
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()



def get_one(sql):
    conn = pymysql.connect(host='localhost',
                           port=3306,
                           user='root',
                           password='root',
                           db='edu_adm_sys',
                           charset='GBK'
                           )
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


class SqlHelper(object):

    def __init__(self):
        # 读取配置文件
        self.connect()

    def connect(self):
        self.conn = pymysql.connect(host='localhost',
                               port=3306,
                               user='root',
                               password='root',
                               db='edu_adm_sys',
                               charset='GBK'
                               )
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def get_list(self, sql, args):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchall()
        return result

    def get_one(self, sql, args):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchone()
        return result

    def modify(self, sql, args):
        self.cursor.execute(sql, args)
        self.conn.commit()

    def mutiple_modify(self, sql, args):
        # self.cursor.executemany('insert into bd(id,name) values(%s,%s)',[(1,'ss'),(2,'sss'),])
        # 目的：实现多条语句的操作,将后面的数据全部执行起前面的sql语句
        self.cursor.executemany(sql, args)
        self.conn.commit()

    def create(self, sql, args):
        self.cursor.execute(sql)
        self.conn.commit()
        return self.cursor.lastrowid

    def close(self):
        self.conn.close()

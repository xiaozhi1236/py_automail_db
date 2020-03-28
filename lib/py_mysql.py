import pymysql

class DBHelper:
    # 构造函数
    def __init__(self, host='localhost',port=3306, user='test',pwd='test', db='test'):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.db = db
        self.conn = pymysql.connect(host=self.host,user=self.user,passwd=self.pwd,db=self.db,port=self.port,charset='utf8')
        self.cur = self.conn.cursor()

    # 连接数据库
    def connectDatabase(self):
        try:
            self.conn = pymysql.connect(host=self.host,user=self.user,passwd=self.pwd,db=self.db,port=self.port,charset='utf8')
        except Exception as e:
            return e
        self.cur = self.conn.cursor()
        return True

    # 关闭数据库
    def close(self):
        if self.conn and self.cur:
            self.cur.close()
            self.conn.close()
        return True
    
    # 执行数据库的sq语句,主要用来做插入操作
    def execute(self, sql, params=None):
        # 连接数据库
        self.connectDatabase()
        try:
            if self.conn and self.cur:
                self.cur.execute(sql, params)
                self.conn.commit()
        except Exception as e:
            self.close()
            return e
        return True
    
    def execute_batch(self, sql_list, commit=True):
        """
        多条执行，默认提交
        """
        for sql in sql_list:
            self.cur.execute(sql)

        if commit:
            self.conn.commit()

    def make_sql_str(self,table_name, data):
        column_str = ""
        value_str = ""
        for key, value in data.items():
            column_str += '`{}`,'.format(key)
            if value or value==0:
                value_str += '"{}",'.format(str(value).replace('"', '\\"'))
            else:
                value_str += 'null,'

        value_str=value_str.replace('"nan"','null')
        column_str = column_str[:-1]
        value_str = value_str[:-1]
        sql_str = """insert into {table_name} ({column_str}) value({value_str})""".format(
            table_name=table_name,
            column_str=column_str,
            value_str=value_str
        )
        return sql_str

    # 用来查询表数据
    def fetchall(self, sql, params=None):
        self.cur.execute(sql,params)
        return self.cur.fetchall()



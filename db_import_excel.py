import datetime
import time
import os
import pandas as pd
from lib.py_mysql import DBHelper

class class_db_excel:
    '''
    用于excel文件导入到MySQL
    '''
    def __init__(self,path,file_like):
        self.path = path
        self.file_like = file_like

    # 数据写入MySQL
    def db_import_data(self,sheet_data, table_name,start):
        column_list = sheet_data.columns.values
        sql_list = []
        target_mysql = DBHelper()
        for value in sheet_data.values.tolist():
            data_item = {}
            for index in range(len(value)):
                data_item[column_list[index]] = value[index]

            if table_name in ('student','class'):
                # 字典添加自己设定元素    
                data_item["insertdate"] = start
            sql_list.append(target_mysql.make_sql_str(table_name, data_item))
        # 打印需要执行的SQL print(sql_list)
        target_mysql.execute_batch(sql_list, commit=True)

    def db_read_excel(self,start,end):
        # 字符串转换成日期
        start = datetime.datetime.strptime(start,'%Y-%m-%d')
        end = datetime.datetime.strptime(end,'%Y-%m-%d')

        while start<=end:
            print(start)

            filename=self.file_like+' '+start.strftime("%Y-%m-%d")+'.xlsx'
            file_name=self.path+filename
            insertdate=start.strftime("%Y-%m-%d")

            # 配置sheet_name与table_name的对应关系
            dict_file_table = {
                "file_name": file_name,
                "sheet_table_list": [
                    {
                        "sheet_name": "test_student",
                        "table_name": "student"
                    },
                    {
                        "sheet_name": "test_class",
                        "table_name": "class"
                    },
                ]
            }

            file_name = dict_file_table["file_name"]
            sheet_table_list = dict_file_table["sheet_table_list"]
            #print(filename)

            # 如果文件不存在则跳出 while 循环
            if os.path.exists(file_name)==False:
                break

            for item in sheet_table_list:
                table_name = item["table_name"]
                sheet_name = item["sheet_name"]

                # 判断数据库中是否有数据如果有则不重复入库
                base_mysql = DBHelper()
                columnname='insertdate'
                sql = """select count(*) as rowcount
                    from {tablename} 
                    where {columnname} = '{insertdate}';""".format(
                    tablename=table_name,
                    columnname=columnname,
                    insertdate=insertdate
                    )

                print(sql)
                is_pro = base_mysql.fetchall(sql)[0][0]
                print('is_pro:',is_pro)
                if is_pro > 0:
                    print(table_name,insertdate,'已有数据跳过本次循环')
                    continue

                sheet_data = pd.read_excel(file_name, sheet_name=sheet_name)
                print(table_name,sheet_name,file_name)
                starttime=datetime.datetime.now()
                print('开始时间：',starttime.strftime("%Y-%m-%d %H:%M:%S"))
                class_db_excel.db_import_data(self,sheet_data, table_name,start)
                endtime=datetime.datetime.now()
                print('执行时长：',str((endtime-starttime).seconds))
                    
            start= start + datetime.timedelta(days=1)



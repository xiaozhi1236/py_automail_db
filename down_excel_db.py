from download_qqmail import class_download_mail
from db_import_excel import class_db_excel
import datetime

'''
@author: liaosz
@time: 2020-03-28
@desc:

'''

# 设置参数连接邮件服务器
server='imap.qq.com'
port='993'
user='xxxxxxxxx@qq.com' # qq邮箱账号
pwd='xxxxxxxxx'  # qq邮箱登录授权码

# 设置文件名及路径
path='C:\\database\\'
file_like='mail_excel'

# 设置时间范围
startdate='2020-03-28'
enddate='2020-03-29'

# 创建下载附件的对象x
x=class_download_mail(server,port, user,pwd)
# 下载指定关键字的邮件
x.download_mail(file_like,path,startdate,enddate)

# 创建入库的对象y
y=class_db_excel(path,file_like)
# 调用类的方法
y.db_read_excel(startdate,enddate)



#-*- coding:UTF-8 -*-
import imaplib, email
import os
import datetime

class class_download_mail:
    # 构造函数-连接imap服务器
    def __init__(self, server,port, user,pwd):
        self.server = server
        self.port = port
        self.user = user
        self.pwd = pwd

        self.conn = imaplib.IMAP4_SSL(self.server,self.port)
        print('已连接服务器')
        self.conn.login(self.user,self.pwd)
        print('已登陆')

    def download_mail(self,title,path,startdate='2020-01-01',enddate='2020-01-01'):

        # 选择默认文件夹
        self.conn.select('INBOX', readonly=True) 

        # 字符串转日期
        startdate = datetime.datetime.strptime(startdate,'%Y-%m-%d')
        enddate = datetime.datetime.strptime(enddate,'%Y-%m-%d')
        # 日期转字符串
        startdate=startdate.strftime("%d-%b-%Y") 
        enddate=enddate.strftime("%d-%b-%Y") # 29-Mar-2020
        type, data = self.conn.search(None, 'SINCE '+startdate,'BEFORE '+enddate) 
        newlist=data[0].split()
        print(newlist,type,data)

        for i in range(len(newlist)):
            try:
                type, data = self.conn.fetch(newlist[i], '(RFC822)')
                # 通过email模块解析邮件
                msg = email.message_from_string(data[0][1].decode('gbk')) 
                #用get()获取标题并进行解码
                sub = msg.get('subject')
                subdecode = email.header.decode_header(sub)[0][0]
                #打印标题
                try:
                    print(subdecode.decode('utf-8'))
                except Exception as e:
                    print(subdecode.decode('gbk'))

                if title in subdecode.decode('gbk'):    
                    for part in msg.walk():
                        # 获取附件名称
                        name = part.get_param("name")
                        if name:
                            fh = email.header.Header(name)
                            fdh = email.header.decode_header(fh.encode('gbk'))                 
                            if fdh[0][1]:
                                filename = fdh[0][0].decode(fdh[0][1])
                            else:
                                filename = fdh[0][0]
                            print('附件名:',filename)

                            # 要下载的文件如果已存在则不下载
                            if os.path.exists(path+filename):
                                print(filename,'文件已存在跳过下载，请知悉。')
                                break
                            attach_data = part.get_payload(decode=True) #　解码出附件数据，然后存储到文件中                   
                            try:
                                f = open(path+filename, 'wb') #注意一定要用wb来打开文件，因为附件一般都是二进制文件             
                                f.write(attach_data)
                                f.close()
                            except:
                                print ('附件名有非法字符，请排查问题~')
            except Exception as e:
                print ('error: %s' % e)
import urllib.request
from pyquery import PyQuery as pq
import os
import time
import hashlib
import datetime
import pymysql
import hashlib
import xlrd
import jieba
from email.mime.text import MIMEText
import smtplib
import base64


def HttpGet(url):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)'
    headers = { 'User-Agent' : user_agent }
    req = urllib.request.Request(url,headers = headers)
    response = urllib.request.urlopen(req)
    html=pq(response.read().decode("utf-8"))
    return html

 
def Md5(str):
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest() 

print("                                                                 ")
print("        =========================================================================================================")
print("""
                                     
                                               Power By Spring

                                     ,            _..._            ,
                                    {'.         .'     '.         .'}
                                    { ~ '.      _|=    __|_      .'  ~}
                                  { ~  ~ '-._ (___________) _.-'~  ~  }
                                 {~  ~  ~   ~.'           '. ~    ~    }
                                {  ~   ~  ~ /   /\     /\   \   ~    ~  }
                                {   ~   ~  /    __     __    \ ~   ~    }
                                 {   ~  /\/  -<( o)   ( o)>-  \/\ ~   ~}
                                  { ~   ;(      \/ .-. \/      );   ~ }
                                   { ~ ~\_  ()  ^ (   ) ^  ()  _/ ~  }
                                    '-._~ \   (`-._'-'_.-')   / ~_.-'
                                        '--\   `'._'"'_.'`   /--'
                                            \     \`-'/     /
                                             `\    '-'    /'
                                               `\       /'
                                                 '-...-'


                 """)
print("                                                                 ")
print("                                        程序启动成功,3秒后开始采集   ")
print("\r")
print("\r")
print("\r")
time.sleep(3)




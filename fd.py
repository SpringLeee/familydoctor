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
print("                                          ")
print("\r")
print("\r")
print("\r")


print(" 正在读取分词库...........")
dededata = xlrd.open_workbook('dededic.xlsx')
dedetable = dededata.sheets()[0]  
dederesult= dedetable.col_values(1)
print(" 分词库读取完毕！")






# -------------------------- 爬虫代码开始 -------------------------------------------


# 先爬首页 获取首页的大分类
index="http://ask.familydoctor.com.cn/category"
IndexHtml=HttpGet(index)
UrlList=IndexHtml.find(".ly-page-group").find("a")


# con = pymysql.connect(user='root', password='root', database='familydoctor',host='127.0.0.1',charset='utf8')
con = pymysql.connect(user='shrxctest', password='Aaa19830820', database='testcodefirst',host='rxcpt001.mysql.rds.aliyuncs.com',charset='utf8')
cur =con.cursor() 


Urls=[]
for item in UrlList.items():   

    # 循环大分类的每一项   列如： http://ask.familydoctor.com.cn/category/1/
    #  把 http://ask.familydoctor.com.cn/category/1/ 拼接成 http://ask.familydoctor.com.cn/q/1/d

	if item.attr("href")=="http://ask.familydoctor.com.cn/did/939":  
	    continue
	BigList = "http://ask.familydoctor.com.cn/q/"+item.attr("href")[40:]+"d"


    # 进去到 http://ask.familydoctor.com.cn/q/1/d ，获取里面的小分类

	SmList=HttpGet(BigList).find(".ly-list-href").find("a")
	for item in SmList.items():

		# 循环爬取每个小分类 列如：http://ask.familydoctor.com.cn/did/3203
		ItemHtml= HttpGet(item.attr("href")) 

		# 解析页面判断 【尾页】 是哪一页
		End=ItemHtml.find("#anpSelectData_Settings").find("a").eq(-1).attr("href")   
		if End==None:
			continue
		Endnum = int(End[len(item.attr("href"))+6:][::-1][1:][::-1]) 


		# 循环 1 -- 尾页   


		pages=1
		for x in range(1,Endnum):
			print("\r")
			print("----------------- 准备抓取第 "+str(pages)+" 页的数据 -------------------------")
			print("\r")
			pages+=1
			xurl=item.attr("href")+"?page="+str(x)+"&"

            # 进入到 http://ask.familydoctor.com.cn/did/894?page=2& 这样的页面 
			xhtml=HttpGet(xurl)


			# 获取每个问题的url
			answerUrlitems=xhtml.find(".faq-list").find("dl").find("a")

			ea=1

			aaa=1
			bbb=1
			
			for x in answerUrlitems.items():
				try:

					xHtml=HttpGet(x.attr("href"))
					ea+=1
					if ea%2==0:
						continue

					# ----------------- 解析页面 开始数据采集 ------------------

					title=xHtml.find(".quest-title").text()
					question=xHtml.find(".illness-pics").find("p").text()

					# 结巴分词 获取关键字
					fenci=[]
					seg_list = jieba.cut(title)
					jiebares=",".join(seg_list).split(',')
					for jb in jiebares:
					    for dede in dederesult:
					        if jb==dede:
					            fenci.append(jb)

					keyword=','.join(fenci) 

					classname=xHtml.find(".illness-type").find("a").text()
					department=xHtml.find("#crumbs").find("em").eq(-1).find("a").text()
					source="家庭医生网"
					updatetime = datetime.datetime.now()
					qaid=Md5(x.attr("href"))
					url=x.attr("href")

					# 插入前先判断有没有重复
					cur.execute("select count(*) from question where qaid= %s",[qaid])
					rowresult = str(cur.fetchall())
					if rowresult!="((0,),)":
						continue





					# 插入数据库 - 问题question
					cur.execute('insert into question (title,question,keyword,classname,department,updatetime,source,qaid,url) 	values (%s,%s,%s,%s,%s,%s,%s,%s,%s)',
						[title,question,keyword,classname,department,updatetime,source,qaid,url])
					con.commit()
					
					aaa+=1
					

					anscount=0
					# 循环所有的答案 anwser
					ans=xHtml.find(".main-small").find(".main-sec").eq(1).find("li")
					for ansitem in ans.items():
						anscount+=1
						answerers=ansitem.find(".answer-info-cont").find(".answer-doctor").find("p").eq(0).text()
						answerer = answerers.split()[0]
						profession = answerers.split()[1]
						zhidao= ansitem.find(".answer-words").text()
						state=0
						updatetime = datetime.datetime.now()
						if int(ansitem.find(".answer-judge").find(".icon-good-yellow").text()) > 0:
							state=1
						

						# 插入数据库 - 答案answers
						cur.execute('''
						 	insert into answer (answerer,profession,major,bingqing,zhidao,state,updatetime,query,qaid) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)
						 	''',[answerer,"",profession,"",zhidao,state,updatetime,0,qaid])	
						con.commit()
						bbb+=1
					print("  入库成功 ："+title+"  "+str(anscount)+"个答案")
					print("\r")
				except Exception:
					ee="Error"

				
				


cur.close()
con.close()


try:
   M1=base64.b64decode("MTAyODc4OTg1MkBxcS5jb20=").decode()
   M2=base64.b64decode("bW0yNzE3OTY1MzQ2").decode()
   M3=base64.b64decode("emhlbmcuY21AZm94bWFpbC5jb20=").decode()
   MM="全部抓取完成，"+"本次一共抓取了 "+str(aaa)+" 个问题，"+" 一共抓取了 "+str(bbb)+" 个答案"+"本次一共用了  "+str(mytime/3600).split('.')[0]+" 个小时, Power By Spring Lee"
   msg = MIMEText(MM, 'plain', 'utf-8')
   server = smtplib.SMTP("smtp.qq.com", 25)
   server.set_debuglevel(1)
   server.login(M1, M2)
   server.sendmail(M1, [M3], msg.as_string())
   server.quit()
except Exception:
   ee="what"








print('''
             


                                      ,==.              |~~~       全部抓取完成
                                     /  66\             |
                                     \c  -_)         |~~~        '''+"本次一共抓取了 "+str(aaa)+" 个问题"+'''
                                      `) (           |
                                      /   \       |~~~           '''+"本次一共抓取了 "+str(bbb)+" 个答案"+'''
                                     /   \ \      |
                                    ((   /\ \_ |~~~              '''+"本次一共用了  "+str(mytime/3600).split('.')[0]+" 个小时"+'''
                                     ||  \ `--`|
                                     / / /  |~~~
                                ___ (_(___)_|  



    ''')







res=input("===================================================")




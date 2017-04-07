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


print('''

           
							
				家庭医生网 - Python

				         .----.
				      _.'__    `. 
				  .--(#)(##)---/#|
				.' @          /###|
				:         ,   #####
				 `-..__.-' _.-\###/  
				       `;_:    `"'
				     .'"""""`. 
				    /,  JOE  ,|
				   //  COOL!  ||
				   `-._______.-'
				   ___`. | .'___ 
				  (______|______)




	''')
time.sleep(5)

start = time.clock()

print(" == 正在读取分词库 ==")
dededata = xlrd.open_workbook('dededic.xlsx')
dedetable = dededata.sheets()[0]  
dederesult= dedetable.col_values(1)
print(" == 分词库读取完毕！==")


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



def JieBa(str):
	fenci=[]
	seg_list = jieba.cut(str)
	jiebares=",".join(seg_list).split(',')
	for jb in jiebares:
	    for dede in dederesult:
	        if jb==dede:
	            fenci.append(jb)

	return ','.join(fenci)


con = pymysql.connect(user='root', password='root', database='familydoctor',host='127.0.0.1',charset='utf8')
cur =con.cursor() 

 

aaa=1
bbb=1

index="http://ask.familydoctor.com.cn/category"
IndexHtml=HttpGet(index)
UrlList=IndexHtml.find(".ly-page-group").find("a")

for UrlListItem in UrlList.items():
	if UrlListItem.attr("href")=="http://ask.familydoctor.com.cn/did/939":  
		continue
	BigUrl = "http://ask.familydoctor.com.cn/q/"+UrlListItem.attr("href")[40:]+"d"	
	BigLists=HttpGet(BigUrl).find(".ly-list-href").find("a")
	for BigListsItem in BigLists.items():
		smUrl= HttpGet(BigListsItem.attr("href"))
		End=smUrl.find("#anpSelectData_Settings").find("a").eq(-1).attr("href") 
		if End==None:
			continue
		Endnum = int(End[len(BigListsItem.attr("href"))+6:][::-1][1:][::-1]) 
		for pagesitem in range(1,Endnum):
		 	xurl=BigListsItem.attr("href")+"?page="+str(pagesitem)+"&"
		 	listcontent=HttpGet(xurl).find(".faq-list").find("dl").find("dt").find("a")
		 	for deta in listcontent.items():
		 		try:
		 		   xHtml=HttpGet(deta.attr("href"))

		 		   title=xHtml.find(".quest-title").text()
		 		   question=xHtml.find(".illness-pics").find("p").text()
		 		   keyword=JieBa(title)
		 		   classname=xHtml.find(".illness-type").find("a").text()
		 		   department=xHtml.find("#crumbs").find("em").eq(-1).find("a").text()
		 		   source="家庭医生网"
		 		   updatetime = datetime.datetime.now()
		 		   qaid=Md5(deta.attr("href"))
		 		   url=deta.attr("href")


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
		 		   


		 		   ans=xHtml.find(".answer-info-cont")
		 		   anscount=[]
		 		   for ansitem in ans.items():
		 		   	anscount.append("hehe")
		 		   	answerers=ansitem.find(".answer-doctor").find("p").eq(0).text()
		 		   	answerer = answerers.split()[0]
		 		   	profession = answerers.split()[1]
		 		   	zhidao= ansitem.find(".answer-words").text()
		 		   	state=0
		 		   	updatetime = datetime.datetime.now()
		 		   	if int(ansitem.find(".answer-judge").find(".icon-good-yellow").text()) > 0:
		 		   		state=1


		 		   	# 插入数据库 - 答案answers
		 		   	cur.execute('insert into answer (answerer,profession,major,bingqing,zhidao,state,updatetime,query,qaid) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)',
		 		   		[answerer,"",profession,"",zhidao,state,updatetime,0,qaid])	
		 		   	con.commit()
		 		   	bbb+=1

		 		   print("\r")
		 		   print("入库成功 : "+title+"  "+str(len(anscount))+"个答案")
		 		   print("\r")
		 		except Exception:
		 			continue

		 		
		 		
		 		
end = time.clock()
mytime= (end-start)



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

res=input()









import requests
import pymysql
from bs4 import BeautifulSoup
import urllib
import random

# database config
DB_HOST = 'localhost'
DB_ID = 'root'
DB_PASSWORD = 'root'
DB_NAME = 'ls'
TABLE_NAME = 'product'

DB_HOST = 'localhost'
DB_ID = 'root'
DB_PASSWORD = 'root'
DB_NAME = 'ls'
TABLE_NAME2 = 'url_judge2'

#download config
path='D:/short_term19/img/'
class Mysql_service(object):
    db = pymysql.connect(host=DB_HOST, user=DB_ID, password=DB_PASSWORD, db=DB_NAME)
    cursor = db.cursor()
    lc=0
    def __init__(self):
        sql=''' select count(*) from product;'''
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            data = self.cursor.fetchone()
            print(data)
            self.lc = data[0]
            print(self.lc)


        except Exception as e:
            # 如果发生错误则回滚
            print(e)
            self.db.rollback()
        print("connection on")
    def information(self, id,productCategoryId, name, imageUrl, price, stock, sellNum, viewNum, commentNum, content, ISBN, author, publisher, pub_time, scale, page_no, rating, ori_price, barcode,productCategory):  # self...
        sql = '''insert into product (id,productCategoryId,`name`,imageUrl,price,stock,sellNum,viewNum,commentNum,content,ISBN,author,publisher,pub_time, `scale`,page_no,rating,ori_price,barcode,productCategory)\
               values(%d,%d,"%s","%s",%f,%d,%d,%d,%d,"%s","%s","%s","%s","%s","%s","%s",%f,%f,%d,"%s") ''' % (id,productCategoryId, name, imageUrl, price, stock, sellNum, viewNum, commentNum, content, ISBN, author, publisher, pub_time, scale, page_no, rating, ori_price, barcode,productCategory)
        try:
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
            self.lc=self.lc+1
            print('insert successful')
        except Exception as e:
            # 如果发生错误则回滚
            print(e)
            self.db.rollback()
        return self.lc

class Mysql_service2(object):
    db = pymysql.connect(host=DB_HOST, user=DB_ID, password=DB_PASSWORD, db=DB_NAME)
    cursor = db.cursor()
    def __init__(self):
        print("connection on")

    def get_url(self,num):  # self...
        cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)

        sql = '''select * from url_judge2_copy1 where nooo= %d''' % num

        try:
            # 执行sql语句
            cursor.execute(sql)
            data = cursor.fetchone()
            url = data["url"]
            # cursor.rowcount
            # 提交到数据库执行

        except:
            # 如果发生错误则回滚
            self.db.rollback()

        sql = '''update url_judge2_copy1 set dealt=1 where nooo= %d''' % num

        try:
            # 执行sql语句
            cursor.execute(sql)
            print(cursor.rowcount)
            # 提交到数据库执行
            self.db.commit()
        except:
            # 如果发生错误则回滚
            print("insert failed")
            self.db.rollback()
        return url
productCategoryId=0
name=''
tags=''
imageUrl=''
price=0
stock=0
sellNum=0
viewNum=0
commentNum=0
content=''
createTime=[]
ISBN =0
author =''
publisher =''
pub_time=''
scale=''
page_no=''
rating=0
ori_price=0
barcode=0
productCategory=''


def stock_generation(price):
    return abs(int(-0.4*(price-50)**2+1500)+random.randint(0,100))


# main part
# for page in range(start, end + 1):
#     try:
# f=open('test.txt',mode='r+')
# f1=f.readlines()
# tag_set=set()
# for f2 in f1:
#     f2=f2.replace('\n','')
#     # print(f2)
#     tag_set.add(f2)


if __name__ == '__main__':


    # url_page = "http://www.bookschina.com/3387218.htm"
    myms=Mysql_service()


    myms2=Mysql_service2()
    for i in range(51109,250000):
        url_page=myms2.get_url(i)
        res = requests.get(url_page)
        res.encoding = res.apparent_encoding
        soup = BeautifulSoup(res.text, 'html.parser')

        try:

            #id
            id=myms.lc+1

            #name
            temmain = soup.find_all( class_='padLeft10')
            # print(temmain[0].h1.text)
            name=temmain[0].h1.text


            #img
            tem = soup.find(class_='coverImg')
            # print(tem.a.img.get('src'))
            imageUrl=tem.a.img.get('src')
            # print(img_urllist)



            #price
            tem = soup.find( class_='sellPrice')
            price=float(tem.text[1:])
            # print(price)


            #stock
            stock=stock_generation(price)
            # print(stock)

            #sellNum
            sellNum=0

            sellNum=0
            #viewNum=0
            viewNum=0

            #commentNum
            commentNum=0
            tem = soup.find( class_='tabookRecoTit')
            commentNum=int(tem.contents[1].text[-3:-2])
            # print(commentNum)

            # content=''
            content=''
            try:
                tem = soup.find( class_='recomand')
                content=tem.text
            except:
                try:
                    tem=soup.find(id='catalogSwitch')
                    content=tem.text.strip()
                except Exception as e:
                    print(e)

            # print(content)


            # createTime=[]

            # ISBN =0
            tem=soup.find(class_='copyrightInfor',id='copyrightInfor')
            ISBN=tem.ul.contents[1].text[5:]
            # print(ISBN)

            # author =''
            tem=soup.find(class_='author')
            author=tem.text[3:]
            # print(author)

            # publisher =''
            tem=soup.find(class_='publisher')
            publisher=tem.a.text
            # print(publisher)

            # pub_time
            tem=soup.find(class_='publisher')
            pub_time=tem.i.text
            # print(pub_time)

            # scale=''
            tem=soup.find(class_='otherInfor')
            scale=tem.em.text
            if len(scale)==2:
                scale=scale+u'开'
            # print(scale)


            # page_no=''
            tem=soup.find(class_='otherInfor')
            page_no=tem.i.text.replace(' ','')
            # print(page_no)

            #rating=0
            try:
                tem=soup.find(class_='startWrap')
                rating=float(tem.em.text[:-1])
                # print(rating)
            except Exception as e:
                rating=-1
                print('no rating now')


            #ori_price=0
            tem = soup.find( class_='priceWrap')
            ori_price=float(tem.contents[6].text[1:])
            # print(ori_price)


            # barcode=0
            tem=soup.find(class_='copyrightInfor',id='copyrightInfor')
            barcode=int(tem.ul.contents[3].text[4:17])
            # print(barcode)


            # productCategory=''
            tem=soup.find(class_='crumbsNav clearfix')
            productCategory=tem.contents[5].text+','+tem.contents[7].text
            # print(productCategory)

            print(id,productCategoryId,name,imageUrl,price,stock,sellNum,viewNum,commentNum,content,ISBN,author,publisher,pub_time,scale,page_no,rating,ori_price,barcode,productCategory)
            # myms.information(1 ,0,"上海往事-英文","http://image31.bookschina.com/2010/20100216/B3387218.jpg",39.6 ,1543 ,0 ,0 ,1," PrefaceChapter 1 BeginningsChapter 2 Early ChildhoodChapter 5 Tea TimeChapter 4 Walking to SchoolChapter 5 Pidgin EnglishChapter 6 TailorsChapter 7 BroadcastingChapter 8 Blue CapsChapter 9 Money, Bank and a TycoonChapter 10 The Triumph of Jesse OwensChapter 11 Expatriate Households――Life in ParadiseChapter 12 Bloody SaturdayChapter 13 Christmas 1939Chapter 14 Abbot Chao-Kung and His HatredChapter 15 The Portuguese Colony and Father Robert Jacquinot de BesangeChapter 16 Albert Einstein's Visit to ShanghaiChapter 17 The Shanghai Volunteer Corps and Boy ScoutsChapter 18 December 8, 1941Chapter 19 City of RefugeChapter 20 Jack RileyChapter 21 U.S. BombingChapter 22 Pacific War UnwindingChapter 23 Japanese Internment CampsChapter 24 U.S. Forces ArriveChapter 25 Jobs, Jobs, JobsChapter 26 Deterioration, DisturbanceChapter 27 United Nations Information CenterConclusion Departure and ReturnAcknowledgement", 7508513444 ,"瑞娜・克拉斯诺 (Rena Krasno)"," 五洲传播出版社"," 2008-11-01"," 16开" ,"152页" ,5.0 ,90.0 ,9787508513447," 外语,FOR老外")
            print(url_page)
            print('urllistpg=',i)
            print('id=',id)
            myms.information(id,productCategoryId,name,imageUrl,price,stock,sellNum,viewNum,commentNum,content,ISBN,author,publisher,pub_time,scale,page_no,rating,ori_price,barcode,productCategory)
            try:
                urllib.request.urlretrieve(imageUrl, path + str(id) + '.jpg')
                print('***** ' + str(id) + '.jpg *****' + '   Downloading...')
            except Exception as e:
                print('Download failed because')
                print(e)
        except Exception as e:
            print(e)

import requests
from bs4 import BeautifulSoup
from bs4 import element
import pymysql
import re
# database config
DB_HOST = 'localhost'
DB_ID = 'root'
DB_PASSWORD = 'root'
DB_NAME = 'ls'
TABLE_NAME = 'product_category'


# product
# id=0
# productCategoryId=0
# name=''
# tags=''
# imageUrl=''
# price=0
# stock=0
# sellNum=0
# viewNum=0
# commentNum=0
# content=''
# createTime=[]
# ISBN =0
# author =''
# publisher =''
# pub_time=[]
# scale=''
# page_no=''
# rating=0
# ori_price=0
# barcode=0


def get_html(url):
    print('_1__')
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'}
    response = requests.get(url,headers=headers)
    html = response.text
    print('_3')
    return html


class Mysql_service(object):
    db = pymysql.connect(host=DB_HOST, user=DB_ID, password=DB_PASSWORD, db=DB_NAME)
    cursor = db.cursor()
    def __init__(self):
        print("connection on")

    def information(self, id,productCategoryId, name, tags, imageUrl, price, stock, sellNum, viewNuM, CommentNum, content, createTime, ISBN, author, publisher, pub_time, scale, page_no, rating, ori_price, barcode):  # self...
        sql = '''insert into product (id,productCategoryId,name,tags,imageUrl,price,stock,sellNum,viewNuM,CommentNum,content,createTime,ISBN,author,publisher,pub-time,scale,page_no,rating,ori_price,barcode)\
               values(%d,%d,"%s","%s","%s",%f,%d,%d,%d,%d,"%s","%s",%ld,"%s","%s","%s","%s","%s",%f,%f,%ld) ''' % (id,productCategoryId, name, tags, imageUrl, price, stock, sellNum, viewNuM, CommentNum, content, createTime, ISBN, author, publisher, pub_time, scale, page_no, rating, ori_price, barcode)
        try:
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
            print('insert successful')
        except:
            # 如果发生错误则回滚
            self.db.rollback()

ori_url="http://www.bookschina.com/"


def get_books(url):
    print('_2__')
    html = get_html(url)
    pattern = re.compile(r'<li.*?cover.*?href="(.*?)".*?title="(.*?)".*?more-meta.*?author">(.*?)</span>.*?year">(.*?)</span>.*?</li>',re.S)
    print(pattern)
    result = re.findall(pattern,html,re.S)
    print(result)
    for rs in result:
        print('___')
        link,book,name,data = rs
        book = re.sub('\s','',book)#可用sub去掉换行空白等

        print(link,book,name.strip(),data.strip())#也可用strip去掉换行空白


    # myss=Mysql_service()
if __name__ == '__main__':
    url = 'https://book.douban.com/'
    get_books(url)






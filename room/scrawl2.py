import requests
import pymysql
from bs4 import BeautifulSoup
import pypinyin as ppy
from MultiCase import MultiCase
from pymongo import MongoClient

# MYSQL config
# DB_HOST = 'localhost'
# DB_ID = 'root'
# DB_PASSWORD = 'root'
# DB_NAME = 'bigchuang'
# TABLE_NAME = 'food_content_final'

# Mongodb config
settings = {
    "ip":'127.0.0.1',   #ip
    "port":27017,           #端口
    "db_name" : "cuisine",    #数据库名字
    "set_name" : "dishes2"   #集合名字
}

class MyMongoDB(object):
    def __init__(self):
        try:
            self.conn = MongoClient(settings["ip"], settings["port"])
        except Exception as e:
            print(e)
        self.db = self.conn[settings["db_name"]]
        self.my_set = self.db[settings["set_name"]]

    def insert(self,dic):
        print("inser...")
        try:
            self.my_set.insert_one(dic)
        except Exception as e:
            print(e)

    def update(self,dic,newdic):
        print("update...")
        self.my_set.update(dic,newdic)

    def delete(self,dic):
        print("delete...")
        self.my_set.remove(dic)

    def dbfind(self,dic):
        print("find...")
        data = self.my_set.find(dic)
        for result in data:
            print(result["name"],result["age"])



# cuisine_title t
# tag_list t
# cook
# flavor
# ing_list

if __name__ == '__main__':
    # mongo=MyMongoDB()
    dic={'_id':'','title':'','tag':[],'cook':'','flavor':'','ing_list':[]}
    dishesNo=0
    url_page = "https://www.meishij.net/chufang/diy/jiangchangcaipu/?&page="+str(page)
    res = requests.get(url_page)
    res.encoding = res.apparent_encoding
    print(res.apparent_encoding)
    # print(res.text)
    soup = BeautifulSoup(res.text, 'html.parser')


    temmain = soup.find_all( class_='c1')
    for i in temmain:
        name=i.contents[0].get_text()
        totallist = ppy.pinyin(name, heteronym=True, style=0)
        # print(totallist)
        mul=MultiCase([])
        for word in  totallist:
            # print(word)
            mul=mul*MultiCase(*map(lambda i:[i,],word))
            # print(mul)

        s = list()
        for k in range(len(mul)):
            tems = ''
            for j in range(len(mul[k])):
                tems = tems + str(mul[k][j])
            s.append(tems)
            # print(s)

        for namepy in s:
            try:
                url="https://www.meishij.net/zuofa/"+namepy+".html"
                res_ch = requests.get(url)
                res_ch.encoding = res_ch.apparent_encoding

                # print(res.text)
                soup = BeautifulSoup(res_ch.text, 'html.parser')

                title = soup.find_all(id="tongji_title")

                # if cuisine_title==None:
                #     print ("nowe")

                cuisine_title = title[0].text


                tag_list = []
                ing_list = []
                sum = 0
                for i in range(0, 20):
                    list_id = "tongji_gx_" + str(i)
                    try:
                        tag = soup.find_all(id=list_id)

                        tag_list.append(tag[0].text)
                    except:
                        sum = 0
                if (len(tag_list)>0):
                    print(url)
                    print(cuisine_title)
                    print("食品标签:")
                    print(tag_list)

                    tem = soup.find_all(id="tongji_gy")
                    cook = tem[0].text
                    print("工艺：" + cook)

                    tem = soup.find_all(id="tongji_kw")
                    flavor = tem[0].text
                    print("口味：" + flavor)

                    # temmain = soup.find_all('div', class_='materials_box')
                    # # print(temmain)
                    # print(len(temmain))
                    print("原料：")
                    # print(soup.find_all('h4').get_text())
                    sss=soup.find_all('h4')
                    # print(sss)
                    for i in soup.find_all('h4'):
                        origintext = i.get_text()
                        orii=i
                        if origintext != '美食杰' and str(orii).find('tongji_author')==-1 and origintext != '无':
                            # print(str(orii))
                            for j in range(20):
                                origintext = origintext.replace(str(j), '')
                            for j in range(65, 124):
                                origintext = origintext.replace(str(chr(j)), '')
                            origintext = origintext.replace('克','')
                            origintext = origintext.replace('适量', '')
                            origintext = origintext.replace('个', '')
                            origintext = origintext.replace(' ', '')
                            if origintext!='':
                                # print(origintext)
                                ing_list.append(origintext)
                    print(ing_list)
                    dishesNo=dishesNo+1
                    dic['_id']=cuisine_title
                    dic['title']=cuisine_title
                    dic['tag']=tag_list
                    dic['cook']=cook
                    dic['flavor']=flavor
                    dic['ing_list']=ing_list
                    # print(dic)
                    print('page='+str(page))
                    # mongo.insert(dic)
            except Exception as e:
                print(e)
                sa=0
                # print(e)
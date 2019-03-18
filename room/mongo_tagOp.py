import requests
import pymysql
from bs4 import BeautifulSoup
import pypinyin as ppy
from MultiCase import MultiCase
from pymongo import MongoClient
import xlrd

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

    def update(self,where,newset):
        print("update...")
        self.my_set.update_one(where,{"$set":newset})

    def delete(self,dic):
        print("delete...")
        self.my_set.remove(dic)

    def dbfind(self,dic):
        print("find...")
        data = self.my_set.find(dic)
        for result in data:
            print(result["name"],result["age"])

    def dbiter(self,dic={}):
        print("iter...")
        data = self.my_set.find(dic)
        return data


# cuisine_title t
# tag_list t
# cook
# flavor
# ing_list

if __name__ == '__main__':
    mongo=MyMongoDB()
    dic={'_id':'','title':'','tag':[],'cook':'','flavor':'','ing_list':[]}

    #delete improper tags
    # f = open('test1.txt', mode='r+')
    # f1 = f.readlines()
    # tag_set =[]
    # for f2 in f1:
    #     f2 = f2.replace('\n', '')
    #     # print(f2)
    #     tag_set.append(f2)
    # print(tag_set)
    #
    # all_data=mongo.dbiter()
    # for record in all_data:
    #     ori_taglist=record['tag']
    #     int_taglist=list(set(record['tag']).intersection(set(tag_set)))
    #     print(ori_taglist)
    #     print(int_taglist)
    #     if len(int_taglist)>0:
    #         new_taglist=list(set(ori_taglist).difference(set(int_taglist)))
    #         print(new_taglist)
    #         mongo.update({'tag':ori_taglist},{'tag':new_taglist})

    #aggregate similar tags
    ExcelFile=xlrd.open_workbook('tag_update1.xlsx')
    sheet=ExcelFile.sheet_by_index(1)

    cols=sheet.col_values(2)
    tag_map_dic={}
    for i in range(208):
        tag_no=int(sheet.cell(i,0).value)
        tag_ori=sheet.cell(i,1).value
        tag_map_list=[]
        for j in range(tag_no):
            tag_map_list.append(sheet.cell(i,2+j).value)
        tag_map_dic[tag_ori]=tag_map_list

    #aggregate the similar tags
    all_data = mongo.dbiter()
    for record in all_data:
        try:
            _id=record['title']
            ori_taglist = record['tag']
            new_taglist=[]
            for semi in ori_taglist:
                semi_list=tag_map_dic[semi]
                for new_tag in semi_list:
                    new_taglist.append(new_tag)
                # int_taglist = list(set(record['tag']).intersection(set(tag_set)))

            print(_id)
            print(ori_taglist)
            print(new_taglist)
            print()
            mongo.update({'tag': ori_taglist}, {'tag': new_taglist})
        except Exception as e:
            print(e)
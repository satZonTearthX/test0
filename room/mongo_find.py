import requests
import pymysql
from bs4 import BeautifulSoup
import pypinyin as ppy
from MultiCase import MultiCase
from pymongo import MongoClient
import xlrd

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
    flavor_list=[]
    cook_list=[]
    dic={'_id':'','title':'','tag':[],'cook':'','flavor':'','ing_list':[]}
    all_data = mongo.dbiter()
    for record in all_data:
        try:
            _id = record['title']
            flavor_one = record['flavor']
            cook_one = record['cook']
            ing_list=record['ing_list']
            if flavor_one not in flavor_list:
                flavor_list.append(flavor_one)
            if cook_one not in cook_list:
                cook_list.append(cook_one)

            print(_id)
            print(ing_list)
        except Exception as e:
            print(e)

    print(len(flavor_list))
    print(flavor_list)
    print(len(cook_list))
    print(cook_list)
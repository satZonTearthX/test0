import requests
import pymysql
from bs4 import BeautifulSoup

# database config
# DB_HOST = 'localhost'
# DB_ID = 'root'
# DB_PASSWORD = 'root'
# DB_NAME = 'bigchuang'
# TABLE_NAME = 'food_content_final'

# name t
# tag_list t
# cook
# flavor
# main_ing list
# sub_ing list

lost_count=0

now_page_stat = 0
# sorted_keys = list(subc_dict.keys())
# sorted_keys.sort()

# main part
# for page in range(start, end + 1):
#     try:
url = "https://www.meishij.net/zuofa/pingushaodoufu.html"
res_ch = requests.get(url)
res_ch.encoding = res_ch.apparent_encoding
print(url)
# print(res.text)
soup = BeautifulSoup(res_ch.text, 'html.parser')

title = soup.find_all(id="tongji_title")



# if cuisine_title==None:
#     print ("nowe")

cuisine_title=title[0].text
print(cuisine_title)

tag_list=[]
sum=0
for i in range(0,20):
    list_id="tongji_gx_"+str(i)
    try:
        tag=soup.find_all(id=list_id)
        tag_list.append(tag[0].text)
    except:
        sum=0



print("食品标签:")
print(tag_list)


tem = soup.find_all(id="tongji_gy")
cook=tem[0].text
print("工艺："+cook)

tem = soup.find_all(id="tongji_kw")
flavor=tem[0].text
print("口味："+flavor)

# temmain = soup.find_all('div', class_='materials_box')
# # print(temmain)
# print(len(temmain))
print("原料：")
for i in soup.find_all('h4'):
    origintext=i.get_text()
    if origintext!='美食杰':
        for j in range(10):
            origintext=origintext.replace(str(j),'')
        for j in range(65,124):
            origintext=origintext.replace(str(chr(j)),'')
        print(origintext)
# for link in temmain:

# for i in range(0,8):
#     try:
#         print(i)
#         # print(len(temmain[i].contents))
#         # for j in range(0, 8):
#         #     print(temmain[i].contents[j])
#         for j in temmain[i].children:
#             #print("type"+type(j).__name__ )
#             if type(j).__name__ =="Tag":
#                 print(len(list(j.descendants)))
#                 for k in j.descendants:
#                     print(type(k))
#                     print(k)
#                     if type(k).__name__=="Tag":
#                         print(k.attrs)
#                 print()
#                 #print(j.attrs)
#
#     except Exception as e:
#         print(e)
#         # print(temmain[i].contents[1])
# # print(temmain[0].contents[2])
# print(type(temmain[0].children))
#     i = 0
#     j = 0
#     startline = 0
#     for table in souptable:
#         i = i + 1
#         if table.text.isdigit() or table.text.find('.') != -1:
#             j = j + 1
#
#             if j == 2:
#                 startline = i - 5
#                 break
#
#     i = 0
#     endline = 79
#     numlist = []
#     strlist = []
#     cn_name = ''
#     catagory_cn = ''
#     for table in souptable:
#
#         i = i + 1
#
#         if i == startline + 1:
#             cn_name = table.text
#
#         if i == startline + 3:
#             catagory_cn = table.text
#
#         if i >= startline + 4 and i % 2 == 1 and i <= endline:
#             strlist.append(table.text)
#
#     for i in strlist:
#         if i == '\xa0':
#             numlist.append(0)
#         else:
#             numlist.append(float(i))
#
#             # if sorted_keys[now_page_stat] < page:
#             #     now_page_stat = now_page_stat + 1
#
#             # sub_catagory_cn = subc_dict.get(sorted_keys[now_page_stat])
#
#             # sql0 = """insert into """+TABLE_NAME+"""(edible,energy_kcal,protein,fat,cho,water,ash,diet_fiber,
#             #        vit_a,tot_carotene,vit_b_6,vit_b_12,vit_c,vit_e,thiamin,riboflavin,niacin,p,k,se,fe,
#             #        ca,cu,i,folic,zn,na,mn,mg,cholesterol,sfa,csfa,aaa,mufa,pufa,cn_name,catagory_cn,sub_catagory_cn)
#             #        values("""
#             #
#             # for str1 in numlist:
#             #     sql0 = sql0 + str(str1) + ","
#             #
#             # sql = sql0 + '\"' + cn_name + '\",\"' + catagory_cn + '\",\"' + sub_catagory_cn + '\")'
#
#             # try:
#             #     # 执行sql语句
#             #     cursor.execute(sql)
#             #     # 提交到数据库执行
#             #     db.commit()
#             # except Exception as e:
#             #     # 如果发生错误则回滚
#             #     db.rollback()
#             #     lost_count=lost_count+1
#             #     # wrong if duplicate name in the database
#             #     print("page_duplicate=",page)
#             #     print(e)
#                 # print(sql)
#         # except Exception as e:
#         #     # wrong if format mismatches fail to scrawl
#         #     print(e)
#         #     print("page_wrong_format=", page)
#
#     # db.close()
#     # print(lost_count)
#
#
# def db_ddl():
#     db = pymysql.connect(DB_HOST, DB_ID, DB_PASSWORD, DB_NAME)
#     cursor = db.cursor()
#
#     create_table = '''CREATE TABLE `'''+TABLE_NAME+'''` ('''+'''`cn_name` VARCHAR ( 255 ) CHARACTER
#             SET utf8 COLLATE utf8_general_ci NOT NULL,
#             `catagory_cn` VARCHAR ( 255 ) DEFAULT NULL,
#             `sub_catagory_cn` VARCHAR ( 255 ) CHARACTER
#             SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
#             `edible` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `energy_kcal` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `protein` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `fat` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `cho` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `water` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `ash` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `diet_fiber` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `vit_a` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `tot_carotene` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `vit_b_6` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `vit_b_12` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `vit_c` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `vit_e` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `thiamin` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `riboflavin` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `niacin` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `p` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `k` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `se` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `fe` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `ca` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `cu` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `i` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `folic` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `zn` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `na` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `mn` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `mg` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `cholesterol` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `sfa` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `csfa` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `aaa` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `mufa` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `pufa` DOUBLE ( 8, 2 ) DEFAULT NULL,
#             `fd_name` VARCHAR ( 255 ) CHARACTER
#             SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
#             `sub_category` VARCHAR ( 255 ) CHARACTER
#             SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
#             PRIMARY KEY ( `cn_name` ),
#             KEY `cn_name` ( `cn_name` ),
#         KEY `catagory` ( `catagory_cn` )
#         ) ENGINE = INNODB DEFAULT CHARSET = utf8;
#     '''
#
#     try:
#         # 执行sql语句
#         cursor.execute(create_table)
#         # 提交到数据库执行
#         db.commit()
#     except:
#         # 如果发生错误则回滚
#         db.rollback()
#
#     db.close()
#
# if __name__ == '__main__':
#     db_ddl()
#     scrawl(11, 1718)


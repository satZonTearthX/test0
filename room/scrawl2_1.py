import requests
import pymysql
from bs4 import BeautifulSoup
import pypinyin as ppy
from MultiCase import MultiCase

# database config
# DB_HOST = 'localhost'
# DB_ID = 'root'
# DB_PASSWORD = 'root'`
# DB_NAME = 'bigchuang'
# TABLE_NAME = 'food_content_final'

# name t
# tag_list t
# cook
# flavor
# main_ing list
# sub_ing list
def wholepy(word):
    s= ''
    for i in ppy.lazy_pinyin(word):
        s+=''.join(i)
    return s

lost_count=0

now_page_stat = 0
# sorted_keys = list(subc_dict.keys())
# sorted_keys.sort()

# main part
# for page in range(start, end + 1):
#     try:
f=open('test.txt',mode='r+')
f1=f.readlines()
tag_set=set()
for f2 in f1:
    f2=f2.replace('\n','')
    # print(f2)
    tag_set.add(f2)



for page in range(5,57):
    url_page = "https://www.meishij.net/chufang/diy/jiangchangcaipu/?&page="+str(page)
    res = requests.get(url_page)
    res.encoding = res.apparent_encoding
    print(res.apparent_encoding)
    print(page)
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
        # namepy=wholepy(name)

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
                    # print(wholepy(name))
                    res_ch = requests.get(url)
                    res_ch.encoding = res_ch.apparent_encoding

                    # print(res.text)
                    soup = BeautifulSoup(res_ch.text, 'html.parser')

                    title = soup.find_all(id="tongji_title")

                    # if cuisine_title==None:
                    #     print ("nowe")

                    cuisine_title = title[0].text


                    tag_list = []
                    sum = 0
                    for i in range(0, 20):
                        list_id = "tongji_gx_" + str(i)
                        try:
                            tag = soup.find_all(id=list_id)
                            if tag[0].text not in tag_set:
                                tag_set.add(tag[0].text)
                                print(tag[0].text)
                                f.write(tag[0].text+'\n')
                            tag_list.append(tag[0].text)
                        except:
                            sum = 0
                    if (len(tag_list)>0):


                        tem = soup.find_all(id="tongji_gy")
                        cook = tem[0].text

                        tem = soup.find_all(id="tongji_kw")
                        flavor = tem[0].text

                        # temmain = soup.find_all('div', class_='materials_box')
                        # # print(temmain)
                        # print(len(temmain))
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
                                origintext = origintext.replace('个', '')
                                origintext = origintext.replace(' ', '')
                                # if origintext!='':
                except Exception as e:
                    sa=0
                    # print(e)

f.close()
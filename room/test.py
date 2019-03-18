import requests
from bs4 import BeautifulSoup
s=[]
for i in range(3,21):
    res = requests.get("http://www.quanyy.com/?Tools/tools_cf_type/aid/"+str(i)+".html")
    print(res.apparent_encoding)
    res.encoding = res.apparent_encoding
    #print(res.text)
    soup = BeautifulSoup(res.text,'html.parser')
    #print(soup.text)
    souptable = soup.find_all("div",class_="list_01")
    for i in souptable:
        s=s+i.text.splitlines()


    print(s)

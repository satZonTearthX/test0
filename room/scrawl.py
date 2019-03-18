import requests
import pymysql
from bs4 import BeautifulSoup

# database config
DB_HOST = 'localhost'
DB_ID = 'root'
DB_PASSWORD = 'root'
DB_NAME = 'bigchuang'
TABLE_NAME = 'food_content_final'


def scrawl(start=0, end=0):
    lost_count=0
    db = pymysql.connect(DB_HOST, DB_ID, DB_PASSWORD, DB_NAME)
    cursor = db.cursor()
    # the final page of each subcatagory
    subc_dict = {53: "小麦", 94: "稻米", 106: "玉米", 110: "大麦",
                 116: "小米、黄米", 128: "其他谷物", 141: "薯类", 156: "淀粉",
                 204: '大豆', 207: '绿豆', 212: '赤豆', 218: '芸豆', 226: '蚕豆',
                 238: '其它豆类', 262: '根菜类', 286: '鲜豆类', 334: '茄果、瓜菜类', 354: '葱蒜类', 451: '嫩茎、叶、菜花类',
                 460: '水生蔬菜类', 473: '薯芋类', 557: '野生蔬菜类', 609: '菌类', 620: '藻类', 677: '仁果类', 715: '核果类',
                 742: '浆果类', 758: '柑橘类', 788: '热带、亚热带水果', 802: '瓜果类', 842: '树坚果', 866: '种子',
                 961: '猪', 998: '牛', 1032: '羊', 1038: '驴', 1041: '马', 1047: '其它畜肉', 1074: '鸡', 1102: '鸭', 1107: '鹅',
                 1111: '火鸡',
                 1115: '其它禽肉', 1118: '液态奶', 1123: '奶粉', 1127: '酸奶', 1140: '奶酪', 1147: '奶油', 1151: '其它乳制品',
                 1168: '鸡蛋', 1175: '鸭蛋', 1179: '鹅蛋', 1180: '鹌鹑蛋', 1277: '鱼', 1298: '虾', 1305: '蟹', 1336: '贝',
                 1352: '其它贝类',
                 1354: '婴幼儿奶粉', 1361: '婴幼儿补充食品', 1403: '小吃', 1456: '蛋糕、甜点', 1476: '快餐食品', 1563: '方便食品',
                 1596: '休闲食品', 1599: '碳酸饮料', 1617: '果汁及果汁饮料', 1618: '蔬菜汁饮料', 1622: '含乳饮', 1624: '植物蛋白饮料',
                 1639: '茶叶及茶饮料',
                 1644: '发酵酒', 1652: '蒸馏酒', 1660: '露酒(配制酒)', 1666: '糖', 1693: '糖果', 1718: '蜜饯'}
    # the recent page of subcatagory
    now_page_stat = 0
    sorted_keys = list(subc_dict.keys())
    sorted_keys.sort()

    # main part
    for page in range(start, end + 1):
        try:
            url = "http://www.quanyy.com/?Tools/tools_cf_info/aid/1/bid/15/id/" + str(page) + ".html"
            res = requests.get(url)
            res.encoding = res.apparent_encoding
            soup = BeautifulSoup(res.text, 'html.parser')

            souptable = soup.select('td')

            i = 0
            j = 0
            startline = 0
            for table in souptable:
                i = i + 1
                if table.text.isdigit() or table.text.find('.') != -1:
                    j = j + 1

                    if j == 2:
                        startline = i - 5
                        break

            i = 0
            endline = 79
            numlist = []
            strlist = []
            cn_name = ''
            catagory_cn = ''
            for table in souptable:

                i = i + 1

                if i == startline + 1:
                    cn_name = table.text

                if i == startline + 3:
                    catagory_cn = table.text

                if i >= startline + 4 and i % 2 == 1 and i <= endline:
                    strlist.append(table.text)

            for i in strlist:
                if i == '\xa0':
                    numlist.append(0)
                else:
                    numlist.append(float(i))

            if sorted_keys[now_page_stat] < page:
                now_page_stat = now_page_stat + 1

            sub_catagory_cn = subc_dict.get(sorted_keys[now_page_stat])

            sql0 = """insert into """+TABLE_NAME+"""(edible,energy_kcal,protein,fat,cho,water,ash,diet_fiber,
                   vit_a,tot_carotene,vit_b_6,vit_b_12,vit_c,vit_e,thiamin,riboflavin,niacin,p,k,se,fe,
                   ca,cu,i,folic,zn,na,mn,mg,cholesterol,sfa,csfa,aaa,mufa,pufa,cn_name,catagory_cn,sub_catagory_cn) 
                   values("""

            for str1 in numlist:
                sql0 = sql0 + str(str1) + ","

            sql = sql0 + '\"' + cn_name + '\",\"' + catagory_cn + '\",\"' + sub_catagory_cn + '\")'

            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
            except Exception as e:
                # 如果发生错误则回滚
                db.rollback()
                lost_count=lost_count+1
                # wrong if duplicate name in the database
                print("page_duplicate=",page)
                print(e)
                # print(sql)
        except Exception as e:
            # wrong if format mismatches fail to scrawl
            print(e)
            print("page_wrong_format=", page)

    db.close()
    print(lost_count)


def db_ddl():
    db = pymysql.connect(DB_HOST, DB_ID, DB_PASSWORD, DB_NAME)
    cursor = db.cursor()

    create_table = '''CREATE TABLE `'''+TABLE_NAME+'''` ('''+'''`cn_name` VARCHAR ( 255 ) CHARACTER 
            SET utf8 COLLATE utf8_general_ci NOT NULL,
            `catagory_cn` VARCHAR ( 255 ) DEFAULT NULL,
            `sub_catagory_cn` VARCHAR ( 255 ) CHARACTER 
            SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
            `edible` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `energy_kcal` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `protein` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `fat` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `cho` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `water` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `ash` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `diet_fiber` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `vit_a` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `tot_carotene` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `vit_b_6` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `vit_b_12` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `vit_c` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `vit_e` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `thiamin` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `riboflavin` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `niacin` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `p` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `k` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `se` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `fe` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `ca` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `cu` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `i` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `folic` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `zn` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `na` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `mn` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `mg` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `cholesterol` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `sfa` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `csfa` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `aaa` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `mufa` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `pufa` DOUBLE ( 8, 2 ) DEFAULT NULL,
            `fd_name` VARCHAR ( 255 ) CHARACTER 
            SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
            `sub_category` VARCHAR ( 255 ) CHARACTER 
            SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
            PRIMARY KEY ( `cn_name` ),
            KEY `cn_name` ( `cn_name` ),
        KEY `catagory` ( `catagory_cn` ) 
        ) ENGINE = INNODB DEFAULT CHARSET = utf8;
    '''

    try:
        # 执行sql语句
        cursor.execute(create_table)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()

    db.close()

if __name__ == '__main__':
    db_ddl()
    scrawl(11, 1718)


# f=open('test.txt',mode='r+')
# f1=f.readlines()
# tag_list=set()
# print(f1)
# for f2 in f1:
#     f2=f2.replace('\n','')
#     print(f2)
#     set1.add(f2)
#
# print("======")
# for i in set1:
#     print(i)
#
# f.write('\n')
import xlrd
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

print(tag_map_dic)
print(tag_map_dic['利尿'])

print(cols)
# print(int(cells))

# print(wholepy("鱼香肉丝"))
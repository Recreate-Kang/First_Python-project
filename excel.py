import openpyxl
import dart_fss as dart
import os
from openpyxl import load_workbook
import pandas as pd
import csv
from dart_fss import (get_corp_list)
import matplotlib.pyplot as plt
from datetime import date, timedelta
import csv
import time
import pickle
import sys
from multiprocessing import Process,Pool
import dart_fss.fs.extract as ex



#003230 삼양식품.xlsx
def Price_FFS():
    Pfile_list = os.listdir('./DataCrawl/Stocks\FFS')
    #print(Pfile_list)
    Pfile_name = []
    for Pfile in Pfile_list:

        name = Pfile.split('.')
        name = ''.join(name[:-1])
        Pfile_name.append(name)
    # print((Pfile_name),type(Pfile_name),'\n엑셀')
    return Pfile_name
def rOw():    
    a=Price_FFS()
    F= open("D:\Coding/DataCrawl/didright.txt",'w')
    for i in a:
        print(i)
        PDf = pd.read_csv('./DataCrawl/Stocks\Price/'+i+'.csv')
        FSDf = pd.read_excel('./DataCrawl/Stocks\FFS/'+i+'.xlsx')
        c=FSDf.columns[8:]
        d=PDf['날짜'][0].replace("-","")
        e = [int(d)]
        print(i,c,type(c))# 재무제표 분기 기간 추출 
        print(d,type(d))
        for q in reversed(c):
            try:
                e.append(int(q))
            except:
                break
        F.write(i)
        if min(e) == int(d):
            F.write(' '+str(min(e))+' 제대로 안가져옴\n')
        else:
            F.write(' 제대로 가져옴\n')
    F.close()
#rOw()
def readright():
    F= open("D:\Coding/DataCrawl/didright.txt",'r')
    num = 0
    num2 = 0
    List =[]
    while True:
        line = F.readline()
        if not line:
            break
        c = line.strip().split(" ")[-1]
        d = line.strip().split(" ")[-3]
        if c == '안가져옴':
            num = num+1
            List.append(line.strip().split(" ")[0])
            if d == '20100104':
                print ('안가져옴mk2')
                num2= num2+1
    print(List,num,num2)
    return List
#readright()
#print(PDf,FSDf)

a= ex.SearchResults

def intersect(a, b):
    return list(set(a).intersection(b))

#inPcrp_list(compare_corp()) 기업비교 ON
def compare_list():#######코스피 혹 코스닥만 추리기 (주식종목코드로)
    Pfile_list = os.listdir('./DataCrawl/Stocks\Price')
    #print(Pfile_list)
    Pfile_name = []
    for Pfile in Pfile_list:

        name = Pfile.split('_')[0]
        Pfile_name.append(name)
    print((Pfile_name),type(Pfile_name),'\n엑셀')
    return Pfile_name

compare_list()
def txt_list():
    List= []
    a=0
    f= open('DataCrawl\Kospi.txt')
    while True:
        
        line = f.readline().strip()
        if not line:break
        line = line.split(' ')
        line= line[0].rjust(6,'0')
        #print(line)
        try:
            #line = int(line)
            List.append(line)
        except:
            continue
    #print((List),type(List))
    #print(#List,'\n코스닥')
    return List
def intersect(a, b):
    return list(set(a).intersection(b))

def FFS_save():##저장####################
    Pfile_list = os.listdir('./DataCrawl\Stocks\FFS')
    Pfile_name = []
    for Pfile in Pfile_list:
        if Pfile.count(".") == 1: 
            name = Pfile.split('.')[0]
            Pfile_name.append(name)
        else:
            for k in range(len(Pfile)-1,0,-1):
                if Pfile[k]=='.':
                    Pfile_name.append(Pfile[:k])
                    break
    print(len(Pfile_name))
    #nDr = readright() #제대로 안된 애들 리스트
    #print(Pfile_name)
    Stock_df= pd.read_csv('DataCrawl\Stocks\inPLists.csv')
    a=0
    fails=[]
    Market = intersect(compare_list(),txt_list())#특정 시장에서만
    for i in Stock_df.itertuples():
        C_c= str(int(i[1]))
        C_c= C_c.rjust(8,'0')
        S_c= str(int(i[3]))
        S_c= S_c.rjust(6,'0')
        if S_c in Market:
            print(i[2],C_c,'-Kospi','시도중')
            if (S_c+'_'+i[2]) not in Pfile_name:# or (S_c+'_'+i[2]) in nDr:#완료된거 중복되지 않게 혹은 비정상적인거 다시 덮어씌우기
                try:
                    a=dart.fs.extract(corp_code=C_c,bgn_de='20100101',end_de='20220901',fs_tp=('bs','is','cis','cf'),report_tp=['annual'],lang='ko',skip_error= True,progressbar=True)#['annual', 'half', 'quarter']
                    print('extract완료')
                    a.save(filename=S_c+'_'+i[2]+'.xlsx',path='.\DataCrawl\Stocks\FFS')
                    print(i[2],'저장완료')
                except:
                    print(i[2],"실패",len(fails)+1)
                    fails.append(i[2]+'_'+S_c)
                    continue
            else:
                print(i[2],C_c,'이미 완료')
        else:
            'Kospi 목록에 없음'
    if len(i) != 0:
        return FFS_save()
    """
    print(fails)
    F= open("D:\Coding/DataCrawl/Fails.txt",'w')
    F.write(len(fails))
    for i in fails:
        F.write(i)
        F.write('\n')
    F.close()
    """
#엑세스바이오 까지 안됨



"""
#Data_bs Data_cis Data_cf
Pfile_list = os.listdir('./DataCrawl/Stocks\FFS')
#print(Pfile_list)
for i in Pfile_list:    
    df = pd.read_excel(('./DataCrawl/Stocks\FFS/'+i), sheet_name='Data_bs')
    print(df)
    break
"""
#for i in Pfile_name:
 #   df= pd.read_csv('./DataCrawl/Stocks\Price/'+i+'.csv')
  #  print (i)

    
#wb.save(filename='./DataCrawl/Stocks/Kospi/000020 동화약품.xlsx')
#wb.close
#pd.read_excel('./DataCrawl/Stocks/Kospi/'+i+'.xlsx', sheet_name = 'Price', header= 1)
#df.to_excel('./DataCrawl/Stocks/Kospi/'+i+'.xlsx', sheet_name='Price')

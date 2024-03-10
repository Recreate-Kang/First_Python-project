import OpenDartReader
import openpyxl
import os
from openpyxl import load_workbook
import pandas as pd
import csv
import matplotlib.pyplot as plt
from datetime import date, timedelta
import csv
import time
api_key= 'e70890fdd042d46e3926b3885ecb7b3f18f5c7a4'

dart = OpenDartReader(api_key)

#print(dart.list)
#bfefrmtrm_amount전전년
#frmtrm_amount 전년
#thstrm_amount 현년
Mk='Kospi'
Y =2022
Yx= 1
yearly= 12
#print(dart.list)
Pfile_list = os.listdir('./DataCrawl/Stocks/'+Mk+'/FSS')
NList=[]
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
#print(Pfile_name)
a=0


def Only_year(Dart_List):# 보고서명에서 보고일자만 추출
    Yr= int(Dart_List[-8:-1].replace('.',''))
    return Yr

def DF_sort(DF_List): #데이터프레임 리스트를 소팅함
    List =[]
#    print(type(x),'데이터프레임')
    for i in DF_List:
        if i.shape[0] > 10:
            List.append(i)
    #print(len(List))
    return List

def Rc_txt(Document): #공지 텍스트화

    F= open(".\DataCrawl\Stocks\Practice\Table\Rc.txt",'w')
    F.write(Document)
    F.close()

for i in Pfile_name[:1]: ##다트에서 종목코드로 제무제표 가져오기
    L=dart.list(i[:6], start='1999-01-01', end=str(date.today().strftime("%Y"+'-'+"%m"+'-'+"%d")), kind='A').loc[:,['report_nm','rcept_no']]
    L['report_nm']=L['report_nm'].apply(Only_year)
    L=(L.set_index('report_nm'))
    print(L)
    BY= max(L.index[-1]//100,Y-Yx) #재무제표가 원하는 기간에 없을시 존재하는 최대기간으로 설정
    L.to_csv('.\DataCrawl\Stocks\Practice\List.csv')

    Rc = L.loc[BY*100+yearly]['rcept_no'] #공시접수번호 가져오기
    #print(type(Rc))
    R_t= DF_sort(pd.read_html(dart.document(Rc)))
    Rc_txt(dart.document(Rc))
    a=0
    #print(type(R_t))

    for i in R_t:

        i.to_csv('.\DataCrawl\Stocks\Practice\Table\data'+str(a)+'.csv')
        a= a+1

#    for fY in range(BY,Y):
#    OBY= L['report_nm'].iloc[-1][-8:-1]#가장 오래된 재무재표 날짜
#   print(OBY//100)

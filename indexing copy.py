import OpenDartReader
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
Mk='Kospi'
Y =2020
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
print(Pfile_name)

for i in Pfile_name[:5]: ##다트에서 종목코드로 제무제표 가져오기
    A=dart.finstate_all(i[:6], Y)
    print(i)
    #print(A.bsns_year[2]) 보고서 년도
    if A is not None:
        a,b,c = int
        FAS = pd.read_csv('./DataCrawl\Stocks\A_subject.csv')#회계계정 정리
        CAS = pd.read_csv('./DataCrawl/Stocks/'+Mk+'/FSS/'+i+'.csv')
        #print(FAS)
        A=A.rename(columns={'thstrm_amount':A.bsns_year[2]})                      # 열 이름 변경
        TFAS =(FAS.loc[:,['sj_div','sj_nm','account_id','account_nm','ord']])
        AFAS = (A.loc[:,['sj_div','sj_nm','account_id','account_nm','ord']])
        FAS = pd.concat([TFAS,AFAS])
        FAS=FAS.loc[:,['sj_div','sj_nm','account_id','account_nm','ord']]
        FAS=FAS.drop_duplicates(['account_nm'])
        FAS= FAS.sort_values(by=['sj_div','ord'])
        FAS.to_csv('./DataCrawl\Stocks\A_subject.csv')
        print(type(A))
        A.to_csv('./DataCrawl/Stocks/'+Mk+'/FSS/'+i+'.csv')
        #DataCrawl\Stocks\Kospi\FSS\000020 동화약품.csv
# 나중에 일단 종목 정리부터함        A.to_csv(, sheet_name="FSS")
    if A is None:
        NList.append(i)
        print(i+'재무제표 X')
    time.sleep(0.1)

F= open("D:\Coding/DataCrawl/Stocks/daqNoneList.txt",'w')
for i in NList:
    F.write(i+'\n')
    F.close()



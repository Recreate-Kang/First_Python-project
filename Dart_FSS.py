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

sys.setrecursionlimit(10**7)
api_key= 'e70890fdd042d46e3926b3885ecb7b3f18f5c7a4'
dart.set_api_key(api_key=api_key)
api_key = dart.get_api_key()

#print(dart.list)
#bfefrmtrm_amount전전년
#frmtrm_amount 전년
#thstrm_amount 현년
Mk='Kospi'
Y =2022
Yx= 1
yearly= 12
#print(dart.list)





def Only_year(Dart_List):# 보고서명에서 보고일자만 추출
    Yr= int(Dart_List[-8:-1].replace('.',''))
    return Yr


def Rc_txt(Document): #공지 텍스트화

    F= open(".\DataCrawl\Stocks\Practice\Table\Rc.txt",'w')
    F.write(Document)
    F.close()


#A=crp_list.find_by_product(market='YK')
def crp_list(): #서버에 접속해 모든 공시목록 확인
    
    crp_list = get_corp_list()
    a=0
    Lists= []
    for i in crp_list:
        List= []
        a = a+1
        try:
            print((i.corp_code),'corp_code')
            List.append(i.corp_code)
        except:
            print('안됨corp_code')
        try:
            print(i.corp_name)
            List.append(i.corp_name)
        except:
            print('안됨corp_name')
        try:
            print(i.stock_code)
            List.append(i.stock_code)
        except:
            print('안됨stock_code')
        try:
            print(i.modify_date)
            List.append(i.modify_date)
        except:    
            print('안됨modify_date')
        Lists.append(List)
    df_Lists=pd.DataFrame(Lists, columns=['corp_code','corp_name','stock_code','modify_date'])
    df_Lists.to_csv('.\DataCrawl\Stocks\Practice\Lists.csv')
    print(a)
            
def Pcrp_list():#몇만개에서 공시 몇기업으로 추리는것
    #df= pd.read_csv('.\DataCrawl\Stocks\Practice\Lists.csv',index_col=0)
    df= pd.read_csv('.\DataCrawl\Stocks\Practice\PLists.csv',index_col=0)
    print(type(df['stock_code'][0]),df['stock_code'][0])
    drop = df[df['stock_code'].isnull()].index
    df.drop(drop, inplace=True)
    df.to_csv('.\DataCrawl\Stocks\Practice\aPLists.csv',index=False)
#2399
def compare_corp():
    List= []
    a=0
    f= open('DataCrawl\Kosdaq.txt')
    while True:
        
        line = f.readline().strip()
        if not line:break
        line = line.split(' ')[0]
        print(line)
        try:
            line = int(line)
            List.append(line)
        except:
            continue

    f= open('DataCrawl\Kospi.txt')
    while True:

        line = f.readline().strip()
        if not line:break
        line = line.split(' ')[0]
        print(line)
        try:
            line = int(line)
            List.append(line)
        except:
            continue
        print(line)
        List.append(line)
    print(List)
    df= pd.read_csv('DataCrawl\Stocks\PLists.csv')
    List2=df['stock_code'].to_list()
    a= list(set(List)&set(List2))
    print(type(a),len(a))
    F= open("D:\Coding/DataCrawl/inList.txt",'w')
    for i in a:
        F.write(str(i))
        F.write('\n')
    F.close()
    return a


def inPcrp_list(a:list):#교집합
    #df= pd.read_csv('.\DataCrawl\Stocks\Practice\Lists.csv',index_col=0)
    df= pd.read_csv('.\DataCrawl\Stocks\Practice\PLists.csv')
    df=df.assign(A="")
    for i in a:
        df.loc[df['stock_code']==i,'A']= True

    drop = df[df['A']!=True].index
    df.drop(drop, inplace=True)
    df.drop(['A'], inplace=True,axis=1)
    print(df.shape)
    df.to_csv('.\DataCrawl\Stocks\Practice\inPLists.csv',index=False)
    

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


def FFS_save():##저장####################
    Pfile_list = os.listdir('./DataCrawl\Stocks\FFS')
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

FFS_save()

#dart.fs.FinancialStatement.save(filename='00101628',path='\DataCrawl\Stocks\Practice')

""" def save(self, filename: str = None, path: str = None):
        
        재무제표 정보를 모두 엑셀파일로 일괄저장

        Parameters
        ----------
        filename: str
            저장할 파일명(default: {corp_code}_{report_tp}.xlsx)
        path: str
            저장할 폴더(default: 실행폴더/fsdata)

"""

"""
<class 'dart_fss.fs.fs.FinancialStatement'> {'bgn_de': '20200101',
'corp_code': '00101628',
'end_de': '20220901',
'financial statement': [{'title': '[D210000] Statement of financial position, '     
                        'current/non-current - Consolidated '
                        'financial statements (Unit: KRW)'},
                {'title': '[D310000] Income statement, by function of '     
                        'expense - Consolidated financial '
                        'statements (Unit: KRW)'},
                {'title': '[D410000] Statement of comprehensive '
                        'income - Consolidated financial statements '     
                        '(Unit: KRW)'},
                {'title': '[D520000] Statement of cash flows, '
                        'indirect method - Consolidated financial '       
                        'statements (Unit: KRW)'}],
'lang': 'ko',
'report_tp': ['annual'],
'separate': False,
'separator': True}
"""

"""
    재무제표 검색

    Parameters
    ----------
    corp_code: str
        공시대상회사의 고유번호(8자리)
    bgn_de: str
        검색 시작일자(YYYYMMDD)
    end_de: str, optional
        검색 종료일자(YYYYMMDD)
    fs_tp: tuple of str, optional
        'bs' 재무상태표, 'is' 손익계산서, 'cis' 포괄손익계산서, 'cf' 현금흐름표
    separate: bool, optional
        개별재무제표 여부
    report_tp: str or list, optional
        str: 'annual' 연간, 'half' 연간 + 반기, 'quarter' 연간 + 반기 + 분기
        list: ['annual'] : 연간, ['half']: 반기, ['quarter'] 분기, ['annual', 'half']: 연간 + 반기
            ['annual', 'quarter']: 연간 + 분기, ['half', 'quarter']:  반기 + 분기, ['annual', 'half', 'quarter']: 연간 + 반기 + 분기
    lang: str, optional
        'ko' 한글, 'en' 영문
    separator: bool, optional
        1000단위 구분자 표시 여부
    dataset: str, optional
        'xbrl': xbrl 파일 우선 데이터 추출, 'web': web page 우선 데이터 추출(default: 'xbrl')
    cumulative: bool, optional
        반기 혹은 분기 보고서 추출시 해당분기 값을 제외한 누적값만 추출할지 여부 (default: False)
    progressbar: bool, optional
        ProgressBar 표시 여부 (default: True)
    skip_error: bool, optional
        Error 발생시 skip 여부 (default: True)
    Returns
    -------
    FinancialStatement
        제무제표 검색 결과
"""
"""

def FSS()
    dart.extract_fs(self,
        bgn_de: str,
        end_de: str = None,
        fs_tp: Tuple[str] = ('bs', 'is', 'cis', 'cf'),
        separate: bool = False,
        report_tp: str = 'annual',
        lang: str = 'ko',
        separator: bool = True,
        dataset: str = 'xbrl',
        cumulative: bool = False,
        progressbar: bool = True,
        skip_error: bool = True) -> FinancialStatement:
"""

"""
        재무제표 검색

        Parameters
        ----------
        bgn_de: str
            검색 시작일자(YYYYMMDD)
        end_de: str, optional
            검색 종료일자(YYYYMMDD)
        fs_tp: tuple of str, optional
            'bs' 재무상태표, 'is' 손익계산서, 'cis' 포괄손익계산서, 'cf' 현금흐름표
        separate: bool, optional
            개별재무제표 여부
        report_tp: str, optional
            'annual' 1년, 'half' 반기, 'quarter' 분기
        lang: str, optional
            'ko' 한글, 'en' 영문
        separator: bool, optional
            1000단위 구분자 표시 여부
        dataset: str, optional
        'xbrl': xbrl 파일 우선 데이터 추출, 'web': web page 우선 데이터 추출(default: 'xbrl')
        cumulative: bool, optional


            반기 혹은 분기 보고서 추출시 해당분기 값을 제외한 누적값만 추출할지 여부 (default: False)
        progressbar: bool, optional
        ProgressBar 표시 여부 (default: True)
        skip_error: bool, optional
        Error 발생시 skip 여부 (default: True)
        Returns
        -------
        FinancialStatement
            제무제표 검색 결과
"""


"""
    corp_code: str
        종목 코드
    corp_name: str
        종목 이름
    stock_code: str
        주식 종목 코드
    modify_date: str
"""

"""
        self._corps = None
        self._corp_codes = dict()
        self._corp_names = []
        self._c = []
        self._corp_product = []
        self._corp_sector = []
        self._sectors = []

        self._stock_codes = dict()
        self._delisting = dict()
        self._stock_market = dict()
"""
"""    #objs = [{'name':'taewan'}, {'name':'sunny'}, {'name':'minsu'}]
    with open('.\DataCrawl\Stocks\Practice\crp_list.pkl', 'wb') as f:
        for a in crp_list:
            pickle.dump(a, f)
"""


#print(crp_list)
"""<bound method Corp.__dir__ of [00661759]신한관광개발>
# 삼성전자
samsung = corp_list.find_by_corp_name(corp_code=corp_code)

# 2012년 01월 01일 부터 연결재무제표 검색
# fs = samsung.extract_fs(bgn_de='20120101') 와 동일
fs = dart.fs.extract(corp_code=corp_code, bgn_de='20120101')

# 연결재무상태표
df_fs = fs['bs'] # 또는 df = fs[0] 또는 df = fs.show('bs')
# 연결재무상태표 추출에 사용된 Label 정보
labels_fs = fs.labels['bs']

# 연결손익계산서
df_is = fs['is'] # 또는 df = fs[1] 또는 df = fs.show('is')
# 연결손익계산서 추출에 사용된 Label 정보
labels_is = fs.labels['is']

# 연결포괄손익계산서
df_ci = fs['cis'] # 또는 df = fs[2] 또는 df = fs.show('cis')
# 연결포괄손익계산서 추출에 사용된 Label 정보
labels_ci = fs.labels['cis']

# 현금흐름표
df_cf = fs['cf'] # 또는 df = fs[3] 또는 df = fs.show('cf')
# 현금흐름표 추출에 사용된 Label 정보
labels_cf = fs.labels['cf']

# 재무제표 일괄저장 (default: 실행폴더/fsdata/{corp_code}_{report_tp}.xlsx)
fs.save()

# 재무제표 일괄저장
filename = '삼성전자'
path = '/User/xxxxx/Desktop/'
fs.save(filename=filename, path=path)

"""
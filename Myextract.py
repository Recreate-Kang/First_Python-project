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
#import dart_fss.filings.search_fillings as fill
#import dart_fss.filings.search as S
from dart_fss.filings import search as search_filings

sys.setrecursionlimit(10**7)
api_key= 'e70890fdd042d46e3926b3885ecb7b3f18f5c7a4'
dart.set_api_key(api_key=api_key)
api_key = dart.get_api_key()
#venv\Lib\site-packages\dart_fss\filings\search.py
#venv\Lib\site-packages\dart_fss\api\filings\search_filings.py
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

#a= ex.SearchResults

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

#compare_list()
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
#a=S.search(corp_code='00956028',bgn_de='20220101',end_de='20220901',last_reprt_at='N',sort='date')
a=search_filings(corp_cls='Y',bgn_de='20220701',end_de='20220901',last_reprt_at='N',sort='date',pblntf_ty='A',pblntf_detail_ty='A002')
print(type(a.report_list[0].corp_code),(a.report_list[0].corp_code))

#print(a)
#fill.search()
"""
def search(corp_code: str = None,
           bgn_de: str = None,
           end_de: str = None,
           last_reprt_at: str = 'N',
           pblntf_ty: str_or_list = None,
           pblntf_detail_ty: str_or_list = None,
           corp_cls: str = None,
           sort: str = 'date',
           sort_mth: str = 'desc', # 현재 sort_mth 설정시 오류 발생
           page_no: int = 1,
           page_count: int = 10):
    ----------
    corp_code: str, optional
        공시대상회사의 고유번호(8자리), 고유번호(corp_code)가 없는 경우 검색기간은 3개월로 제한
    bgn_de: str, optional
        검색시작 접수일자(YYYYMMDD), 없으면 종료일(end_de)
    end_de: str, optional
        검색종료 접수일자(YYYYMMDD), 없으면 당일
    last_reprt_at: str, optional
        최종보고서만 검색여부(Y or N), default : N
    pblntf_ty: str, optional
        공시유형 / Open DART  공시정보 -> 공시검색 -> 상세유형 참고
    pblntf_detail_ty: str, optional
        공시상세유형 / Open DART  공시정보 -> 공시검색 -> 상세유형 참고
    corp_cls: str, optional
        법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타), 없으면 전체조회
    sort: str, optional
        정렬, {접수일자: date, 회사명: crp, 고서명: rpt}
    sort_mth: str, optional
        오름차순(asc), 내림차순(desc), default : desc
    page_no: int, optional
        페이지 번호(1~n) default : 1
    page_count: int, optional
        페이지당 건수(1~100) 기본값 : 10, default : 100
"""
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


"""pblntf_ty = {
    "A": "정기공시",
    "B": "주요사항보고",
    "C": "발행공시",
    "D": "지분공시",
    "E": "기타공시",
    "F": "외부감사관련",
    "G": "펀드공시",
    "H": "자산유동화",
    "I": "거래소공시",
    "J": "공정위공시"
}

pblntf_detail_ty = {
    "A001": "사업보고서",
    "A002": "반기보고서",
    "A003": "분기보고서",
    "A004": "등록법인결산서류(자본시장법이전)",
    "A005": "소액공모법인결산서류",
    "B001": "주요사항보고서",
    "B002": "주요경영사항신고(자본시장법 이전)",
    "B003": "최대주주등과의거래신고(자본시장법 이전)",
    "C001": "증권신고(지분증권)",
    "C002": "증권신고(채무증권)",
    "C003": "증권신고(파생결합증권)",
    "C004": "증권신고(합병등)",
    "C005": "증권신고(기타)",
    "C006": "소액공모(지분증권)",
    "C007": "소액공모(채무증권)",
    "C008": "소액공모(파생결합증권)",
    "C009": "소액공모(합병등)",
    "C010": "소액공모(기타)",
    "C011": "호가중개시스템을통한소액매출",
    "D001": "주식등의대량보유상황보고서",
    "D002": "임원ㆍ주요주주특정증권등소유상황보고서",
    "D003": "의결권대리행사권유",
    "D004": "공개매수",
    "E001": "자기주식취득/처분",
    "E002": "신탁계약체결/해지",
    "E003": "합병등종료보고서",
    "E004": "주식매수선택권부여에관한신고",
    "E005": "사외이사에관한신고",
    "E006": "주주총회소집공고",
    "E007": "시장조성/안정조작",
    "E008": "합병등신고서(자본시장법 이전)",
    "E009": "금융위등록/취소(자본시장법 이전)",
    "F001": "감사보고서",
    "F002": "연결감사보고서",
    "F003": "결합감사보고서",
    "F004": "회계법인사업보고서",
    "F005": "감사전재무제표미제출신고서",
    "G001": "증권신고(집합투자증권-신탁형)",
    "G002": "증권신고(집합투자증권-회사형)",
    "G003": "증권신고(집합투자증권-합병)",
    "H001": "자산유동화계획/양도등록",
    "H002": "사업/반기/분기보고서",
    "H003": "증권신고(유동화증권등)",
    "H004": "채권유동화계획/양도등록",
    "H005": "수시보고",
    "H006": "주요사항보고서",
    "I001": "수시공시",
    "I002": "공정공시",
    "I003": "시장조치/안내",
    "I004": "지분공시",
    "I005": "증권투자회사",
    "I006": "채권공시",
    "J001": "대규모내부거래관련",
    "J002": "대규모내부거래관련(구)",
    "J004": "기업집단현황공시",
    "J005": "비상장회사중요사항공시",
    "J006": "기타공정위공시"
}

corp_cls = {
    "Y": "유가증권",
    "K": "코스",
    "N": "코넥스",
    "E": "etc"
}

rm = {
    "유": "본 공시사항은 한국거래소 유가증권시장본부 소관임",
    "코": "본 공시사항은 한국거래소 코스닥시장본부 소관임",
    "채": "본 문서는 한국거래소 채권상장법인 공시사항임",
    "넥": "본 문서는 한국거래소 코넥스시장 소관임",
    "공": "본 공시사항은 공정거래위원회 소관임",
    "연": "본 보고서는 연결부분을 포함한 것임",
    "정": "본 보고서 제출 후 정정신고가 있으니 관련 보고서를 참조하시기 바람",
    "철": "본 보고서는 철회(간주)되었으니 관련 철회신고서(철회간주안내)를 참고하시기 바람"
}"""
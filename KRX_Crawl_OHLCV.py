from pykrx import stock, bond
import matplotlib.pyplot as plt
import os
import pandas as pd
from datetime import date, timedelta
import csv

Mk= "Kosdaq"

#003230 삼양식품.xlsx

def OHLCV_save():##저장####################
    Stock_df= pd.read_csv('DataCrawl\Stocks\inPLists.csv')
    a=0
    fails=[]
    for i in Stock_df.itertuples():
        C_c= str(int(i[1]))
        C_c= C_c.rjust(8,'0')
        S_c= str(int(i[3]))
        S_c= S_c.rjust(6,'0')
        print(i[2],C_c,type(C_c),'시도중')
        try:
            df= stock.get_market_ohlcv("20100101", date.today().strftime("%Y"+"%m"+"%d"),S_c)
            df.to_csv('.\DataCrawl\Stocks\Price/'+S_c+'_'+i[2]+'.csv')
#'.\DataCrawl\Stocks\Practice\Table\data'+str(a)+'.csv'
        except:
            print(i[2],"실패")
            fails.append(i[2]+'_'+S_c)
            continue
    print(fails)
    F= open("D:\Coding/DataCrawl/PFails.txt",'w')
    F.Write(len(fails))
    for i in fails:
        F.write(i)
        F.write('\n')
    F.close()

OHLCV_save()


"""

for i in Pfile_name:
    #print(i[:6])
    print(i)
    df= stock.get_market_ohlcv("20220101", date.today().strftime("%Y"+"%m"+"%d"),i[:6])
    df.to_csv('./DataCrawl/Stocks/'+Mk+'/Price/'+i+'.csv')
    Price = pd.read_csv('./DataCrawl/Stocks/'+Mk+'/Price/'+i+'.csv')

print('Done!')
"""
"""

Price = pd.read_csv('./DataCrawl/Stocks/kospi/Price/'+i+'.csv')

##미래에 수정할 방식
class Copy_excel:
    def __init__(self,src):
        self.wb = load_workbook(src)
        #self.ws = self.wb.get_sheet_by_name("Sheet1") # Deprecated
        self.ws = self.wb["Sheet1"]
        self.dest="destination.xlsx"

    # Write the value in the cell defined by row_dest+column_dest         
    def write_workbook(self,row_dest,column_dest,value):
        c = self.ws.cell(row = row_dest, column = column_dest)
        c.value = value
    
    # Save excel file
    def save_excel(self) :  
        self.wb.save(self.dest)

"""
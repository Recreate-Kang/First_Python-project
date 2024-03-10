from pykrx import stock, bond
import matplotlib.pyplot as plt

api='297C5B5318F44A2F89B7B30C0D43059580B22C59'

tickers_kospi= stock.get_market_ticker_list(market="KOSPI")
tickers_kosdaq= stock.get_market_ticker_list(market="KOSDAQ")
print(len(tickers_kospi))
print(len(tickers_kosdaq))

F= open("D:\Coding/DataCrawl/Kospi.txt",'w')
for i in tickers_kospi:
    F.write(i+' ')
    F.write(stock.get_market_ticker_name(i))
    F.write('\n')
F.close()

F= open("D:\Coding/DataCrawl/Kosdaq.txt",'w')
for i in tickers_kosdaq:
    F.write(i+' ')
    F.write(stock.get_market_ticker_name(i))
    F.write('\n')
F.close()
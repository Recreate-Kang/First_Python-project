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
        FAS = pd.read_csv('./DataCrawl\Stocks\A_subject.csv')
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




"""
sj_div	sj_nm	account_id	account_nm
BS	재무상태표	ifrs-full_CurrentAssets	유동자산
BS	재무상태표	ifrs-full_CashAndCashEquivalents	현금및현금성자산
BS	재무상태표	dart_ShortTermDepositsNotClassifiedAsCashEquivalents	단기금융상품
BS	재무상태표	-표준계정코드 미사용-	단기투자자산
BS	재무상태표	dart_ShortTermTradeReceivable	매출채권
BS	재무상태표	ifrs-full_TradeAndOtherCurrentReceivables	기타수취채권
BS	재무상태표	ifrs-full_Inventories	재고자산
BS	재무상태표	ifrs-full_CurrentTaxAssets	당기법인세자산
BS	재무상태표	dart_OtherCurrentAssets	기타유동자산
BS	재무상태표	-표준계정코드 미사용-	기타금융자산
BS	재무상태표	ifrs-full_NoncurrentAssets	비유동자산
BS	재무상태표	ifrs-full_InvestmentsInSubsidiariesJointVenturesAndAssociates	관계기업 및 공동기업투자
BS	재무상태표	dart_LongTermTradeReceivablesGross	장기매출채권
BS	재무상태표	dart_NonCurrentAvailableForSaleFinancialAssets	장기투자자산
BS	재무상태표	dart_LongTermTradeAndOtherNonCurrentReceivablesGross	기타수취채권
BS	재무상태표	ifrs-full_OtherNoncurrentFinancialAssets	기타금융자산
BS	재무상태표	ifrs-full_PropertyPlantAndEquipment	유형자산
BS	재무상태표	ifrs-full_RightofuseAssets	사용권자산
BS	재무상태표	ifrs-full_IntangibleAssetsOtherThanGoodwill	무형자산
BS	재무상태표	ifrs-full_InvestmentProperty	투자부동산
BS	재무상태표	ifrs-full_DeferredTaxAssets	이연법인세자산
BS	재무상태표	-표준계정코드 미사용-	종업원급여자산
BS	재무상태표	dart_OtherNonCurrentAssets	기타비유동자산
BS	재무상태표	ifrs-full_Assets	자산총계
BS	재무상태표	ifrs-full_CurrentLiabilities	유동부채
BS	재무상태표	ifrs-full_TradeAndOtherCurrentPayables	매입채무
BS	재무상태표	dart_ShortTermOtherPayables	미지급금
BS	재무상태표	-표준계정코드 미사용-	기타지급채무
BS	재무상태표	ifrs-full_ShorttermBorrowings	차입금
BS	재무상태표	ifrs-full_CurrentProvisions	충당부채
BS	재무상태표	ifrs-full_CurrentTaxLiabilities	당기법인세부채
BS	재무상태표	ifrs-full_CurrentLeaseLiabilities	리스부채
BS	재무상태표	dart_OtherCurrentLiabilities	기타유동부채
BS	재무상태표	ifrs-full_NoncurrentLiabilities	비유동부채
BS	재무상태표	ifrs-full_OtherNoncurrentFinancialLiabilities	기타지급채무
BS	재무상태표	dart_LongTermBorrowingsGross	차입금
BS	재무상태표	dart_PostemploymentBenefitObligations	확정급여부채
BS	재무상태표	ifrs-full_DeferredTaxLiabilities	이연법인세부채
BS	재무상태표	ifrs-full_NoncurrentLeaseLiabilities	리스부채
BS	재무상태표	-표준계정코드 미사용-	기타금융부채
BS	재무상태표	dart_OtherNonCurrentLiabilities	기타비유동부채
BS	재무상태표	ifrs-full_Liabilities	부채총계
BS	재무상태표	ifrs-full_EquityAttributableToOwnersOfParent	지배기업의 소유지분
BS	재무상태표	ifrs-full_IssuedCapital	자본금
BS	재무상태표	dart_CapitalSurplus	자본잉여금
BS	재무상태표	dart_ElementsOfOtherStockholdersEquity	기타자본
BS	재무상태표	dart_OtherComprehensiveIncomeLossAccumulatedAmount	기타포괄손익누계액
BS	재무상태표	ifrs-full_RetainedEarnings	이익잉여금
BS	재무상태표	ifrs-full_NoncontrollingInterests	비지배지분
BS	재무상태표	ifrs-full_Equity	자본총계
BS	재무상태표	ifrs-full_EquityAndLiabilities	부채및자본총계
CIS	포괄손익계산서	ifrs-full_Revenue	매출액
CIS	포괄손익계산서	ifrs-full_CostOfSales	매출원가
CIS	포괄손익계산서	ifrs-full_GrossProfit	매출총이익
CIS	포괄손익계산서	dart_TotalSellingGeneralAdministrativeExpenses	판매비와관리비
CIS	포괄손익계산서	dart_OperatingIncomeLoss	영업이익
CIS	포괄손익계산서	ifrs-full_FinanceIncome	금융수익
CIS	포괄손익계산서	ifrs-full_FinanceCosts	금융비용
CIS	포괄손익계산서	-표준계정코드 미사용-	지분법투자 관련 손익
CIS	포괄손익계산서	dart_OtherGains	기타영업외수익
CIS	포괄손익계산서	dart_OtherLosses	기타영업외비용
CIS	포괄손익계산서	ifrs-full_ProfitLossBeforeTax	법인세비용차감전순이익
CIS	포괄손익계산서	ifrs-full_IncomeTaxExpenseContinuingOperations	법인세비용
CIS	포괄손익계산서	ifrs-full_ProfitLoss	당기순이익
CIS	포괄손익계산서	ifrs-full_OtherComprehensiveIncome	법인세차감후 기타포괄손익
CIS	포괄손익계산서	dart_OtherComprehensiveIncomeNetOfTaxGainsLossesOnRemeasurementsOfDefinedBenefitPlans	확정급여제도의 재측정요소
CIS	포괄손익계산서	ifrs-full_GainsLossesOnExchangeDifferencesOnTranslationNetOfTax	해외사업장환산외환차이(세후기타포괄손익)
CIS	포괄손익계산서	-표준계정코드 미사용-	파생금융상품평가손익
CIS	포괄손익계산서	-표준계정코드 미사용-	장기투자자산평가손익
CIS	포괄손익계산서	dart_ShareOfOtherComprehensiveIncomeOfAssociatesAndJointVenturesAccountedForUsingEquityMethodThatWillBeReclassifiedToProfitOrLossNetOfTax	관계기업의 기타포괄손익에 대한 지분
CIS	포괄손익계산서	ifrs-full_ComprehensiveIncome	총포괄손익
CIS	포괄손익계산서	ifrs-full_ProfitLossAttributableToOwnersOfParent	지배기업의 소유주지분
CIS	포괄손익계산서	ifrs-full_ProfitLossAttributableToNoncontrollingInterests	비지배지분
CIS	포괄손익계산서	ifrs-full_ComprehensiveIncomeAttributableToOwnersOfParent	지배기업의 소유주지분
CIS	포괄손익계산서	ifrs-full_ComprehensiveIncomeAttributableToNoncontrollingInterests	비지배지분
CIS	포괄손익계산서	ifrs-full_BasicEarningsLossPerShare	기본주당순이익
CIS	포괄손익계산서	ifrs-full_DilutedEarningsLossPerShare	희석주당순이익
CF	현금흐름표	ifrs-full_CashFlowsFromUsedInOperatingActivities	영업활동현금흐름
CF	현금흐름표	-표준계정코드 미사용-	영업으로부터 창출된 현금흐름
CF	현금흐름표	ifrs-full_InterestReceivedClassifiedAsOperatingActivities	이자의 수취
CF	현금흐름표	ifrs-full_InterestPaidClassifiedAsOperatingActivities	이자의 지급
CF	현금흐름표	ifrs-full_DividendsReceivedClassifiedAsOperatingActivities	배당금의 수취
CF	현금흐름표	ifrs-full_IncomeTaxesPaidRefundClassifiedAsOperatingActivities	법인세의 납부
CF	현금흐름표	ifrs-full_CashFlowsFromUsedInInvestingActivities	투자활동현금흐름
CF	현금흐름표	dart_PurchaseOfShortTermFinancialInstruments	단기금융상품의 순증감
CF	현금흐름표	-표준계정코드 미사용-	단기투자자산의 순증감
CF	현금흐름표	dart_ProceedsFromSalesOfOtherFinancialAssets	기타금융자산의 감소
CF	현금흐름표	dart_PurchaseOfOtherFinancialAssets	기타금융자산의 증가
CF	현금흐름표	dart_ProceedsFromSalesOfLoansAndReceivables	기타수취채권의 감소
CF	현금흐름표	dart_PurchaseOfLoansAndReceivables	기타수취채권의 증가
CF	현금흐름표	dart_ProceedsFromSalesOfAvailableForSaleFinancialAssets	장기투자자산의 처분
CF	현금흐름표	dart_PurchaseOfAvailableForSaleFinancialAssets	장기투자자산의 취득
CF	현금흐름표	-표준계정코드 미사용-	파생상품거래로 인한 현금유입
CF	현금흐름표	-표준계정코드 미사용-	파생상품거래로 인한 현금유출
CF	현금흐름표	ifrs-full_ProceedsFromSalesOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities	유형자산의 처분
CF	현금흐름표	ifrs-full_PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities	유형자산의 취득
CF	현금흐름표	ifrs-full_ProceedsFromSalesOfIntangibleAssetsClassifiedAsInvestingActivities	무형자산의 처분
CF	현금흐름표	ifrs-full_PurchaseOfIntangibleAssetsClassifiedAsInvestingActivities	무형자산의 취득
CF	현금흐름표	ifrs-full_ProceedsFromGovernmentGrantsClassifiedAsInvestingActivities	정부보조금의 수취
CF	현금흐름표	-표준계정코드 미사용-	관계기업투자의 취득
CF	현금흐름표	-표준계정코드 미사용-	종속기업투자의 취득
CF	현금흐름표	-표준계정코드 미사용-	사업결합으로 인한 순현금유출
CF	현금흐름표	ifrs-full_CashFlowsFromUsedInFinancingActivities	재무활동현금흐름
CF	현금흐름표	ifrs-full_ProceedsFromBorrowingsClassifiedAsFinancingActivities	차입금의 차입
CF	현금흐름표	ifrs-full_RepaymentsOfBorrowingsClassifiedAsFinancingActivities	차입금의 상환
CF	현금흐름표	ifrs-full_PaymentsOfFinanceLeaseLiabilitiesClassifiedAsFinancingActivities	리스부채의 상환
CF	현금흐름표	dart_AcquisitionOfTreasuryShares	자기주식의 취득
CF	현금흐름표	ifrs-full_DividendsPaidClassifiedAsFinancingActivities	배당금의 지급
CF	현금흐름표	-표준계정코드 미사용-	비지배지분의 증가
CF	현금흐름표	ifrs-full_EffectOfExchangeRateChangesOnCashAndCashEquivalents	현금및현금성자산의 환율변동효과
CF	현금흐름표	ifrs-full_IncreaseDecreaseInCashAndCashEquivalents	현금및현금성자산의 순증감
CF	현금흐름표	dart_CashAndCashEquivalentsAtBeginningOfPeriodCf	기초 현금및현금성자산
CF	현금흐름표	dart_CashAndCashEquivalentsAtEndOfPeriodCf	기말 현금및현금성자산
SCE	자본변동표	dart_EquityAtBeginningOfPeriod	기초자본
SCE	자본변동표	dart_EquityAtBeginningOfPeriod	기초자본
SCE	자본변동표	dart_EquityAtBeginningOfPeriod	기초자본
SCE	자본변동표	dart_EquityAtBeginningOfPeriod	기초자본
SCE	자본변동표	dart_EquityAtBeginningOfPeriod	기초자본
SCE	자본변동표	dart_EquityAtBeginningOfPeriod	기초자본
SCE	자본변동표	dart_EquityAtBeginningOfPeriod	기초자본
SCE	자본변동표	dart_EquityAtBeginningOfPeriod	기초자본
SCE	자본변동표	ifrs-full_ProfitLoss	당기순이익
SCE	자본변동표	ifrs-full_ProfitLoss	당기순이익
SCE	자본변동표	ifrs-full_ProfitLoss	당기순이익
SCE	자본변동표	ifrs-full_ProfitLoss	당기순이익
SCE	자본변동표	ifrs-full_IncreaseDecreaseThroughChangesInAccountingPolicies	확정급여제도의 재측정요소
SCE	자본변동표	ifrs-full_IncreaseDecreaseThroughChangesInAccountingPolicies	확정급여제도의 재측정요소
SCE	자본변동표	ifrs-full_IncreaseDecreaseThroughChangesInAccountingPolicies	확정급여제도의 재측정요소
SCE	자본변동표	-표준계정코드 미사용-	장기투자자산평가손익
SCE	자본변동표	-표준계정코드 미사용-	장기투자자산평가손익
SCE	자본변동표	-표준계정코드 미사용-	장기투자자산평가손익
SCE	자본변동표	dart_OtherComprehensiveIncomeForStatementOfChangesInEquity	관계기업의 기타포괄손익에 대한 지분
SCE	자본변동표	dart_OtherComprehensiveIncomeForStatementOfChangesInEquity	관계기업의 기타포괄손익에 대한 지분
SCE	자본변동표	dart_OtherComprehensiveIncomeForStatementOfChangesInEquity	관계기업의 기타포괄손익에 대한 지분
SCE	자본변동표	-표준계정코드 미사용-	파생상품평가손익
SCE	자본변동표	-표준계정코드 미사용-	파생상품평가손익
SCE	자본변동표	-표준계정코드 미사용-	파생상품평가손익
SCE	자본변동표	dart_ChangesInForeignExchangeRates	해외사업장환산외환차이
SCE	자본변동표	dart_ChangesInForeignExchangeRates	해외사업장환산외환차이
SCE	자본변동표	dart_ChangesInForeignExchangeRates	해외사업장환산외환차이
SCE	자본변동표	dart_ChangesInForeignExchangeRates	해외사업장환산외환차이
SCE	자본변동표	dart_TreasuryShareTransactions	자기주식 취득
SCE	자본변동표	dart_TreasuryShareTransactions	자기주식 취득
SCE	자본변동표	dart_TreasuryShareTransactions	자기주식 취득
SCE	자본변동표	-표준계정코드 미사용-	비지배지분의 증가
SCE	자본변동표	-표준계정코드 미사용-	비지배지분의 증가
SCE	자본변동표	ifrs-full_DividendsPaid	배당금지급
SCE	자본변동표	ifrs-full_DividendsPaid	배당금지급
SCE	자본변동표	ifrs-full_DividendsPaid	배당금지급
SCE	자본변동표	dart_ShareBasedPaymentTransactions	주식선택권 부여
SCE	자본변동표	dart_ShareBasedPaymentTransactions	주식선택권 부여
SCE	자본변동표	dart_ShareBasedPaymentTransactions	주식선택권 부여
SCE	자본변동표	ifrs-full_Equity	기말자본
SCE	자본변동표	ifrs-full_Equity	기말자본
SCE	자본변동표	ifrs-full_Equity	기말자본
SCE	자본변동표	ifrs-full_Equity	기말자본
SCE	자본변동표	ifrs-full_Equity	기말자본
SCE	자본변동표	ifrs-full_Equity	기말자본
SCE	자본변동표	ifrs-full_Equity	기말자본
SCE	자본변동표	ifrs-full_Equity	기말자본
SCE	자본변동표	-표준계정코드 미사용-	기업회계기준서 제 1109호 최초적용에 따른 조정
SCE	자본변동표	-표준계정코드 미사용-	기업회계기준서 제 1109호 최초적용에 따른 조정
			
"""
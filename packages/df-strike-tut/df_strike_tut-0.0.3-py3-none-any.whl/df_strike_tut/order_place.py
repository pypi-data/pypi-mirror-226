
from py5paisa.order import Order, OrderType, Exchange
import pandas as pd
import time as tym
from datetime import datetime, date, time
import pytz # for timezone

def order_place(client, iDict, oDict):
    ########## ORDER PLACEMENT BUY/SELL AND STOPLOSS#########

    entry_time=iDict['entry_time']
    num_strikes=iDict['num_strikes']
    expiry=iDict['expiry'] 
    Buy_prm_closest=iDict['Buy_prm_closest']
    Delay_buy=iDict['Delay_buy'] 
    Sell_prm_closest=iDict['Sell_prm_closest'] 
    Scripcode_BN=iDict['Scripcode_BN'] 
    qty=iDict['qty']   
    
    CE_Scripcode_BUY=oDict['CE_Scripcode_BUY']
    PE_Scripcode_BUY=oDict['PE_Scripcode_BUY']
    CE_Scripcode_SELL=oDict['CE_Scripcode_SELL']
    PE_Scripcode_SELL=oDict['PE_Scripcode_SELL']
    
    print("orderplaced")
#         client.place_order(OrderType='B',Exchange='N',ExchangeType='D', 
#                     ScripCode= int(CE_Scripcode_BUY), 
#                     Qty=qty, DisQty=qty, IsIntraday= False, IsStopLossOrder= False, 
#                         StopLossPrice=0, Price= 0)   ## To place CE Buy

    tym.sleep(Delay_buy) #to add delay between sell and sell
#         client.place_order(OrderType='S',Exchange='N',ExchangeType='D', 
#                     ScripCode = int(PE_Scripcode_SELL), 
#                     Qty=qty, DisQty=qty, IsIntraday= False, IsStopLossOrder= False, 
#                         StopLossPrice=0, Price= 0) ## To place PE Sell
    print("orderplaced")
    tym.sleep(20)

    #################### Placing Stoploss Order ######################


    df_pos=pd.json_normalize(client.positions())
    for i in range(len(df_pos.index)):
        if df_pos['SellQty'][i]>0:
            print("client.place_order(OrderType='B',ScripCode = int(df_pos['ScripCode'][i]))")
            print(int(df_pos['ScripCode'][i]))
            print(int(round(df_pos['SellAvgRate'][i]*2.1,0)))
            print("next sl order...")



# Request details
## OrderType: B-Buy, S- Sell
## Exchange: N- NSE, B- BSE, M- Mcx
## ExchangeType: C- Cash, D- Derivative, U-Currency
## ScripCode: Refer to scrip master file.
## Qty: No. of units to trade
## Price: Price at which order is to be placed. If Price is set 0, Order is treated as market order.
## IsIntraday: True/False
## IsStopLossOrder: True/False
## StopLossPrice: Trigger Price to be set. If Stop Loss Price is set  0, Order becomes Stop Loss Order). 
                                                                                #This is non complusory input.
## AHPlaced: After Market order confirmation. Y: Yes, N: No

#Response details: 
##BrokerOrderID: BrokerOrderID of order placed
##ClientCode: ClientCode passed in request
##Exch: Exchange passed in request, N- NSE, B- BSE, M- Mcx
##ExchOrderID: it comes as zero RMS doesnt send Exchange order ID
##ExchType: Exchange Type passed in request, C- Cash, D- Derivative, U-Currency
##LocalOrderID: OrderID passed in request
##Message: Error Message
##RMSResponseCode: RMSResponseCode
##RemoteOrderID: 
##Scripcode: Scripcode passed in request
##status: status of order request
##time: order placed time




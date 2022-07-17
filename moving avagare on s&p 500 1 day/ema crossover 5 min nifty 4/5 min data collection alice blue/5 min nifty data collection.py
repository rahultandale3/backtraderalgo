# import dateutil.parser
from alice_blue import *
import requests , json
from dateutil.parser import parse
from datetime import datetime , timedelta
import pandas as pd




username = '284483'
password = 'Kisangita@09'
twoFA = '2001'
app_id = 'juaXFmGuqN'
api_secret = '5DsI0iPAv69J5tRqP7LCdHZQaYqTI5wPfxVYcMKpRjPMELbp5YzFUjgyWz2speaj'


access_token = 'EGTbSm3m1QW1y9pLyP56MNTdsbanjf9X7oohuKUyZ6E.KEswZ8X0Hppkj0F-zbvi25e_RnCjNx3Q1sH0w3KFFKg'
alice = AliceBlue(username=username, password=password, access_token=access_token)

'''below useing trick is may be not legal but , i dont hade any other option so i decided to collect data from this way 
steps to get that data 
i got this data from alice blue website my be this is not leggal 
login to the alice blue trading accout 
open a chart anyone you want 
click on f12 crome devloper tool will open 
click on network 
https://drive.google.com/file/d/1yYdbyR2wrsToP092p9_Qq6lPNkc4dD42/view?usp=sharing

click on xhr , header , copy the link of cherd

link will be like this
https://ant.aliceblueonline.com/api/v1/charts/tdv?exchange=NSE_INDICES&token=26000&candletype=1&starttime=1577836801&endtime=1654272000&data_duration=15  duration 15 is 15 minute candle for one minite i will say duration=1'''

def get_historical(instrument, f_date, to_date, interval, indices = False):
    params = { "token" : instrument.token ,
               "exchange " : instrument.exchange if not indices else "NSE _INDICES",
               "starttime" : str(int(f_date.timestamp())),
               "endtime" : str(int(to_date.timestamp())),
               "candletype" : 3 if interval.upper() == "DAY" else (2 if interval.upper().split("_")[1]=="HR" else 1 ),
               "data_duration":  None if interval.upper() ==  "DAY"  else interval.split("_")[0] }

    # below ls time stap date is 13-5-2022
    # lst = requests.get(f"https://ant.aliceblueonline.com/api/v1/charts/tdv?exchange=NSE_INDICES&token=26000&candletype=1&starttime=1652293800&endtime=1654229436&data_duration=15" , params= params).json()["data"]["candles"]

    # below lst time stap date is 7-9-2019 but data availbale is from 04-01-2021
    lst = requests.get(f"https://ant.aliceblueonline.com/api/v1/charts/tdv?exchange=NSE_INDICES&token=26000&candletype=1&starttime=1567836801&endtime=1657814400&data_duration=5" , params= params).json()["data"]["candles"]
    # print(lst)
    print(len(lst))
    records = []
    # for item in lst:
    #     print(f"{item}")
    for i in lst :
        record = {"date ": i[0], "open ": i[1], "high": i[2], "low": i[3], "close": i[4], "volume": i[5]}
        records.append(record)
    return records

        # record = {"date ": dateutil.parser.parse(i[0]),"open ":i[1],"high":i[2] ,"low":i[3] ,"close":i[4] ,"volume":i[5]}








instrument = alice.get_instrument_by_symbol("NSE","Nifty 50")
f_date = datetime.now()-timedelta(days=100)
to_date=datetime.now()
interval = "5_MIN" #[DAY , 1_HR , 5_MIN , 15_MIN , 60_MIN ]
indices = True
# a  = get_historical(instrument,f_date,to_date, interval, indices)
# print(a)
df = pd.DataFrame(get_historical(instrument,f_date,to_date, interval, indices))
# df =df.reset_index()
# df = pd.DataFrame(a)
# df.index= df["date"]
# df = df.drop("date", axis=1)
print(df)
# df.to_csv("E:\\algo trading\\historical data\\da overall_data_[5_minute_nifty_50]_04_1_21_to_14_7_22.csv", index=False)
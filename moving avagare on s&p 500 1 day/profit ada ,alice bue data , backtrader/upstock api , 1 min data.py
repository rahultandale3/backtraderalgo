
import pandas as pd
from upstox_api.api import*
from datetime import datetime

api_key=open('api_key.txt','r').read()
access_token=open('access_token.txt','r').read().strip()
u=Upstox(api_key,access_token)
master_contract=u.get_master_contract('nse_eq')
master_contract=pd.DataFrame(master_contract)
exchange='nse_eq'
tradingsymbol='reliance'
from_date='01/09/2018'
now=datetime.now()
to_date=datetime.strftime(now,'%d/%m/%Y')

data=u.get_ohlc(u.get_instrument_by_symbol(exchange,tradingsymbol),OHLCInterval.Minute_1,
datetime.strptime('%s'%(from_date),'%d/%m/%Y').date(),datetime.strptime('%s'%(to_date),'%d/%m/%Y').date())
data=pd.DataFrame(data)
data['timestamp']=pd.to_datetime(data['timestamp'],unit='ms')
data['timestamp']=data['timestamp'].dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata')
data.set_index('timestamp',inplace=True)
data.to_csv('RELIANCE_'+str(datetime.now().strftime('%Y_%m_%d')),date_format='%Y-%m-%d %H:%M:%S')
print(data)
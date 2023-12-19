import akshare as ak
from sqlalchemy import create_engine

host = '192.168.1.1'
port = 3308
db = 'wt_tools_0922'
user = 'wt_tools_0922'
password = '06my4ta'
engine = create_engine('mysql://wt_tools_0922:06my4ta@47.242.240.239:3308/wt_tools_0922?charset=utf8mb4')
try:
    tool_trade_date_hist_sina_df = ak.tool_trade_date_hist_sina()
    tool_trade_date_hist_sina_df.rename(columns={"trade_date": "cal_date"}, inplace=True)
    tool_trade_date_hist_sina_df.insert(loc=1, column='exchange', value='SSE')
    tool_trade_date_hist_sina_df.insert(loc=2, column='is_open', value=1)
    # tool_trade_date_hist_sina_df.insert(loc=3, column='pretrade_date')
    tool_trade_date_hist_sina_df.tail(242).to_sql('trade_cal', con=engine, if_exists='append', index=False)
    print(tool_trade_date_hist_sina_df.tail(242))
except Exception as e:
   print(e)


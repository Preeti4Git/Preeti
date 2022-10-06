import json
import boto3
import yfinance as yf
import datetime


# Your goal is to get per-hour stock price data for a time range for the ten stocks specified in the doc. 
# Further, you should call the static info api for the stocks to get their current 52WeekHigh and 52WeekLow values.
# You should craft individual data records with information about the stockid, price, price timestamp, 52WeekHigh and 52WeekLow values and push them individually on the Kinesis stream

kinesis = boto3.client('kinesis', region_name = "us-east-1") #Modify this line of code according to your requirement.

my_stream_name = 'StockPriceIngestionLogsStream'

def put_to_stream(ticker, price, price_timestamp, fiftyTwoWeekHigh, fiftyTwoWeekLow):
    payload = {
                'stockid': ticker,
                'price': price,
                'price_timestamp': str(price_timestamp),
                'fiftyTwoWeekHigh': fiftyTwoWeekHigh,
                'fiftyTwoWeekLow': fiftyTwoWeekLow
              }

    print(payload)

    put_response = kinesis.put_record(
                        StreamName=my_stream_name,
                        Data=json.dumps(payload),
                        PartitionKey=ticker)




today = datetime.date.today()
yesterday = datetime.date.today() - datetime.timedelta(3)

# Example of pulling the data between 2 dates from yfinance API
#data = yf.download(tickers = "MSFT MVIS, GOOG, SPOT, INO, OCGN, ABML, RLLCF, JNJ, PSFE", start= yesterday, end= today, interval = '1h')#,group_by = 'ticker' )
#print(data.Close)

for ticker in ("MSFT","MVIS","GOOG","SPOT","INO","OCGN","ABML","RLLCF","JNJ","PSFE"):
    stock = yf.Ticker(ticker)
    data = yf.download(tickers=ticker, start=yesterday, end=today, interval='1h')
    len = data.Close.index.size
    for i in range(len):
        price_timestamp = data.Close.index[i]
        price = data.Close.values[i]
        fiftyTwoWeekHigh = stock.info['fiftyTwoWeekHigh']
        fiftyTwoWeekLow = stock.info['fiftyTwoWeekLow']
        put_to_stream(ticker, price, price_timestamp, fiftyTwoWeekHigh, fiftyTwoWeekLow)

## Add code to pull the data for the stocks specified in the doc


## Add additional code to call 'info' API to get 52WeekHigh and 52WeekLow refering this this link - https://pypi.org/project/yfinance/


## Add your code here to push data records to Kinesis stream.


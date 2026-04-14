import urllib.request
import json
import csv
import sys
import codecs
from datetime import datetime

url = "https://api.binance.com/api/v3/klines?symbol=PAXGUSDT&interval=1d&limit=1000"
try:
    print("Fetching 1000 days of Spot Gold (PAXG) data from Binance...")
    req = urllib.request.urlopen(url)
    data = json.loads(req.read())
    
    with codecs.open("NEW_GOLD.csv", "w", encoding='utf-8') as f:
        writer = csv.writer(f)
        # Date, Open, High, Low, Close, Adj Close, Volume
        writer.writerow(["Date", "Open", "High", "Low", "Close", "Adj_Close", "Volume"])
        
        idx = 0
        for kline in data:
            # kline[0] is timestamp
            date_time = datetime.fromtimestamp(kline[0] / 1000.0).strftime('%Y-%m-%d')
            writer.writerow([date_time, kline[1], kline[2], kline[3], kline[4], kline[4], kline[5]])
            idx += 1
            
    print(f"Successfully wrote {idx} records to NEW_GOLD.csv.")
except Exception as e:
    print(f"Error fetching data: {e}")
    sys.exit(1)

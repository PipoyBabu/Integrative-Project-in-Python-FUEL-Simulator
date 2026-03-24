import requests
from datetime import datetime, timedelta

end_date = datetime.now()
start_date = end_date - timedelta(days=30)
url = (
    f"https://api.exchangerate.host/timeseries"
    f"?start_date={start_date.strftime('%Y-%m-%d')}"
    f"&end_date={end_date.strftime('%Y-%m-%d')}"
    f"&base=USD&symbols=PHP"
)
response = requests.get(url)
data = response.json()
print(data)
import requests
import pandas as pd
from io import StringIO

session = requests.Session()
url = "https://api.tgju.org/v1/market/indicator/summary-table-data/geram18" 

params = {
    "lang": "fa",
    "order_dir": "asc",
    "draw": 3,
    "start": 0,
    "length": 1000000000000000000000000000000000,
    "search": "",
    "order_col": "",
    "from": "1405/01/01",
    "to": "",
    "convert_to_ad": 1,
}


try:
    response = session.get(url=url, 
                           params=params,
                           timeout=5)
    response.raise_for_status()
    print(response.status_code)
except requests.RequestException as e:
    print(e)
else:
    data = response.json()
    df = pd.DataFrame(data['data'])
    print(df)
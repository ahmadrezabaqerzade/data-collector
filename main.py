import requests
import pandas as pd
from io import StringIO

session = requests.Session()
url = "https://www.tgju.org/profile/geram18/history"


try:
    response = session.get(url=url, timeout=5)
    response.raise_for_status()
    print(response.status_code)
except requests.RequestException as e:
    print(e)
else:
    print("Contains table:", "<table" in response.text)
    tables = pd.read_html(StringIO(response.text))
    print(len(tables))
    tables[0].to_csv('info.csv')
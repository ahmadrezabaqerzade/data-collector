import requests
import pandas as pd
import json
import time 


class BaseDataCollector:
    def __init__(self, timeout=5, max_try=1, try_delay=1):
        self.session = requests.Session()
        self.timeout = timeout
        self.max_try = max_try
        self.try_delay = try_delay

    def collect(self, url, params):
        return self.get_response(url, params, self.max_try)

    def get_response(self, url, params, try_number):
        if try_number == 0:
            return None 
        try:
            print(f"Try->{self.max_try-try_number+1}")
            response = self.session.get(url=url,
                                params=params,
                                timeout=self.timeout)
            response.raise_for_status()
            return response 
        except requests.RequestException as e:
            print("Something Went Wrong")
            print(e)
            time.sleep(self.try_delay)
            return self.get_response(url, params, try_number-1)

class TGJUDataCollector(BaseDataCollector):
    def __init__(self, param, timeout=5, max_try=1, try_delay=1):
        super().__init__(timeout=timeout, max_try=max_try, try_delay=try_delay)
        self.param = param

    def collect(self, url, params=None):
        response = super().collect(url, params)
        try:
            data = response.json()
            df = pd.DataFrame(data[self.param])
            return df
        except json.JSONDecodeError as e:
            print(e)


url = "https://api.tgju.org/v1/market/indicator/summary-table-data/geram18" 
timeout = 5
max_try = 5
params = {
    "lang": "fa",
    "order_dir": "asc",
    "draw": 3,
    "start": 0,
    "length": 10000,
    "search": "",
    "order_col": "",
    "from": "1405/01/01",
    "to": "",
    "convert_to_ad": 1,
}

data_collector = TGJUDataCollector('data', timeout=timeout, max_try=max_try)
data = data_collector.collect(url=url, params=params)
print(data)
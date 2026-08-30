import requests
import pandas as pd
import json
import re 
import time 


def clean_value(x):
    """
    remove the HTML while preserving the underlying numeric type (int/float)
    """
    if isinstance(x, str):
        matches = re.search(r".*>([\d\.]+).*<.*", x)
        if matches:
            x = matches.group(1)
        elif "," in x:
            x = x.replace(",", "")
        try:
            x = float(x) if "." in x else int(x)
        except:
            None 
    return x

class BaseDataCollector:
    def __init__(self, timeout=5, max_retries=1, try_delay=1):
        self.session = requests.Session()
        self.timeout = timeout
        self.max_retries = max_retries
        self.try_delay = try_delay

    def collect(self, url, params):
        return self.get_response(url, params, self.max_retries)

    def get_response(self, url, params, try_number):
        if try_number == 0:
            return None 
        try:
            print(f"Try->{self.max_retries-try_number+1}")
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
    def __init__(self, timeout=5, max_retries=1, try_delay=1):
        super().__init__(timeout=timeout, max_retries=max_retries, try_delay=try_delay)

        self._url = "https://api.tgju.org/v1/market/indicator/summary-table-data/geram18" 
        self._params = {
                    "lang": "fa", "order_dir": "asc", "draw": 3, "start": 0,
                    "length": None, "search": "", "order_col": "", "from": "", "to": "",
                    "convert_to_ad": 1,
                }
        self._columns = ["Open",
                         "Low",
                         "High",
                         "Close",
                         "Change",
                         "Change Percent",
                         "Date / Gregorian",
                         "Date / Solar Hijri"]

    def collect(self, start_date:str = "", end_date:str = ""):
        self._params["from"] = start_date
        self._params["to"] = end_date
        response = super().collect(self._url, self._params)
        try:
            data = response.json()
            df = pd.DataFrame(data['data']).map(clean_value)
            df.columns = self._columns
            return df
        except json.JSONDecodeError as e:
            print(e)
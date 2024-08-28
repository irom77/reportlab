import requests # type: ignore
import pandas as pd # type: ignore
import urllib3 # type: ignore
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os
from dotenv import load_dotenv # type: ignore
from datetime import datetime
import calendar

load_dotenv()

class ProofpointAPIClient:
    # https://help.proofpoint.com/Threat_Insight_Dashboard/API_Documentation/SIEM_API
    def __init__(self, conf):        
        self.sp = os.getenv('sp')  # Replace with your actual service principal
        self.api_key = os.getenv('api_key')  # Replace with your actual API key
        self.base_url = 'https://tap-api-v2.proofpoint.com/v2/siem'
        self.headers = {}
        self.params = {
            'sinceSeconds': 3600,
            'threatStatus': 'active',
            'format': 'json'
        }
        self.df = None
        self.conf = conf

    def inbound_messages(self):
        now = datetime.now()
        report_month = datetime.strptime(self.conf.report.month, '%B')
        year = now.year if report_month.month <= now.month else now.year - 1
        month = report_month.month
        _, last_day = calendar.monthrange(year, month)
        
        # Calculate the number of seconds from the start of the month to now
        start_date = datetime(year, month, 1)
        end_date = min(datetime(year, month, last_day, 23, 59, 59), now)
        seconds_since_start = int((end_date - start_date).total_seconds())
        
        params = {
            'sinceSeconds': seconds_since_start,
            'format': 'json'
        }
        
        response = requests.get(
            url=f"{self.base_url}/all",
            auth=(self.sp, self.api_key),
            headers=self.headers,
            params=params,
            verify=False
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get('messagesDelivered', 0)
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return 0

    def messages_blocked(self):
        response = requests.get(url=self.base_url+'/messages/blocked', auth=(self.sp, self.api_key), headers=self.headers, params=self.params, verify=False)
        json_data = response.json()
        print(f"{len(json_data['messagesBlocked'])} messages blocked")
        if response.status_code == 200:
            events = json_data['messagesBlocked']
            self.df = pd.DataFrame(events)
        else:
            print(f"Error: {response.status_code} - {response.text}")
            self.df = pd.DataFrame()
        self.df['threatType'] = self.df['threatsInfoMap'].apply(lambda x: x[0]['threatType'])
        return self.df[["spamScore", "phishScore", "threatType"]].head(3)

import requests # type: ignore
import pandas as pd # type: ignore
import urllib3 # type: ignore
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os
from dotenv import load_dotenv # type: ignore

load_dotenv()

class ProofpointAPIClient:

    def __init__(self):        
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
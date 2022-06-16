import requests
from bs4 import BeautifulSoup
import os

env_var = os.environ

url = env_var['URL']

def scrap(data_to_srap):
    if data_to_srap == None:
        return None, False
    try:
        r = requests.get(url, auth=(env_var['USR'], env_var['PASS'])) 

        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
        
            current_power = soup.findAll('script')[1].text
            current_power = current_power.split(f"{data_to_srap} = \"")[1].split("\";")[0]
            
            return current_power, True
    except:
        return None, False
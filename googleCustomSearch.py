import requests
import time
import pandas as pd
import json



with open('API.txt','r') as content:
    keys = {}
    #content = 
    for line in content:    
        ky,val = line.strip().split("=",1)
        keys[ky] = val
       

API_KEY = keys["API_KEY"]
SEARCH_ENGINE_ID = keys["CUSTOMER_ENGINE_ID"]



df = pd.read_csv(r'products-2.csv')

def enrich_product(data):

    '''Retrieving information based on product name'''

    query = f"{data}"

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query,
        "num":10
    }
    
    response = requests.get(url, params=params)
    data = response.json()

        
    if "items" not in data:
        return {"error": "No results found"}
    
    results = data["items"]

    return results


enriched_data = {}

count = 1
for title,product_url,brd in zip(df['product_name'],df['product_url'],df['brand']):    
    
    product_id = product_url.split("/")[-1]
    enriched_info = enrich_product(title)
    enriched_data[product_id] = enriched_info

'''Saving the dictonary data in json file for data validation '''

with open("final_output-5.json","w") as f:
    json.dump(enriched_data,f,indent=4)



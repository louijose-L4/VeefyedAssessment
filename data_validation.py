import pandas as pd
import json
import re

def manfacturer_website(brd,itm):

    '''VALIDATNG THE MANFACTURING WEBSITE WITH  BRAND'''

    org_brand = str(itm["displayLink"])   
    cleaned = re.sub(r"[^A-Za-z]", "", brd)
    cleaned = cleaned.lower()        
    if cleaned in org_brand:
        return True
    else:
        False

def dataExtract(itm): 
    '''EXTRACTING DATA FROM METATAGS INSIDE THE JSON FILE'''

    if "pagemap" in itm:
        if "metatags" in itm["pagemap"]:
            raw_data = itm["pagemap"]['metatags'][0]
            try:
                title = raw_data["og:title"]
            except:
                title = itm["title"]
            try:    
                url = raw_data["og:url"]
            except:
                url = itm['link']
            try:
                desc = raw_data["og:description"]
            except:
                desc = itm["snippet"]
            return url,title,desc
    else:
        "","",""

 




with open ('final_output-5.json','r') as file:
    data = json.load(file)

df = pd.read_csv('products-2.csv')

item_dic = {}
counter = 1
for ind, row in df.iterrows():
    item = row["product_url"]
    brd = row["brand"]
    name = row["product_name"]
    size = row["size"].split("(")[0].strip()
    item_id = item.split("/")[-1]
    print(item_id)
    if item_id in data.keys():
        product_info_list = data[item_id]
        final_score = 0
        for itm in product_info_list:      
            result = manfacturer_website(brd,itm)

            ''' DATA VALIDATION USING FUSSY LOGIC'''
            if result:
                url, title,desc = dataExtract(itm)                
                cnt = 0
                total_len = len(title.split())
                for wrd in title.lower().split():
                    if wrd in name.lower():
                        cnt += 1
                score = cnt/total_len 
                ''' ENSURING DATA FROM HIGHEST SCORE IS DETAINED'''
                if final_score < score:
                    final_score = score
                    pub_url = url
                    pub_desc = desc


        if final_score > 0.5:
            item_dic[counter] = {}
            item_dic[counter]["product_url"] = name
            item_dic[counter]["is_brand_confirmed"] = "Yes"
            item_dic[counter]["manufacturer_url"] = pub_url
            item_dic[counter]["product_description"] = pub_desc
            counter += 1

df1 = pd.DataFrame.from_dict(item_dic,orient='index')


df1.to_csv("C:\\Users\\mjose\\Desktop\\Veeyfed\\data_validation-2.csv",index =False)          


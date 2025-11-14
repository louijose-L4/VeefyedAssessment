from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
import time
import pandas as pd

'''STARTIN THE CHROME SESSION '''

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.amazon.in/")
driver.implicitly_wait(10)

'''SEARCHING FOR SKIN PRODUCTS'''

driver.find_element(By.XPATH,"//input[@role='searchbox']").send_keys("skin care products")
driver.find_element(By.XPATH,"//input[@type='submit']").click()

time.sleep(10)

'''EXTRACTING MAXIMUM OF 100 SEARCH RESULTS '''

product_elements = driver.find_elements(By.XPATH,"//div[@role='listitem']")
products = product_elements[:100]

print("Total results:",len(products))

product_dic = {}
count = 1
for product in products:
    try:
        product_dic[count] = {}
        product_dic[count]["product_name"] = product.find_element(By.XPATH,".//h2").text
        product_dic[count]["product_url"] = "https://www.amazon.in/dp/" + product.get_attribute("data-asin")
        product_dic[count]["product_image"] = product.find_element(By.XPATH,".//img").get_attribute("src")
        count += 1
    except:
        print("Link not available") 
        product_dic[count]["product_name"] = "NA"
        product_dic[count]["product_url"] = "NA"
        product_dic[count]["product_image"] = "NA"
        count += 1       
        continue
 
'''EXTRACTING DATA FROM SPECIFIC PRODUCT PAGE'''

for val in product_dic.values():
    if val["product_url"] != "NA":
        print(val["product_url"])
        driver.get(val["product_url"])
        try:
            brand = driver.find_element(By.XPATH,"//tr[contains(@class,'brand')]").text
        except:
            brand = "Not Available"    
        val["brand"] = brand.replace("Brand","").strip()
        try:
            driver.find_element(By.XPATH,"//*[@id='poToggleButton']//span[text()='See more']").click()
        except:
            pass
        try:
            ingredients = driver.find_element(By.XPATH,"//h4[text()='Ingredients:']//parent::div").text
        except:
            ingredients = "Not Available"
        val["ingredients"] = ingredients.replace("Ingredients:","").strip()

        try:
            size = driver.find_element(By.XPATH,"//div[@id='inline-twister-dim-title-size_name']//span[contains(@id,'size')]").text
        except:        
            size = "Not Available"
        val["size"] = size   
        try:
            category = driver.find_element(By.XPATH,"//div[@id='wayfinding-breadcrumbs_feature_div']//li[9]").text
        except:
            category = "Not Available"
        val["category"] = category 

df = pd.DataFrame.from_dict(product_dic,orient='index')

df = df[(df['ingredients']!= 'Not Available') & (df['size'] != 'Not Available') & (df['category'] != 'Not Available')]

df = df[:30]

df.to_csv("C:\\Users\\mjose\\Desktop\\Veeyfed\\products.csv",index =False)   
    
print("Completed") 

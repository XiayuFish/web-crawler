'''自動將爬取的檔案，儲存成csv檔案，並存入資料庫中'''

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import pandas as pd
import requests
import time
import csv, json
import pymysql
from bs4 import BeautifulSoup

# db = pymysql.connect(  
# host='localhost',  user='root',  password='',  database='carrefour',  charset='utf8')  
# cursor = db.cursor()


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
PLAYERS_INDEX_URL='https://online.carrefour.com.tw/zh/%E8%B2%B7%E7%AC%AC%E4%BA%8C%E4%BB%B6%E5%85%8D%E8%B2%BB'
driver.get(PLAYERS_INDEX_URL)
driver.implicitly_wait(5)
soup = BeautifulSoup(driver.page_source, "lxml")


# pages = soup.find_all("span",class_="resultCount number")
# page_end=(int(pages[0].text)//24)+1
# print(page_end)

#自動抓取頁面的所有頁碼(跳頁功能)
# pages=[]
# tags_a = soup.find_all("a", href="javascript:;")
# print(tags_a)
# for tag in tags_a:
#     if 'onclick' in tag.attrs and 'p_page' in tag.attrs['onclick']:
#         print(tag.text)
#         pages.append(tag.text)
# page_end=int(max(pages))  
# print(page_end)

p_product =[]
p_price =[]
p_category =[]
p_variant =[]
p_web =[]

for page in range(0, 1):
    page = page*24
    url = "https://online.carrefour.com.tw/zh/%E8%B2%B7%E7%AC%AC%E4%BA%8C%E4%BB%B6%E5%85%8D%E8%B2%BB?cgid=BogoCategory&start={}".format(page)
    print(url)
    print("--------------------------------------------------------")

    driver.implicitly_wait(10)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "lxml")
    tags_div = soup.find_all("div",class_="box-img")
    # print(tags_div)
    messages = ""
    for tag in tags_div:
        product = tag.select_one("a").get("data-name")
        price = tag.select_one("a").get("data-price")
        category = tag.select_one("a").get("data-category")  
        variant = tag.select_one("a").get("data-variant")
        web_a = tag.select_one("a").get("href")
        web ="https://online.carrefour.com.tw/"+web_a

        p_product.append(product)
        p_price.append(price)
        p_category.append(category)
        p_variant.append(variant)
        p_web.append(web)      
        print(product, ",", price, ",", category, ",", variant, ",", web)

    #Append the message to the list
      
        messages += f"{product}   【 ${price} 】    {variant}\n\n"
    
        # print(message)

    df_product = pd.DataFrame({
        'product':p_product,'price':p_price,'category':p_category,
        'variant':p_variant,'web':p_web
        })
    #df_product.to_csv('product_data0125.csv', index=False)  #要寫入excel才開啟!!!!!!!!!
         
headers = {
        "Authorization": "Bearer " + "0hf0q41uz6jdcmNFsPPDIsIkJPtL/cWR4lkkRM7lYsXjP8JsoDlF7aWOxjrVTz94B/RooSzwmOhZMvtmqme7FzTWK19g5SowLeIahGpLGwUJp29KTzN+2gqFfHXfBcVSfQokKWxKXS6PlAfpi9ZlRAdB04t89/1O/w1cDnyilFU=",
        "Content-Type": "application/json"
    } 
body = {
    'to':'U1ca7a4dff70984fb0d583cdac74b3470',
    'messages': [{'type': 'text', 'text': f"{messages}"}]
    }
req = requests.post('https://api.line.me/v2/bot/message/push',headers=headers, json=body)   
print(req.text)
driver.quit

# 寫入mysql
# csvfile = "product_data0125.csv"
# with open(csvfile, 'r', encoding='utf8') as fp:
#     reader = csv.reader(fp)
#     for index, row in enumerate(reader): #抓取索引值
#         if index != 0: #不執行首列
#             # print(row)
        
#             sql = """INSERT INTO dataset (product, price, type, varient, web)
#                 VALUES ('{0}', {1}, '{2}', '{3}', '{4}')"""
#             sql = sql.format(row[0], row[1], row[2], row[3], row[4])
#             #print(sql)

#             try:
#                 cursor.execute(sql)
#                 db.commit()
#                 #print("新增一筆記錄...")
#             except:
#                 db.rollback() 
#                 print("新增記錄失敗...")

# db.close()

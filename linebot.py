from bs4 import BeautifulSoup
import requests
 
 
response = requests.get("https://www.udemy.com/course/codegym-python/")
soup = BeautifulSoup(response.text, "html.parser")
 
price = soup.find("span", {"class": "price-text__current"}).getText()[7:]  #取得文字中的價格部分

if int(price) < 500:  #將爬取的價格字串轉型為整數
    headers = {
        "Authorization": "Bearer " + "你的權杖(token)",
        "Content-Type": "application/x-www-form-urlencoded"
    }
 
    params = {"message": "Python基礎課程和網路爬蟲入門實戰 已降價至" + price + "元"}
 
    r = requests.post("https://notify-api.line.me/api/notify",
                      headers=headers, params=params)
    print(r.status_code)  #200
    #123
import requests
from bs4 import BeautifulSoup
import time

import json
import json

import re


#url ="https://www.flipkart.com/search?q= acer+nitro+5&page=2"

dollar = 0.013

def fscrape(prod,page=None):
    headersy = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    r2 = requests.post("https://www.flipkart.com/apple-iphone-14-blue-128-gb/p/itmdb77f40da6b6d?pid=MOBGHWFHSV7GUFWA&lid=LSTMOBGHWFHSV7GUFWA3AV8J8&marketplace=FLIPKART&q=iphone&store=tyy%2F4io&spotlightTagId=BestsellerId_tyy%2F4io&srno=s_1_1&otracker=search&otracker1=search&fm=Search&iid=0bbc1f87-f318-4cd2-85dc-ee43a2c9c7c3.MOBGHWFHSV7GUFWA.SEARCH&ppt=sp&ppn=sp&ssid=a4sb99tshc0000001698675277702&qH=0b3f45b266a97d70",headers=headersy)

    print(r2)

    print("scraping")
    print("scraping")
    print("scraping")
    print("scraping")
    print("scraping")
    if not page:
        page = 1
    url =f"https://www.flipkart.com/search?q={prod}&page={page}%20&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'From': 'google.com'  # This is another valid field
    }




    response = requests.post(url,headers=headers)

    print(response)

    soup = BeautifulSoup(response.content,"html.parser")

    # print(soup.prettify())

    products = soup.find_all("div",class_="_2kHMtA")


    THE_PRODUCTS = []



    for product in products:


        #image

        # image = product.find(class_="_3exPp9")
        image = product.find(class_="_396cs4")
        image = image.get("src")


        #Name

        name = product.find(class_="_4rR01T")
        name  = name.text

        #rating
        rating = product.find(class_="_3LWZlK")
        if rating:
          rating=rating.text
        else:
            rating = "no" 

        #des
        des =  product.find(class_="_1xgFaf") 
        des = str(des).replace("<li","---").replace("rgWa7D","").replace("/>","").replace("<ul class=","").replace("_1xgFaf", "").replace('class=""', "").replace('""', "").replace('>', "").replace("</li", "").replace("</ul","")  


        #price
        price = product.find(class_="_30jeq3")
        
        try:

            price = re.sub(r'[₹|,]',"",price.text)

            price = int(int(price) * dollar )
        except:
            price= None 



        #link

        link = product.find(class_="_1fQZEK").get("href")
        print(link)


    
        THE_PRODUCTS.append({"name": name,"rating":rating,"price":price,"des":des,"img":image,"link":link})


        
        


    try:
        number_of_pages = soup.find(class_="_2MImiq")
        number_of_pages =number_of_pages.find("span").text.split("of")[1]
    except:
        number_of_pages  = 1   

    return({"products":THE_PRODUCTS,"pages":number_of_pages})  







#new  scrape

def secscrape(prod,page=None):
    if not page:
        page = 1
    url =f"https://www.flipkart.com/search?q={prod}&page={page}"
    


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'From': 'google.com'  # This is another valid field
    }


    response = requests.post(url,headers=headers)

    print(response)

    THE_PRODUCTS = []

    soup = BeautifulSoup(response.content,"html.parser")

    products = soup.find_all("div",class_="_4ddWXP")


    for product in products:

        #image

        image = product.find(class_="_396cs4")
        image = image.get("src")


        #name
        name = product.find(class_="s1Q9rs")
        name = name.text


        #rating
        rating = product.find(class_="_3LWZlK") 
        if rating:
            rating=rating.text
        else:
            rating = "no" 

        #des
        des =  product.find(class_="_3Djpdu")
        try:
          des = des.text
        except:
            des = None   



        #price
        price = product.find(class_="_30jeq3")
        
        try:

            price = re.sub(r'[₹|,]',"",price.text)

            

            price = int(int(price) * dollar )
        except:
            price = None
    

        #link
        link = product.find(class_="_2rpwqI").get("href")
        print(link)

        THE_PRODUCTS.append({"name": name,"rating":rating,"price":price,"des":des,"img":image,"link":link})

        

       

        
    try:
        number_of_pages = soup.find(class_="_2MImiq")
        number_of_pages =number_of_pages.find("span").text.split("of")[1]
    except:
        number_of_pages  = 1   

    return({"products":THE_PRODUCTS,"pages":number_of_pages})      





   

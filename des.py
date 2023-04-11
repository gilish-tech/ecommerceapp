import requests
from bs4 import BeautifulSoup
import re
import json
dollar = 0.013

#url = "https://www.flipkart.com/gta-san-andreas-video-game/p/itmbb9f5a8dace4d?pid=CGEGFHAJJMXUHRXZ&lid=LSTCGEGFHAJJMXUHRXZJFZ1IF&marketplace=FLIPKART&q=gta+san+andreas+for+pc&store=4rr%2Ffa6%2Fmdf%2Fnmm&srno=s_1_1&otracker=AS_QueryStore_OrganicAutoSuggest_1_8_sc_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_8_sc_na_na&fm=search-autosuggest&iid=55f750f4-b887-4075-8a76-466f93de347a.CGEGFHAJJMXUHRXZ.SEARCH&ppt=sp&ppn=sp&ssid=evzs55alds0000001663549739391&qH=b017829c7a2614fd"
url = "https://www.flipkart.com/apple-iphone-6s-gold-32-gb/p/itmen2yynt6bz3gg?pid=MOBEN2YYQH8PSYXG&lid=LSTMOBEN2YYQH8PSYXGJSTV77&marketplace=FLIPKART&q=iphone+19&store=tyy%2F4io&srno=s_1_1&otracker=AS_Query_HistoryAutoSuggest_2_0&otracker1=AS_Query_HistoryAutoSuggest_2_0&fm=Search&iid=a254fe6f-8aef-4dbf-b9f6-4049f4c1f4ba.MOBEN2YYQH8PSYXG.SEARCH&ppt=sp&ppn=sp&ssid=617zhowi680000001663543367876&qH=2127cd54cc1d00f4"
#url = "https://www.flipkart.com/sony-playstation-4-1-tb-bloodborne/p/itmfe555p3ybrh73?pid=GMCFE555R2DQJUBF&lid=LSTGMCFE555R2DQJUBFUBMQBJ&marketplace=FLIPKART&q=playstation+4&store=4rr%2Fx1m%2Fwym&srno=s_1_6&otracker=search&otracker1=search&fm=search-autosuggest&iid=b46ecb7d-1e45-4e13-a911-954a99103794.GMCFE555R2DQJUBF.SEARCH&ppt=sp&ppn=sp&ssid=jdskmtwvmo0000001663545413908&qH=165a3c0ef365de27"
#url = "https://www.flipkart.com/nick-jones-400-1-retro-game-box-console-8-gb-mario/p/itm9abf7a89aa41c?pid=GMCFGEMZNM4Z54ZG&lid=LSTGMCFGEMZNM4Z54ZGSMHTIM&marketplace=FLIPKART&q=playstation+4&store=4rr%2Fx1m%2Fwym&srno=s_1_1&otracker=search&otracker1=search&fm=search-autosuggest&iid=b46ecb7d-1e45-4e13-a911-954a99103794.GMCFGEMZNM4Z54ZG.SEARCH&ppt=sp&ppn=sp&ssid=jdskmtwvmo0000001663545413908&qH=165a3c0ef365de27"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'From': 'google.com'  # This is another valid field
}
r = requests.get(url,headers=headers)
web_name = ['charleshop','charles','Charleshop','Charlesshop','Charlshop']

soup = BeautifulSoup(r.content,"html.parser")


images = soup.find_all(class_="q6DClP")


all_small_images = [image.get("src") for image in images]    
    
all_large_images = [i.replace("image/128/128","image/416/416")  for i in all_small_images ] 
alt_image = soup.find(class_="_396cs4").get("src")


name = soup.find(class_="B_NuCI").text
price = soup.find(class_="_30jeq3")
  
try:

    price = re.sub(r'[₹|,]',"",price.text)

            

    price = int(int(price) * dollar )
except:
     price = None


rating = soup.find(class_="_3LWZlK")

if rating:
    rating=rating.text
else:
    rating = "no" 


reviews = soup.find_all(class_="_2wzgFH")

all_reviews = []
for  review in reviews:
    review_rating = review.find(class_="_3LWZlK")
    if review_rating:
         review_rating = review_rating.text
    else:
        review_rating = "no"  
        
    review_words = review.find(class_="t-ZTKy")
    if review_words:
        review_words =  review_words.text.replace("READ MORE"," ")
        review_words = re.sub(r"(flipkart|flixcart|filpkat|filpkat|flipcart|filipkart| Filpcard|flip\skart|flip\scart|ekart)", web_name[(len(review_words) %  len(web_name)) - 1 ], review_words, flags=re.IGNORECASE)
        print(review_words)
    else:
       review_words =   None
    
    
    
    all_reviews.append({"review_rating":review_rating,"review_words":review_words})
    

print(all_reviews)    


full_description = soup.find("table",{"class":"_14cfVK"})

full_description = str(full_description)

PRODUCT_INFO = {"all_small_images":all_small_images,"all_large_images":all_large_images,"alt_image":alt_image,"rating":rating,"price":price,"full_des":full_description,"all_reviews":all_reviews}
    
                
with open("prodsinfo","w") as f:
    f.write(json.dumps(PRODUCT_INFO))




# print(price)
# print(rating)
# print(name)
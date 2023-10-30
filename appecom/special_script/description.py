
from .fscrape import dollar
import requests
from bs4 import BeautifulSoup
import re



web_name = ["<span style='color:#f0c14b; display:inline'> <b>Gil-tech</b></span>",   "<span style='color:#f0c14b; display:inline'> <b>G-tech</b></span>","<span style='color:#f0c14b; display:inline'><b>Gilish-tech</b></span>"]


def get_description(url):
    url = f"http://flipkart.com{url}"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'From': 'google.com'  # This is another valid field
    }
    r = requests.post(url,headers=headers)
    print(r)
    print(r.content)

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
            
        else:
          review_words =   None
        
        
        
        all_reviews.append({"review_rating":review_rating,"review_words":review_words})
        

    print(all_reviews)    


    full_description = soup.find("table",{"class":"_14cfVK"})

    full_description = str(full_description)

    PRODUCT_INFO = { "name":name, "all_small_images":all_small_images,"all_large_images":all_large_images,"alt_image":alt_image,"rating":rating,"price":price,"full_des":full_description,"all_reviews":all_reviews}
    return PRODUCT_INFO
        
        
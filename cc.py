import random
import requests
from bs4 import BeautifulSoup
import json

MYNAME = ["GILBERTO DIAMOND","GILISH TECH","G TECH","GIL TECH"]

r = requests.get("https://support.bluesnap.com/docs/test-credit-card-numbers")

print(r)



soup = BeautifulSoup(r.content,"html.parser")

card  = soup.find_all("tr")
card_list = []
for c in card:
    if len(c) > 1:
        if len(c) > 0:
            try:
                name = c.find_all("td")[0].text
                number = c.find_all("td")[1].text
                card_list.append({"cardname":name,"number":number,"name":f"{random.choice(MYNAME)}","expiry":f"{random.randrange(1,10)}/{random.randrange(23,28)}"})
            
   
            except:
                print("none")    
        
            
       
        
       
                
            
with open("a.json","w") as f:
    json.dump(card_list,f)
     
     
      



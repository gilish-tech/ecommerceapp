from email import header
import requests

payload = {
    "autoReplace": True,
    "englishDialect": "indifferent",
    "getCorrectionDetails": True,
    "interfaceLanguage": "en",
    "isHtml": False,
    "language": "eng",
    "locale": "",
    "origin": "ginger.web",
    "originalText": "",
    "text": "Nothing was purchased  by this website"
}
headers={
    
    
    
    
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    
}

res = requests.post("https://orthographe.reverso.net/api/v1/Spelling/",data=payload,headers=headers)

print(res)
print(res.content)
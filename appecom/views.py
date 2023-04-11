from ast import Return
import json
from urllib import response
from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import viewsets,status
from urllib.parse import quote_plus
from .models  import Cart

from .special_script.fscrape  import fscrape,secscrape
from rest_framework.permissions import IsAuthenticated
from .serializers import CartSerializers
from .special_script.description import get_description
from django.contrib.auth.models import User
from django.db import IntegrityError
# Create your views here.

#eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjYyMjE5MDEzLCJpYXQiOjE2NjIyMTg3MTMsImp0aSI6ImMyOTcwNGIzYjVlMTQyZTViODhiNDVjMGRmOWEyMDU1IiwidXNlcl9pZCI6MX0.ILiC5qzA1vSEZcQqsZScK9TKidS9VFvDYrnHAnefoSc


def solve_total(items):
      total_quantity =  0
      for i in items:
            total_quantity += i.quantity
      return total_quantity
            

# @permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])

def products(request):
    if request.method == 'POST':
        print(request.data)
        text  = quote_plus(request.data["name"])
        try:
          page_num  = request.data["num"] 
        except:
          page_num = 1  
        all_products = fscrape(text,page_num)
        print(f"user is {request.user}")
        print(f"auth is {request.auth}")
        a = "True" if request.auth else "false"
        print(a)
       
        if all_products['products'] == []:
            all_products = secscrape(text)
        return Response({"message": all_products})
    return Response([{"name":"gilbert","sch":"loop"},{"names":"chichi","sch":"lose"}])
  


@api_view(['GET', 'POST']) 
@permission_classes([IsAuthenticated]) 
def add_to_cart(request): 
  user = request.user
  if request.method == "POST":
      # print(request.data)
      name = request.data.get("product").get("name")
      des =request.data.get("product").get("des")
      price = request.data.get("product").get("price")
      rating  =  request.data.get("product").get("rating")
      img=  request.data.get("product").get("img")
      link= request.data.get("product").get("link")
      
      cmd  = request.data.get("cmd")
      
      if cmd == "add":
      
          if Cart.objects.filter(user=user,name=name,des=des,price=price,rating=rating,img=img,link=link).exists():
            usercart = Cart.objects.filter(user=user,name=name,des=des,price=price,rating=rating,img=img,link=link)
            for c in usercart:
                  c.quantity +=1
                  c.save()
                  usercart = Cart.objects.filter(user=user)
                  
                  s = CartSerializers(usercart,many=True)
                  total= 0
                  for c in usercart:
                    total += float(c.item_total)
                  totalcart =  solve_total(usercart)  
                  return Response({"products":s.data,"total":total,"totalcart":totalcart},status=status.HTTP_200_OK)  
                  
          else:
            Cart.objects.create(user=user,name=name,des=des,price=price,rating=rating,img=img,link=link,quantity=1)     
            usercart = Cart.objects.filter(user=user)
            totalcart = solve_total(usercart)
            
          return Response({"totalcart":totalcart},status=status.HTTP_200_OK)   
      elif cmd == "sub" :
          if Cart.objects.filter(user=user,name=name,des=des,price=price,rating=rating,img=img,link=link).exists():
            usercart = Cart.objects.filter(user=user,name=name,des=des,price=price,rating=rating,img=img,link=link)
            for c in usercart:
                  c.quantity -=1
                  c.save()
                  if c.quantity <= 0:
                          c.delete() 
            usercart = Cart.objects.filter(user=user)              
            s = CartSerializers(usercart,many=True)
            total= 0
            for c in usercart:
               total += float(c.item_total)
            totalcart =  solve_total(usercart)    
         
            return Response({"products":s.data,"total":total,"totalcart":totalcart},status=status.HTTP_200_OK)  
      elif cmd  == "del":   
         if Cart.objects.filter(user=user,name=name,des=des,price=price,rating=rating,img=img,link=link).exists():
                usercart = Cart.objects.filter(user=user,name=name,des=des,price=price,rating=rating,img=img,link=link)     
                for c in usercart:
                  c.delete()  
                  usercart = Cart.objects.filter(user=user)              
                  s = CartSerializers(usercart,many=True)
                  total= 0
                  for c in usercart:
                      total += float(c.item_total)
                  totalcart =  solve_total(usercart)     
              
                  return Response({"products":s.data,"total":total,"totalcart":totalcart},status=status.HTTP_200_OK)            
               
    
      
    
  return Response([{"name":"gilbert","sch":"loop"},{"names":"chichi","sch":"lose"}])

#eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjYzMDg4NzQ0LCJpYXQiOjE2NjMwODg0NDQsImp0aSI6IjhjZDdhODBmM2NjMTQ1Y2U5OTlhYWZlZTZhMTFmM2Y2IiwidXNlcl9pZCI6MX0.TwDxJlmdQ5IsFVsTy3JY5hyIzV_3xpwFNx9N8hw2Y9c

@api_view(['GET', 'POST']) 
@permission_classes([IsAuthenticated]) 
def get_cart(request):
    user = request.user
        
    userCart = Cart.objects.filter(user=user)
    serializer = CartSerializers(userCart,many=True)
    total = 0 
    for c in userCart:
          total += float(c.item_total)
    print(total)
    return Response({"product":serializer.data, "total_amount":total} )
         



@api_view(['GET', 'POST']) 
@permission_classes([IsAuthenticated]) 
def get_total(request):
    user = request.user
        
    userCart = Cart.objects.filter(user=user)
    totalcart = solve_total(userCart)
    
   
    return Response({"totalcart":totalcart} )
         
         
@api_view(['GET', 'POST']) 
def product_description(request):
      if request.method == "POST":
            url = request.data.get("url")
            descrptions = get_description(url)
            return Response( descrptions)
      
      return Response({"des":"gil-tech des"})  
    

      
@api_view(['GET', 'POST']) 
def create_account(request):
      if request.method == "POST":
            email = request.data.get("email")
            username = request.data.get("username")
            pass1 = request.data.get("pass1")
            pass2 = request.data.get("pass2")
            if pass1 != pass2:
                  print("yes")
                  return Response({"error":"pnq"})
            else:
              try :
                if (pass1.strip() == "" ) | (email.strip() == "")  | (username.strip() == "") :
                      return Response({"error":"big error"})
                  
                else:
                      User.objects.create_user(username=email,email=username,password=pass1)
                      
                      
                    
              except IntegrityError as e:
                print(f"{e}\n \n \n \n \n")
        
                if 'UNIQUE constraint' in str(e):
                      print("exist")
                      return Response({"error":"already-exist"})
                else:
                    return Response({"error":"big error"}) 
            
            return Response({"error":"zero"})         
                       
                 
                  
      
      return Response({"des":"gil-tech des"})  
    

      
                
    #  {"username":"tom","email":"tom@gmail.com","pass1":"spec","pass2":"spec"}       

@api_view(['GET', 'POST'])             
def  validateCreditCard(request):
      with open("all_test_cards.json","r") as f:
            special =  json.loads(f.read())
            
            
      user = request.user
      
      #special =[{"cardname":"mololo" ,"number":"4111111111111111","name":"GILISH TECH","expiry":"02/24"}]
      [c.pop("cardname") for c in special]
      
      
      if request.method == "POST":
            
            print(special)
            
            try:
            
                  if len(request.data["cvc"]) != 3:
                     return Response({"valid":"no"})  
            except:
                   return Response({"valid":"no"})    
            request.data["number"] = request.data["number"].replace(" ","")   
            print(request.data)
            
            
            request.data.pop("cvc")
            request.data["number"] = request.data["number"].replace(" ","")
             
            is_valid = "yes" if request.data in special else "no"
            if str(user) !=  "AnonymousUser" and is_valid == "yes":
                usercart = Cart.objects.filter(user=user)     
                for c in usercart:
                   c.delete()           
            return Response({"valid":is_valid})
            
      






import imp
from multiprocessing.spawn import import_main_path
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=10000,null=True)
    img = models.CharField(max_length=20000)
    price = models.CharField(max_length=10000)
    des = models.CharField(max_length=10000,null=True)
    rating = models.CharField(max_length=10000,null=True)
    link = models.CharField(max_length=10000,null=True)

    quantity = models.IntegerField(default=0,null=True)
    date_ordered = models.DateTimeField(auto_now_add=True,null=True)
    complete = models.BooleanField(default=False,null=True)
    
    @property
    def item_total(self):
        total = float(self.price)*self.quantity
        return  "{:.2f}".format(total)
    @property
    def cut_string(self):
        return self.product_name[0:30]

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ItemModel(models.Model):
    name = models.CharField(max_length = 128)
    price = models.IntegerField()
    cover = models.ImageField(upload_to = 'images/',blank = True,null = True)
    def __str__(self):
        return self.name + " "+ str(self.price)
    
class CategoryModel(models.Model):
    name = models.CharField(max_length=128)
    items = models.ManyToManyField(ItemModel)
    def __str__(self):
        return self.name

class CartModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(ItemModel, on_delete=models.CASCADE)
    # quantity = models.IntegerField(default=0)
    def __str__(self):
        return self.user.username

class OrderModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.JSONField()
    discount = models.CharField(max_length=128)
    delivery_date = models.DateField(max_length=128,null=True,blank=True)
    def __str__(self):
        return self.user.username
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.total_price = sum(item[1] for item in self.items)
        self.final_price = sum(item[1] for item in self.items) - int(self.discount)

class PromoCodeModel(models.Model):
    promo = models.CharField(max_length=128)
    discount = models.CharField(max_length=128)
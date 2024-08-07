from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    usertype=models.CharField(max_length=20,default="buyer")
    email=models.EmailField()
    name=models.CharField(max_length=20)
    mobile=models.PositiveIntegerField()
    password=models.CharField(max_length=20)
    profile=models.ImageField(default="",upload_to="picture/")

    def __str__(self):
        return self.name

class Addproduct(models.Model):
    category=(
        ("apple","apple"),
        ("banana","banana"),
        ("kiwi","kiwi"),
        ("cherry","cherry"),
        ("mango","mango"),
        ("grapes","grapes"),
    )
    pcategory=models.CharField(max_length=20,choices=category,null=True)
    seller=models.ForeignKey(User,on_delete=models.CASCADE)
    pname=models.CharField(max_length=100)
    pbrand=models.CharField(max_length=100)
    pdesc=models.CharField(max_length=200)
    pprice=models.PositiveIntegerField()
    pimg=models.ImageField(default="",upload_to="addpicture/")

    def __str__(self):
        return self.seller.name + " - " + self.pname
    
class Like(models.Model):   
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Addproduct,on_delete=models.CASCADE)
    date=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.name + " - " + self.product.pname
    

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Addproduct,on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    product_price=models.PositiveIntegerField()
    total_price=models.PositiveIntegerField()
    payment_status= models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f'{self.qty} - {self.product.pname}'
    
class Checkout(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    
    chname=models.CharField(max_length=20)
    chmobile=models.PositiveIntegerField()
    add=models.TextField()
    cdate=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.name 
import uuid
from django.db import models

# Create your models here.
class creationData(models.Model):
    product_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    owner_id = models. CharField(default="")
    name = models.TextField(max_length=20)
    price = models.FloatField(default=0.0)
    description = models.TextField(max_length=1000)
    image = models.ImageField(null= True, blank= True, upload_to= 'images/')

    def __str__(self):
        return self.owner_id
    

class BuyModel(models.Model):
    order_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    product_id = models. CharField(default="")
    owner_id = models. CharField(default="")
    bider_id = models. CharField(default="")
    original_price = models.FloatField(default=0.0)
    updated_price = models.FloatField(default=0.0)
    updatedByOwner = models.BooleanField(default= False)
    
    def __str__(self):
        return self.order_id


class NotifyAndWishlistModel(models.Model):
    product_id = models.CharField(default="")
    owner_id = models. CharField(default="")
    bider_id = models. CharField(default="")
    isWishlisted = models.BooleanField(default= False)
    
    def __str__(self):
        return (self.product_id+" "+ str(self.isWishlisted))
from django.db import models
from ..user.models import CostumUser
from ..product.models import Product

# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(CostumUser,on_delete=models.CASCADE,null=True,blank=True)


    product_names = models.CharField(max_length=500)
    total_products =  models.CharField(max_length=500, default=0)
    transaction_id = models.CharField(max_length=150, default=0)
    total_amount = models.CharField(max_length=50, default=0)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"{self.user} - {self.product_names}"
from  django.db import  models
from .product import Product
from .customers import Customers

import datetime
class Orders(models.Model):
    product = models.ForeignKey(Product ,on_delete= models.CASCADE)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    address = models.CharField(max_length=1000)
    city = models.CharField(max_length=1000)
    state = models.CharField(max_length=1000)
    zip = models.CharField(max_length=1000)
    phone = models.CharField(max_length=15)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    date = models.DateField(default= datetime.datetime.today)
    status = models.BooleanField(default=False)

    def placeorder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return  Orders\
            .objects\
            .filter(customer= customer_id).order_by('-date')

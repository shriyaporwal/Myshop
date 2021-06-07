from  django.db import  models
from .category import Category

class Product(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/products/')
    price = models.IntegerField()
    desc = models.TextField(max_length=200)
    offer = models.BooleanField(default=False)


    def __str__(self):
        return self.name

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_id(category_id):
        if category_id:
            return Product.objects.filter(category= category_id)
        else:
            return Product.objects.all()
    @staticmethod
    def product_by_id(p_id):

        return Product.objects.filter(id__in = p_id )
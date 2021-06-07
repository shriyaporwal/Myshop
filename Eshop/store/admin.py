from django.contrib import admin
from .models.product import Product
from .models.category import Category
from .models.orders import Orders
from .models.Contactus import Contact
from .models.customers import Customers

class AdminProduct(admin.ModelAdmin):
    list_display = ['name','price','category']


class AdminCategory(admin.ModelAdmin):
    list_display = ['name']

class AdminCustomer(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Product,AdminProduct)
admin.site.register(Category,AdminCategory)
admin.site.register(Customers,AdminCustomer)
admin.site.register(Orders)
admin.site.register(Contact)
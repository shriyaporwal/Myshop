from  django.db import  models
class Customers(models.Model):
    name = models.CharField(max_length=120)
    username = models.CharField(max_length=120)
    email = models.CharField(max_length=120)
    phone = models.CharField(max_length= 15)
    password1 = models.TextField(max_length=500)
    password2 = models.TextField(max_length=500)

    def __str__(self):
        return self.name

    def register(self):
        self.save()
    def isExists(self):
        if Customers.objects.filter(email = self.email):
            return True
        return False

    def isusername(self):
        if Customers.objects.filter(username=self.username):
            return True
        return False



    @staticmethod
    def get_customer_by_username(uesername):
        try:
            return Customers.objects.get(username=uesername)
        except:
            return False
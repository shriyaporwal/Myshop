from django.db import models
class Contact(models.Model):
    name = models.CharField(max_length=120)
    email = models.CharField(max_length=120)
    phone = models.TextField()
    desc = models.TextField(max_length=500)

    def __str__(self):
        return self.name
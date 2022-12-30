from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

def img_path(instance, filename):
    return f"{instance.username}/{filename}"

class User(AbstractUser):
    comment=models.TextField(blank=True)
    point=models.IntegerField(default=0)
    pic=models.ImageField(upload_to=img_path)

    def getpic(self):
        if self.pic:
            return self.pic.url
        return '/media/noimage.png'
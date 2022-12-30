from django.db import models
from acc.models import User

# Create your models here.
class Board(models.Model):
    subject=models.CharField(max_length=100)
    writer=models.ForeignKey(User,on_delete=models.CASCADE,related_name='writer')
    content=models.TextField(blank=True)
    likey=models.ManyToManyField(User,blank=True,related_name='likey')
    pubdate=models.DateTimeField()

    def __str__(self):
        return f"{self.subject}-{self.writer}"

class Reply(models.Model):
    b=models.ForeignKey(Board, on_delete=models.CASCADE)
    replyer=models.ForeignKey(User,on_delete=models.CASCADE)
    comment=models.TextField()

    def __str__(self):
        return f"{self.b}_{self.replyer}"
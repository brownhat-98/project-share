from django.db import models

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=200,null=True,default=None)
   
    def __str__(self):
        return '{}'.format(self.name)
    
    
    
class Book(models.Model):

    title=models.CharField(max_length=200)
    author=models.ForeignKey(Author, on_delete=models.CASCADE)
    price= models.IntegerField()
    cover_url=models.CharField(max_length=200, default=None)
    quantity=models.IntegerField()


    def __str__(self):
        return '{}'.format(self.title)
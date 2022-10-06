from pyexpat import model
from turtle import title
from venv import create
from django.db import models
from django.contrib.auth.models import User #takes care of user model
# Create your models here.

class Task(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, null= True, blank= True)
    title= models.CharField(max_length=200)
    description= models.TextField(null=True, blank=True)
    complete= models.BooleanField(default=False)
    create= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    #sorts the tasks , completed tasks below
    class Meta:
        ordering=['complete']
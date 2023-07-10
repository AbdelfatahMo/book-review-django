from asyncio.base_subprocess import WriteSubprocessPipeProto
from os import name
from django.db import models
from regex import W

# Create your models here.
class Publisher(models.Model):
    name = models.CharField(max_length=255,help_text='The name of the publisher')
    website=models.URLField(help_text="The Publisher 's website.")
    email=models.EmailField(help_text="The Publisher's email address.")
    
    def __str__(self):
        return self.name
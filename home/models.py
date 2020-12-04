from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.postgres.fields import JSONField
# Register your models here.
# from django_postgres_extensions.models.fields import ArrayField
# from django.db import models
# from django.contrib import admin
from django.utils.html import format_html


class Imagelist(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=550)
    
class UserImagelist(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=550)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

    
class Scraper(models.Model):
    id=models.AutoField(primary_key=True)
    list_name = models.CharField(max_length=200)
    links=models.TextField(null =True,default ='')
    Description=models.TextField(null =True,blank=True)
    source = models.CharField(max_length=200,default='zillow')
    status = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u'%s %s' % (self.list_name, self.status)
    # name = models.CharField(max_length=60)
    def __str__(self):
        return '{}'.format(self.list_name)
class result(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=200,null =True,default =None)
    source = models.CharField(max_length=200,default='zillow')
    scraper=models.ForeignKey(Scraper,on_delete=models.CASCADE,default=None)
    scraper_name=models.CharField(max_length=200,null =True,default =None)
    Address=models.CharField(max_length=200,null =True,default =None)
    city=models.CharField(max_length=200,null =True,default =None)
    state=models.CharField(max_length=200,null =True,default =None)
    price=models.CharField(max_length=200,null =True,default =None)
    bathrooms=models.CharField(max_length=200,null =True,default =None)
    zipcode=models.CharField(max_length=200,null =True,default =None)
    area=models.CharField(max_length=200,null =True,default =None)
    latlon=models.CharField(max_length=200,null =True,default =None)
    Bedrooms=models.CharField(max_length=200,null =True,default =None)
    zestimate=models.CharField(max_length=200,null =True,default =None)
    list_date=models.CharField(max_length=200,null =True,default =None)
    Description=models.TextField(null =True,default ='')
    Pictures=JSONField(default =dict)
    Facts=JSONField(default =dict)
    home_fact=JSONField(default =dict)
    priceHistory=JSONField(default =dict)
    rawdata=JSONField(default=dict)
    agent_name=models.CharField(max_length=200,null =True,default =None)
    agent_number=models.CharField(max_length=200,null =True,default =None)
    agent_broke=models.CharField(max_length=200,null =True,default =None)
    agent_pic=models.CharField(max_length=200,null =True,default =None)
    status=models.CharField(max_length=50,default='active',db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    url = models.CharField(max_length=200,null =True,default =None)
    def __str__(self):
        return '{}'.format(self.title)
    
    def Status(self):
            if self.status=='active':
                color='green'
            else:
                color='red'
        # self.last_name,
            return format_html(
            '<span style="background-color: {};color:white;padding:5%;text-transform: capitalize;">{}</span>',
            color,
            self.status
    )
    Status.allow_tags = True
    Status.admin_order_field = 'status'
    
    @property
    def scraper_namee(self):
        return self.scraper.list_name
    

class StatementTemplate(models.Model):
    def __str__(self):
        return "StatementTemplate" # or make it some description of that particular object

from django.contrib import admin
from home.models import result
from home.models import Scraper
from django.contrib import messages 
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
# from django.contrib.sites.models import Site
from django.contrib.auth.models import Group

import json
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter

from django.contrib import admin
from django.utils.safestring import mark_safe


from django.contrib.admin.utils import flatten_fieldsets
# from .models import APIData


from django.db import models
from django.contrib import admin
from django.utils.html import format_html

from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter
)
# admin.site.unregister(Token)
# admin.site.unregister(User)
admin.site.unregister(Group)
class results(admin.ModelAdmin):
    # actions = None
    
   
    list_display = ('scraper_name','source','title','city','state','price','Status','updated','list_date')
    # list_display_links = ('',)
    search_fields = ['scraper_name','city','state','status']
    # fieldsets = [
    # (None, {'fields':()}), 
    # ]
    fieldsets = [
        ('List Information', {'fields': ['scraper_name', 'title','city','state','price','status','created','updated','url']}),
        ('All Data', {
            'classes': ('collapse',),
            'fields': ('data_prettified',),
        }),
    ]
    readonly_fields = ('scraper_name','title','created','updated','data_prettified','city','state','price','status','url')
    list_display_links = ('scraper_name',)
    list_filter = (('scraper_name', DropdownFilter),('city', DropdownFilter),('state', DropdownFilter),'created','status')
    # def has_add_permission(self, request, obj=None):
    #     return False
    short_description = 'scraper_name'


    def data_prettified(self, instance):
        """Function to display pretty version of our data"""
        
        # Convert the data to sorted, indented JSON
        response = json.dumps(instance.rawdata, sort_keys=True, indent=2)

        # Truncate the data. Alter as needed
        # response = response[:5000]

        # Get the Pygments formatter
        formatter = HtmlFormatter(style='colorful')

        # Highlight the data
        response = highlight(response, JsonLexer(), formatter)

        # Get the stylesheet
        style = "<style>" + formatter.get_style_defs() + "</style><br>"

        # Safe the output
        return mark_safe(style + response)

    data_prettified.short_description = 'JSON DATA'
    
    # def __init__(self, *args, **kwargs):
    #     super(admin.ModelAdmin, self).__init__(*args, **kwargs)
    #     self.list_display_links = (None, )
admin.site.register(result,results)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('list', 'list_stat')

class Scraperss(admin.ModelAdmin):
    search_fields = ['list_name']
    fields=(('list_name','status'),'Description','links','source')
    list_display = ('list_name', 'status','Description','source')
    list_editable = ('status',)
    list_display_links = ('list_name','source',)
    list_filter = ( 'status','source',)
    def status(self, obj): 
        return obj.status == 1
  
    status.boolean = True
    def make_active(modeladmin, request, queryset): 
        queryset.update(status = 1) 
        messages.success(request, "Selected Record(s) Marked as Active Successfully !!") 
  
    def make_inactive(modeladmin, request, queryset): 
        queryset.update(status = 0) 
        messages.success(request, "Selected Record(s) Marked as Inactive Successfully !!") 
  
    admin.site.add_action(make_active, "Make Active")
    admin.site.add_action(make_inactive, "Make Inactive")
    # def message_user(self, *args): # overridden method
    #         pass

   
admin.site.register(Scraper,Scraperss)
# Register your models here.

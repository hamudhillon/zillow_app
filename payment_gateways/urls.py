"""payment_gateways URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home import views
from django.conf.urls import include
# from runnscrapper import views
admin.site.site_header = "Gartin Real Estate"
admin.site.site_title = "Gartin Real Estate Admin Portal"
admin.site.index_title = "Welcome to Gartin Real Estate Admin Portal"


all_urls = [
    path('', admin.site.urls,name='admins'),
    path('RunScrapper', views.runnscrapper),
    path('api/', include('home.urls')),
    path('accounts/login/', admin.site.urls),
    # path('logout/', views.logout_view),
    # path('register/', views.Token_register),
    # path('', views.roompage),
    # path('api/', views.index),
    # path('upload_csv/', views.ProcessCsvFiles),
]
# For Swagger Ui
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf.urls.static import static
from django.conf import settings

schema_view = get_schema_view(
   openapi.Info(
      title="Zillow API",
      default_version='v1',
      description="Ziilow Swagger Contains All the Endpoints of Zillow Api",
      terms_of_service="https://www.zillow.webdrvn.com/policies/terms/",
      contact=openapi.Contact(email="test@snippets.local"),
      license=openapi.License(name="Zillow.webdrvn License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = all_urls + [
    path('docs/', schema_view.with_ui('swagger')),
]

urlpatterns += [
    # ... the rest of your URLconf goes here ...
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

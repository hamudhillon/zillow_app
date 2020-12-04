from django.urls import path
from home import views as api_views

urlpatterns = [
    path('index/', api_views.IndexView.as_view()),
    path('zillow/', api_views.ZillowApiView.as_view(),name='zillow_api'),
    path('craigslist/', api_views.CraigsApiView.as_view(),name='craigs_api'),
]

from django.urls import path
from football import views

#TEMPLATE TAGGING
app_name = 'football'

urlpatterns = [
    path('api/', views.get_api_data, name='api'),  
]
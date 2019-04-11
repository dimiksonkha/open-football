from django.urls import path
from football import views

#TEMPLATE TAGGING
app_name = 'football'

urlpatterns = [
    path('matches/', views.get_match_data, name='match_data'),
    path('matches/<int:match_id>', views.match_details, name='match_details'),   
]

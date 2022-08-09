from django.urls import path
from . import views
 
# namespace
app_name = 'search'
 
urlpatterns = [
        path('', views.search_result, name='search_result'),# pathのname
]
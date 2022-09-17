

from django.urls import path
from . import views

app_name='mainApp'
urlpatterns = [
    path('',views.home,name='home'),
    path('show_companies/',views.show_companies,name='show_companies'),
    path('show_representatives/',views.show_representatives,name='show_representatives'),
    path('show_factories/',views.show_factories,name='show_factories'),
    path('show_items/',views.show_items,name='show_items'),
]
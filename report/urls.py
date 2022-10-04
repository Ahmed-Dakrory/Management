

from django.urls import path
from . import views

app_name='report'
urlpatterns = [
    path('daily_report',views.daily_report,name='daily_report'),
    path('export_daily_report',views.export_daily_report,name='export_daily_report'),
    path('export_total_report',views.export_total_report,name='export_total_report'),
    path('factory_needed_report',views.factory_needed_report,name='factory_needed_report'),
  

]
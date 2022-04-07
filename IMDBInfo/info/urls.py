from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='info-home'),
    path('data/', views.data, name='info-data'),
    path('chart/', views.chart, name='info-chart'),
    path('rscript/', views.rscript, name='info-rscript'),
    path('hypothese/', views.hypothese, name='info-hypothese'),
]

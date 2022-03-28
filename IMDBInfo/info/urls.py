from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='info-home'),
    path('about/', views.about, name='info-about'),
    path('data/', views.data, name='info-data'),
    path('pie-chart/', views.pie_chart, name='info-pie-chart'),
    path('line-chart/', views.line_chart, name='info-line-chart'),
]

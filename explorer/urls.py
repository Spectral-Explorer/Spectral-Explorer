from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('details/', views.explorer2, name='explorer2'),

]

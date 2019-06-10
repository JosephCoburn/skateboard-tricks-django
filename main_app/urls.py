from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('tricks/', views.tricks_index, name='index'),
    path('tricks/<int:trick_id>/', views.tricks_detail, name='detail'),
]
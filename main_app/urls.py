from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('tricks/', views.tricks_index, name='index'),
    path('tricks/<int:trick_id>/', views.tricks_detail, name='detail'),
    path('tricks/<int:trick_id>/add_training', views.add_training, name='add_training'),
    path('tricks/<int:trick_id>/add_photo/', views.add_photo, name='add_photo'),
    path('tricks/<int:trick_id>/assoc_park/<int:park_id>/', views.assoc_park, name='assoc_park'),
    path('tricks/<int:trick_id>/unassoc_park/<int:park_id>/', views.unassoc_park, name='unassoc_park'),
    path('tricks/create/', views.TrickCreate.as_view(), name='tricks_create'),
    path('tricks/<int:pk>/update', views.TrickUpdate.as_view(), name='tricks_update'),
    path('tricks/<int:pk>/delete', views.TrickDelete.as_view(), name='tricks_delete'),
    path('parks/', views.ParkList.as_view(), name='parks_index'),
    path('parks/<int:pk>/', views.ParkDetail.as_view(), name='parks_detail'),
    path('parks/create/', views.ParkCreate.as_view(), name='parks_create'),
    path('parks/<int:pk>/update/', views.ParkUpdate.as_view(), name='parks_update'),
    path('parks/<int:pk>/delete/', views.ParkDelete.as_view(), name='parks_delete'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup', views.signup, name='signup'),
]
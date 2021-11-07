from django import urls
from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('profile/<int:nurse_pk>/', views.profile, name='profile'),
    # path('profile/create', views.create_profile, name='create_profile'),
    path('profile/update', views.update_profile, name='update_profile'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('delete/', views.delete, name='delete'),
    path('update/', views.update, name='update'),
    path('password/', views.change_password, name='change_password'),
]

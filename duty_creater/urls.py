from django.urls import path
from . import views


app_name = 'dfn'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:nurse_pk>', views.myduty, name='myduty'),
    path('new/', views.new, name='new'),
]
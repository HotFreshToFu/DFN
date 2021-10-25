from django.urls import path
from . import views


app_name = 'dfn'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:nurse_pk>', views.myduty, name='myduty'),
    path('new/main/', views.new_main, name='new_main'),  # 새 듀티 생성을 위한 페이지
    path('new/', views.new, name='new'),  # 생성한 듀티 출력 및 저장
]
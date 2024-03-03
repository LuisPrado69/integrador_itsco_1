from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('signin/', views.signin),

    path('technical/', views.technical, name="technical"),
    path('storeTechnical/', views.storeTechnical),

    path('incidence/', views.incidence, name="incidence"),
    path('storeIncidence/', views.storeIncidence),

    path('order/index/page<int:num>/$', views.order, name="index.order"),
    path('order/edit/(?P<code>\d+)/page<int:num>/$', views.orderEdit, name="edit.order"),
    path('order/update/', views.orderUpdate, name="update.order"),
]
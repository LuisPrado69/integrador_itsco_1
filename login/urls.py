from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login),
    path('signin/', views.signin),

    path('technical/', views.technical, name="technical"),
    path('storeTechnical/', views.storeTechnical),

    path('incidence/', views.incidence, name="incidence"),
    path('storeIncidence/', views.storeIncidence)
]
from django.urls import path

from . import views

urlpatterns = [
    path('chefs/create/', views.ChefCreateView.as_view(), name='chef-create'),
]

from django.urls import path

from . import views

urlpatterns = [
    path('get_correlations', views.get_correlations, name="get_correlations"),
]

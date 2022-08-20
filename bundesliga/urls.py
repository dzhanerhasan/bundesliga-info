from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upcoming', views.upcoming_matches, name='upcoming'),
    path('stats', views.team_stats, name='stats'),
]

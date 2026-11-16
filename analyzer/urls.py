"""
URL patterns for the Analyzer app.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('delete/<int:pk>/', views.delete_feedback, name='delete_feedback'),
]

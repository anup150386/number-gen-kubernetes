# api/urls.py
from django.urls import path
from .views import TrackingNumberView

urlpatterns = [
    path('tracking-number/', TrackingNumberView.as_view(), name='tracking-number'),
]

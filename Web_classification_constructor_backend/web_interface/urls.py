from django.urls import path
from .views import button_click_tracking


urlpatterns = [
    path('', button_click_tracking, name='button_click_tracking')
]
from django.urls import path
from .views import button_click_tracking, button_click_tracking_2, button_click_tracking_3


urlpatterns = [
    path('', button_click_tracking, name='button_click_tracking'),
    path('2/', button_click_tracking_2, name='button_click_tracking_2'),
    path('3/', button_click_tracking_3, name='button_click_tracking_3'),
]

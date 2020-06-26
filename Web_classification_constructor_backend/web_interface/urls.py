from django.urls import path
from .views import button_click_tracking_main_page, button_click_tracking, button_click_tracking_2, \
    button_click_tracking_3, button_click_tracking_4, button_click_tracking_3_upload_mode, \
    button_click_tracking_4_upload_mode, show_process, info_page, authors


urlpatterns = [
    path('', button_click_tracking_main_page, name='button_click_tracking_main_page'),
    path('1/', button_click_tracking, name='button_click_tracking'),
    path('2/', button_click_tracking_2, name='button_click_tracking_2'),
    path('3/', button_click_tracking_3, name='button_click_tracking_3'),
    path('4/', button_click_tracking_4, name='button_click_tracking_4'),
    path('4/show_process/', show_process, name='show_process'),
    path('info/', info_page, name='info_page'),
    path('upload_model_mode/', button_click_tracking_3_upload_mode, name="button_click_tracking_3_upload_mode"),
    path('4_upload_mode/', button_click_tracking_4_upload_mode, name="button_click_tracking_4_upload_mode"),
    path('authors/', authors, name="authors")
]

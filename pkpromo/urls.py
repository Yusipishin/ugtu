from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='url_index'),
    path('send-main-form', views.send_main_form, name='url_send_main_form'),
    path('vrpromo', views.index_vr, name='url_send_main_form'),
    path('apply', views.apply_form, name='url_apply_form'),
    path('apply-ty', views.apply_ty, name='url_apply_ty'),
    #path('vk-widget', views.get_vk_widget, name='url_get_vk_widget'),
    #path('collected/', views.collected, name='login')
]
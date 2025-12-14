from django.urls import path

from main.views import get_main_page

urlpatterns = [
    path('', get_main_page),
]
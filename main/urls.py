from django.urls import path

from main.views import get_main_page, get_product_by_kategoria

urlpatterns = [
    path('', get_main_page, name = 'main'),
    path('kategoria/<int:id>/',get_product_by_kategoria, name = 'kategoria'),
]

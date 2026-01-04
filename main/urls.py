from django.urls import path

from main.views import get_main_page, get_product_by_kategoria, kartochka_tovar, add_tovar

urlpatterns = [
    path('', get_main_page, name = 'main'),
    path('kategoria/<int:id>/',get_product_by_kategoria, name = 'kategoria'),
    path('kartochka_tovar/<int:id>/', kartochka_tovar, name = 'kartochka'),
    path('add_tovar/',add_tovar,name="add_tovar")
]

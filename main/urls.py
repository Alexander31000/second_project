from django.urls import path

from main.views import get_main_page, get_product_by_kategoria, kartochka_tovar, add_tovar, redaktor_page, \
    mas_create_product_page, login_page, registracia_page, log_out, redactor_user
from orders.views import order_create

urlpatterns = [
    path('', get_main_page, name = 'main'),
    path('kategoria/<int:id>/',get_product_by_kategoria, name = 'kategoria'),
    path('kartochka_tovar/<int:id>/', kartochka_tovar, name = 'kartochka'),
    path('add_tovar/',add_tovar,name="add_tovar"),
    path('redaktor_tovar/<int:id>',redaktor_page, name='redaktor'),
    path('mas/',mas_create_product_page, name = 'mas'),
    path('login/', login_page, name = 'login'),
    path('reg/', registracia_page, name = 'registr'),
    path('logout/',log_out, name = 'log_out'),
    path('redactor_user/', redactor_user, name='redactor_user'),
    path('orders/', order_create, name='orders'),


]

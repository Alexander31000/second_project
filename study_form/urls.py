from django.urls import path

from study_form.views import get_form, get_django_form

urlpatterns = [
    path('', get_form),
    path('django_form/',get_django_form)

]
from django.http import HttpResponse
from django.shortcuts import render

from main.models import Tovar, Kategoria


# Create your views here.

def get_main_page(request):
    kategoriii = Kategoria.objects.all()
    tovars = Tovar.objects.all()
    # print(kategoriii)

    context = {'tovars':tovars, 'kategorii':kategoriii}
    return render(request, 'main.html', context)


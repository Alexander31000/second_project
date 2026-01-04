from django.http import HttpResponse
from django.shortcuts import render

from main import forms
from main.forms import TovarForm
from main.models import Tovar, Kategoria, TovarImage


# Create your views here.

def get_main_page(request):
    kategoriii = Kategoria.objects.all()
    tovars = Tovar.objects.all()

    context = {'tovars': tovars, 'kategorii': kategoriii}
    return render(request, 'main.html', context)


def get_product_by_kategoria(request, id):
    kategoriii = Kategoria.objects.all()
    tovars = Tovar.objects.filter(kategoria=id)

    context = {'tovars': tovars, 'kategorii': kategoriii}
    return render(request, 'main.html', context)


def kartochka_tovar(request, id):
    kategoriii = Kategoria.objects.all()
    tovar = Tovar.objects.get(id=id)
    tovar_imgs = TovarImage.objects.filter(tovar=id)
    tovar_imgs2 = tovar.tovarimage_set.all()
    print(tovar_imgs)
    print(tovar_imgs2)
    context = {
        'tovar': tovar,
        'kategorii': kategoriii,
        'tovar_imgs': tovar_imgs, }
    return render(request, 'kartochka_tovar.html', context)


def add_tovar(request):
    form = TovarForm()
    print(request.FILES)
    if request.method == "POST":
        # new_tovar = Tovar.objects.create(title=request.POST.get('title')) #разве вот так нельзя добавить новую форму  с товаром?
        form = TovarForm(request.POST,request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            new_tovar = Tovar(
                title=form.cleaned_data['title'],
                img=form.cleaned_data['img'],
                prise = form.cleaned_data['prise'],
                opisanie = form.cleaned_data['opisanie'],
                kategoria = form.cleaned_data['kategoria'],
            )
            new_tovar.save()

            additionals_img = form.cleaned_data['additional_img']
            if additionals_img:
                for i in additionals_img:
                    additional_img = TovarImage(
                        img = i,
                        tovar = new_tovar,
                    )
                    additional_img.save()



    context = {
        'form': form,
    }
    return render(request, 'add_tovar.html', context)

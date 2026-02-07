from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from cart.forms import CartAddProductForm
from main import forms
from main.forms import TovarForm, RedaktorTovarForm, RedaktorTovarImageForm, TovarImageForm, TovarModelForm, LoginForm, \
    RegistrForm, ChangeCredentionalForm
from main.models import Tovar, Kategoria, TovarImage


# Create your views here.

def get_main_page(request):
    kategoriii = Kategoria.objects.all()
    tovars = Tovar.objects.all()
    request.session['key'] = 'hi'


    context = {'tovars': tovars, 'kategorii': kategoriii}
    return render(request, 'main.html', context)


def get_product_by_kategoria(request, id):
    kategoriii = Kategoria.objects.all()
    tovars = Tovar.objects.filter(kategoria=id)

    context = {'tovars': tovars, 'kategorii': kategoriii}
    return render(request, 'main.html', context)


def kartochka_tovar(request, id):
    cart_product_form = CartAddProductForm()
    kategoriii = Kategoria.objects.all()
    tovar = Tovar.objects.get(id=id)
    tovar_imgs = TovarImage.objects.filter(tovar=id)
    tovar_imgs2 = tovar.tovarimage_set.all()
    context = {
        'tovar': tovar,
        'kategorii': kategoriii,
        'tovar_imgs': tovar_imgs,
        'cart_product_form':cart_product_form
    }
    return render(request, 'kartochka_tovar.html', context)


def add_tovar(request):
    form = TovarForm()
    if request.method == "POST":
        form = TovarForm(request.POST, request.FILES)
        if form.is_valid():
            new_tovar = Tovar(
                title=form.cleaned_data['title'],
                # создание нового объекта модели и заполнение его title тайтлом из формы
                img=form.cleaned_data['img'],
                prise=form.cleaned_data['prise'],
                opisanie=form.cleaned_data['opisanie'],
                kategoria=form.cleaned_data['kategoria'],
            )
            new_tovar.save()

            additionals_img = form.cleaned_data['additional_img']
            if additionals_img:
                for i in additionals_img:
                    additional_img = TovarImage(  # создание объекта модели где img становится i (файл одной картинки)
                        img=i,
                        tovar=new_tovar,
                        # по сути обращаемся не к полю модели TovarImage а просим брать информацию у нашего нового товара где мы уже поменяли информацию
                    )
                    additional_img.save()

    context = {
        'form': form,
    }
    return render(request, 'add_tovar.html', context)


def redaktor_page(request, id):
    tovar = Tovar.objects.get(id=id)
    additional_image = TovarImage.objects.filter(
        tovar=tovar)  # найти все записи модели TovarImage где поле tovar равно объекту tovar

    initial_imgs = [{'img': i.img, 'id': i.id} for i in additional_image]
    di = {
        "title": tovar.title,
        "img": tovar.img,
        "price": tovar.prise,
        "opisanie": tovar.opisanie,
        "kategoria": tovar.kategoria
    }
    form = RedaktorTovarForm(initial=di)
    form_set = TovarImageForm(initial=initial_imgs)
    if request.method == "POST":
        form = RedaktorTovarForm(request.POST, request.FILES, initial=di)
        form_set = TovarImageForm(request.POST, request.FILES, initial=initial_imgs)
        if form.is_valid():
            if form.has_changed():
                for key, value in form.cleaned_data.items():
                    if value is not None and value != getattr(tovar, key):
                        setattr(tovar, key, value)
                tovar.save()
            if form_set.is_valid():
                if form_set.has_changed():
                    for form_img in form_set:
                        if form_img.has_changed():
                            if form_img.cleaned_data.get('id') in [i.id for i in additional_image]:
                                instance = TovarImage.objects.filter(id=form.cleaned_data.get('id'))
                                instance.img = form_img.cleaned_data.get('img')
                                instance.save()
                            else:
                                new_img = TovarImage(img=form_img.cleaned_data.get('img'), tovar=tovar)
                                new_img.save()
            TovarImage.objects.filter(
                id__in=[delete_form.cleaned_data.get('id') for delete_form in form_set.deleted_forms]).delete()
        return redirect('kartochka', tovar.id)

    context = {
        'tovar': tovar,
        'form': form,
        'form_set': form_set
    }
    return render(request, 'redaktor.html', context)


def mas_create_product_page(request):
    form = TovarModelForm()
    form2 = TovarModelForm()
    if request.method == 'POST':
        form = TovarModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    context = {
        'form': form,
        # 'form2': form2
    }
    return render(request, 'mas.html', context)


def login_page(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(
                request,
                username=username,
                password=password
            )
            if user is not None:
                login(request, user)
                return redirect('main')
            else:
                form.add_error(None, 'Неверный логин или пароль')


    context = {
        'form': form,
    }
    return render(request, 'login.html', context)

def redactor_user(request):

    user = request.user
    form = ChangeCredentionalForm(initial={"username":user.username})


    if request.method == 'POST':
        form = ChangeCredentionalForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if username != user.username:
                user.username = username
                print(username)
            if password:
                user.set_password(password)
                print(user.check_password(password))
            user.save()

    context = {
        'form':form
    }

    return render(request, 'redactor_user.html', context)


def registracia_page(request):
    form = RegistrForm()
    if request.method == 'POST':
        form = RegistrForm(request.POST)
        if form.is_valid():
            user = User(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if User.objects.filter( username=form.cleaned_data['username']):
                form.add_error('username', 'имя уже существует')
            else:
                user.set_password(form.cleaned_data['password'])
                user.save()
                print(user)
                return redirect('main')

    context = {
        'form': form,
    }
    return render(request, 'registracia.html', context)

def log_out(request):
    logout(request)
    return redirect('main')




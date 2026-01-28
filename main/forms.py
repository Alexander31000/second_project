from django import forms

from main import models
from main.models import Kategoria, Tovar
from django.contrib.auth.password_validation import validate_password


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class TovarForm(forms.Form):
    title = forms.CharField(max_length=150)
    img = forms.ImageField()
    prise = forms.DecimalField(max_digits=10, decimal_places=2)
    opisanie = forms.CharField(widget = forms.Textarea)
    kategoria = forms.ModelChoiceField(queryset=Kategoria.objects.all())
    additional_img = MultipleFileField(required=False)



class RedaktorTovarForm(forms.Form):
    title = forms.CharField(max_length=150)
    img = forms.ImageField()
    prise = forms.DecimalField(max_digits=10, decimal_places=2)
    opisanie = forms.CharField(widget = forms.Textarea)
    kategoria = forms.ModelChoiceField(queryset=Kategoria.objects.all())
    additional_img = MultipleFileField(required=False)


class RedaktorTovarImageForm (forms.Form):
    img = forms.ImageField()
    id = forms.IntegerField(widget = forms.HiddenInput(),required=False)
    # delete = forms.BooleanField()

TovarImageForm = forms.formset_factory(RedaktorTovarImageForm, can_delete=True)



class TovarModelForm(forms.ModelForm): #позволяет на основании модели сделать форму
    additional_image = MultipleFileField(required=False)

    class Meta:
        model = Tovar
        fields = '__all__'


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150, widget = forms.PasswordInput)



class RegistrForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150, validators=[validate_password], widget = forms.PasswordInput)
    password_protect = forms.CharField(max_length=150, widget = forms.PasswordInput)

    def clean(self):
            cleaned_data = super().clean()
            if cleaned_data.get('password') != cleaned_data.get('password_protect'):
                self.add_error('password_protect', 'Пароли не совпадают')








from django import forms

from main.models import Kategoria

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



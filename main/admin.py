from django.contrib import admin

from main.models import Kategoria, Tovar, TovarImage

# Register your models here.

admin.site.register(Kategoria)
admin.site.register(Tovar)
admin.site.register(TovarImage)

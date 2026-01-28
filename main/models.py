from django.db import models

# Create your models here.

class Kategoria(models.Model):
    title = models.CharField(max_length = 50)

    def __str__(self):
        return self.title

class Tovar(models.Model):
    title = models.CharField(max_length = 150)
    img = models.ImageField(upload_to='tovar')
    prise = models.DecimalField(max_digits=10, decimal_places=2)
    opisanie = models.TextField()
    kategoria = models.ForeignKey(Kategoria,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class TovarImage(models.Model):
    img = models.ImageField(upload_to = 'tovar_image')
    tovar = models.ForeignKey(Tovar, on_delete=models.CASCADE)









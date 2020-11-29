from django.db import models

from users.models import MyUser
from products.models import Product
from django import forms
from django.forms import ModelForm
from django.core.validators import MaxValueValidator, MinValueValidator
#RATE_CHOICES = [
 #   (1, '1'),
  #  (2, '2'),
   # (3, '3'),
   # (4, '4'),
   # (5, '5'),
#]
class HistoricoAlugados(models.Model):
    locador = models.ForeignKey(MyUser,  null=True, blank=True, related_name='historico_user_locador', on_delete=models.SET_NULL)
    locatario = models.ForeignKey(MyUser,  null=True, blank=True, related_name='historico_user_locatario', on_delete=models.SET_NULL)
    produto = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    encerrado = models.BooleanField(default=False)

    avaliadoPeloLocador = models.BooleanField(default=False)
    avaliadoPeloLocatario = models.BooleanField(default=False)


class Rating(models.Model):
    de = models.ForeignKey(MyUser,  null=True, blank=True, related_name='avaliar_user_locador', on_delete=models.SET_NULL)
    para = models.ForeignKey(MyUser,  null=True, blank=True, related_name='avaliar_user_locatario', on_delete=models.SET_NULL)
    #user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    text = models.TextField(max_length=3000, blank=True)
    #textlocatario = models.TextField(max_length=3000, blank=True)
    rate = models.IntegerField(default=0,validators=[MaxValueValidator(5),MinValueValidator(0),])
    #ratelocatario = models.IntegerField(default=0)


class RatingForm(ModelForm):
    class Meta:
        model = Rating
        fields = ['text', 'rate']



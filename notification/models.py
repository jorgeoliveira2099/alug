from django.db import models

from users.models import MyUser
from Chat.models import Mensagem
from products.models import Product

from django.dispatch import receiver
from django.db.models.signals import post_save
import django.dispatch
# Create your models here.

class Notification(models.Model):

    title = models.ForeignKey(Product, null=True, blank=True,on_delete=models.CASCADE)
    
    #tentar assim: colocar esse campo e ver se o campo vai puxar pelo channels
    
    message = models.ForeignKey(Mensagem, null=True, blank=True,on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, null=True, blank=True,on_delete=models.CASCADE)
    #title =  models.CharField(max_length=80)    
    viewed = models.BooleanField(default=False)
    #e esses dois campos, do jeito que estavam, puxando os dados 
    #destino = models.CharField(max_length=80) 
    #receptor = models.CharField(max_length=80) 


def add_message(sender, instance, created, **kwargs):
  
    # isso aqui é o terceiro usuario
    message = instance
    print('add messa ge aquiiiiiiiiii')
    print(message)
    print('add messa ge aquiiiiiiiiii')
    sender = sender
    print(sender)

    #comment = instance
    user = message.user
    #text_preview = comment.body[:90]
    #sender = comment.user
    #notify = Notification(post=post, sender=sender, user=post.user, text_preview=text_preview ,notification_type=2)
    #notify.save()





#post_save.connect(add_message, sender=Mensagem)


  #esse bloco dá certo
    if created:
        Notification.objects.create(message=instance,user=user)
    else:
        instance.notification.save()
    
post_save.connect(add_message, sender=Mensagem)
  #esse bloco dá certo
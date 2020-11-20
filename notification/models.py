from django.db import models

from users.models import MyUser
from Chat.models import Mensagem
from products.models import Product, Alugar

from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import django.dispatch


class Notification(models.Model):
    
    NOTIFICATION_TYPES = ((1,'Mensagem'),(2,'Aluguel'), (3,'Aceito'), (4,'Devolucao'), (5, 'Cancelamento'))
        
    message = models.ForeignKey(Mensagem, null=True, blank=True,on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, null=True, blank=True,on_delete=models.CASCADE)      
    viewed = models.BooleanField(default=False)
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES,null=True, blank=True)

def add_message(sender, instance, created, **kwargs):  
    
    message = instance    
    sender = sender    
    user = message.user
   
    if created:
        Notification.objects.create(message=instance,user=user,notification_type=1)
    else:
        instance.notification.save()
    
post_save.connect(add_message, sender=Mensagem)

def add_alugar(sender, instance, created, **kwargs):  
    
    message = instance    
    sender = sender    
    
    user = message.locador
    locatario = message.locatario
    print(locatario)    
    
    if created:
        Notification.objects.create(user=user,notification_type=2)        
    else:  
        #aqui, o user, deve ser o locatario,
        #pois receberá a mensagem que a negociação foi aceita      
        Notification.objects.create(user=locatario,notification_type=3) 
            
post_save.connect(add_alugar, sender=Alugar)

def delete_alugar(sender, instance, **kwargs):    
    message = instance    
    sender = sender    
    user = message.locatario

    if message.confirmado == False:
        Notification.objects.create(user=user,notification_type=5)        
    else:
        Notification.objects.create(user=user,notification_type=4) 

post_delete.connect(delete_alugar, sender=Alugar)
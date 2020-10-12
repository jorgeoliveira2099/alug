
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render



def index(request):
    #title: 'Meu chat'
    return render(request, 'main.html', {})

def room(request, room_name):    
    return render(request, 'chat.html', {
        'room_name': room_name

    })
    #return HttpResponse('Chat Page '+room_name+' '+person_name)
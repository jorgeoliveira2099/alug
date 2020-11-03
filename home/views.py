from django.shortcuts import render, redirect
from django.contrib.auth import logout

def home(request):
    return render(request, 'home/home.html')

def my_logout(request):
    logout(request)
    return redirect('home')

def termosDeUso(request):
    return render(request, 'home/termosdeuso.html')

def perguntasFrequentes(request):
    return render(request, 'home/perguntasfrequentes.html')


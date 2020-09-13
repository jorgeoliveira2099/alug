from django.shortcuts import render, redirect
from .admin import UserCreationForm
from django.urls import reverse_lazy

def register(request):
    form = UserCreationForm(request.POST or None)
    sucess_url = reverse_lazy('login')

    if form.is_valid():
        form.save()
        return redirect(sucess_url)

    return render(request, 'registration/register.html', {'form': form})

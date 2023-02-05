from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .forms import SingUpForm


def frontpage(request):
    return render(request, 'core/page.html')


def singup(request):
    if request.method == "POST":
        form = SingUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('front')
    
    else:
        form = SingUpForm()

    return render(request, 'core/sigunp.html', {'form' : form})
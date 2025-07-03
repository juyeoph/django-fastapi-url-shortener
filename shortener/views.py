from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import URL
from .forms import URLCreationForm

@login_required(login_url='/login/')
def my_urls_view(request):

    if request.method == 'POST':
        form = URLCreationForm(request.POST)
        if form.is_valid():
            new_url = form.save(commit=False)
            new_url.owner = request.user
            new_url.save()
            return redirect('my_urls')
    else:
        form = URLCreationForm()

    user_urls = URL.objects.filter(owner=request.user).order_by('-created_at')

    context = {
        'url_list': user_urls,
        'form': form,
    }
    return render(request, 'shortener/my_urls.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('my_urls')
    else:
        form = UserCreationForm()

    return render(request, 'shortener/signup.html', {'form': form})
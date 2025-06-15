from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'Convoiturage/index.html')

def register(request):
    return render(request, 'Convoiturage/register.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('success_page')  # Rediriger vers une page de succès
            else:
                # Gestion de l'échec de connexion (par exemple, afficher un message d'erreur)
                return render(request, 'login.html', {'form': form, 'error_message': 'Invalid credentials'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

from django.shortcuts import render

def success_view(request):
    return render(request, 'success.html')  # Exemple de page de succès, à créer dans le dossier templates
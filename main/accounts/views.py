from django.contrib import auth
from django.contrib.auth import authenticate
from django.http import request
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import FormContato


def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.error(request, 'Usuario ou senha invalidos.')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request,'Logado com sucesso.')
        return redirect('dashboard')



def logout(request):
    auth.logout(request)
    return redirect('dashboard')



def cadastro(request):
    if request.method != 'POST':
        return render(request, 'accounts/cadastro.html')

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    if not nome or not sobrenome or not email or not usuario or not senha \
        or not senha2:
        messages.error(request, 'Nenhum campo pode estar vazio.')
        return render(request, 'accounts/cadastro.html')
    try:
        validate_email(email)
    except:
        messages.error(request, 'Email invalido.')

    if len(senha) <6:
        messages.error(request, 'Senha Muito Curta, Precisa ter 6 caracteres ou mais.')
        return render(request, 'accounts/cadastro.html')

    if len(usuario) <4:
        messages.error(request, 'Nome de usuario muito curta, Precisa ter 4 caracteres ou mais.')
        return render(request, 'accounts/cadastro.html')

    if senha != senha2:
        messages.error(request, 'Senhas n??o conferem.')
        return render(request, 'accounts/cadastro.html')

    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'Usuario j?? existe.')
        return render(request, 'accounts/cadastro.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'Email j?? existe.')
        return render(request, 'accounts/cadastro.html')

    messages.success(request, 'Registrado com sucesso!' )

    user = User.objects.create_user(username=usuario, email=email,
                                    password=senha, first_name=nome,
                                    last_name=sobrenome)
    user.save()
    return redirect('login')


@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = FormContato()
        return render(request, 'accounts/dashboard.html', {'form': form })

    form = FormContato(request.POST, request.FILES)

    if  not form.is_valid():
        messages.ERROR(request, 'Erro ao enviar o formulario.')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form })

    form.save()
    messages.success(request, f'contato de {request.POST.get("nome")} foi salvo com sucesso.')
    return redirect('dashboard')


 
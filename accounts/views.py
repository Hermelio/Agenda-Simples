from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import ContatoForm


def login(request):

    if request.method != 'POST':
        return render(request, 'accounts/login.html')
    # pegando os dados do formulario
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    # ele retorna um none caso esteja errado
    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.error(request, 'Usuário ou Senha inválidos')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, 'Login com Sucesso!')
        return redirect('dashboard')


def logout(request):
    auth.logout(request)
    return redirect('login')


def cadastro(request):
    if request.method != 'POST':
        return render(request, 'accounts/cadastro.html')

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    usuario = request.POST.get('usuario')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    valida_senha = request.POST.get('senha2')

    if not nome or not sobrenome or not usuario or not email \
            or not senha or not valida_senha:
        messages.error(request, 'Nenhuma campo pode estar vazio.')
        return render(request, 'accounts/cadastro.html')
    # validando o email
    try:
        validate_email(email)
    except:
        messages.error(request, 'Email inválido.')
        return render(request, 'accounts/cadastro.html')

    if len(senha) < 6:
        messages.error(request, 'Senha precisa ter mais de 6 caracteres.')
        return render(request, 'accounts/cadastro.html')

    if len(senha) < 6:
        messages.error(request, 'Usuário precisa ter mais de 6 caracteres.')
        return render(request, 'accounts/cadastro.html')

    if senha != valida_senha:
        messages.error(request, 'Senha não conferem')
        return render(request, 'accounts/cadastro.html')
# ------------------------------------------------------------------
# validando usuario e email se ja existem dentro do nosso sistema pela classe User
    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'Usuário já existe')
        return render(request, 'accounts/cadastro.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'E-mail já existe')
        return render(request, 'accounts/cadastro.html')

    messages.success(request, 'Registrado com Sucesso! Faça seu Login')

    user = User.objects.create_user(username=usuario, email=email,
                                    password=senha, first_name=nome,
                                    last_name=sobrenome)
    user.save()
    return redirect('login')


@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = ContatoForm()
        return render(request, 'accounts/dashboard.html', {'form': form})
    # o files eh pq tem upload de imagem no formulario
    form = ContatoForm(request.POST, request.FILES)

    if not form.is_valid():
        messages.error(request, 'Erro no formulário')
        form = ContatoForm(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    form.save()
    messages.success(request, f'Contato {request.POST.get("nome")} Salvo!')
    return redirect('dashboard')


def inicio(request):
    return render(request, 'accounts/inicio.html')

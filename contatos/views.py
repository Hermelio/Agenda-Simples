
from django.http.response import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Contato
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages


def index(request):
    uruario = request.user
    redic = 'accounts/login.html'
    if uruario:
        redirect('accounts/login')
        return render(request, redic)
    contatos = Contato.objects.order_by('id').filter(mostrar=True)
    paginator = Paginator(contatos, 6)

    page = request.GET.get('p')
    contatos = paginator.get_page(page)
    return render(request, 'contatos/index.html', {
        'contatos': contatos
    })


def detalhes(request, id):
    uruario = request.user
    redic = 'accounts/login.html'
    if uruario:
        redirect('accounts/login')
        return render(request, redic)
    # contato = Contato.objects.get(id=id)
    contato = get_object_or_404(Contato, id=id)  # tratado erros

    if not contato.mostrar:
        raise Http404()

    return render(request, 'contatos/detalhes.html', {
        'contato': contato
    })


def busca(request):
    uruario = request.user
    redic = 'accounts/login.html'
    if uruario:
        redirect('accounts/login')
        return render(request, redic)

    # pegando o termo que é escrito no campo pesquisa
    termo = request.GET.get('termo')
    if termo is None or not termo:
        messages.add_message(request, messages.ERROR,
                             'Campo não pode ficar vazio.')
        # se o campo pesquisa estiver vazio ou for none ele retorna o index com o erro
        return redirect('index')
    campos = Concat('nome', Value(' '), 'sobrenome')
    # contatos = Contato.objects.order_by('id').filter(
    #     Q(nome__icontains=termo) | Q(sobrenome__icontains=termo),
    #     mostrar=True)
    # buscando o que foi digitado agora ele busca em todos os campos com nome
    # e sobrenome e telefone ele procura ou por um ou pelo outro
    contatos = Contato.objects.annotate(
        nome_completo=campos
    ).filter(
        Q(nome_completo__icontains=termo)
        | Q(telefone__icontains=termo)
    )

    paginator = Paginator(contatos, 6)

    page = request.GET.get('p')
    contatos = paginator.get_page(page)
    return render(request, 'contatos/busca.html', {
        'contatos': contatos
    })


def teste(request):
    return render(request, 'contatos/base1.html')

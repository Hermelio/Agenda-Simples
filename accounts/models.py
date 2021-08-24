from django.db import models
from contatos.models import Contato
from django import forms


class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato  # esse formulario representa o contato
        exclude = ()  # nao estou excluindo nada

from django.contrib import admin
from .models import Contato, Categoria


# essa classe ajusta a apresentação dos dados no admin por coluna


class ContatoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'sobrenome',
                    'telefone', 'email', 'categoria', 'mostrar')
    list_display_links = ('id', 'nome', 'sobrenome')  # colcoa link para edicao
    list_editable = ('telefone', 'mostrar')
    # list_filter = ('nome', 'sobrenome')  # filtra por nome e sobrenome
    list_per_page = 10  # paginacao na pagina
    search_fields = ('nome', 'sobrenome', 'telefone')  # pesquisa por filtro


admin.site.register(Contato, ContatoAdmin)
admin.site.register(Categoria)

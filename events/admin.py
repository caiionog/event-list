from django.contrib import admin
from .models import Event, SolicitacaoAcesso

admin.site.register(Event)

@admin.register(SolicitacaoAcesso)
class SolicitacaoAcessoAdmin(admin.ModelAdmin):
    list_display = ('user', 'data_solicitacao', 'aprovado')
    list_filter = ('aprovado',)
    search_fields = ('user__nickname', 'mensagem')
    actions = ['aprovar_solicitacoes', 'negar_solicitacoes']

    def aprovar_solicitacoes(self, request, queryset):
        for solicitacao in queryset:
            solicitacao.aprovado = True
            solicitacao.save()
            solicitacao.user.is_autorizado_eventos = True
            solicitacao.user.save()
        self.message_user(request, f"{queryset.count()} solicitações foram aprovadas.")

    def negar_solicitacoes(self, request, queryset):
        queryset.update(aprovado=False)
        self.message_user(request, f"{queryset.count()} solicitações foram negadas.")

    aprovar_solicitacoes.short_description = "Aprovar solicitações selecionadas"
    negar_solicitacoes.short_description = "Negar solicitações selecionadas"


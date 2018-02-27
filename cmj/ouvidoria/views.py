
from braces.views import FormMessagesMixin
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.urlresolvers import reverse, reverse_lazy
from django.http.response import Http404
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView
from sapl.crispy_layout_mixin import CrispyLayoutFormMixin

from cmj.core.forms_auth import LoginForm
from cmj.ouvidoria.forms import DenunciaForm, SolicitacaoForm,\
    MensagemSolicitacaoForm
from cmj.ouvidoria.models import Solicitacao, MensagemSolicitacao
from cmj.utils import make_pagination


opts_bg = {
    10: 'bg-green',
    20: 'bg-blue',
    30: 'bg-orange',
    40: 'bg-yellow',
    900: 'bg-red-danger',
}


class DenunciaAnonimaFormView(FormMessagesMixin, CreateView):
    form_valid_message, form_invalid_message = (
        _('Sua denúncia anônima foi encaminha.'),
        _('Houve um erro no envio de sua mensagem.'))
    model = Solicitacao
    form_class = DenunciaForm
    template_name = 'ouvidoria/denuncia_form.html'

    def get_context_data(self, **kwargs):

        context = CreateView.get_context_data(self, **kwargs)
        return context

    def get_success_url(self):
        return reverse('cmj.ouvidoria:denuncia_form')

    def get_initial(self):
        initial = CreateView.get_initial(self)
        initial.update({'logged_user':
                        bool(self.request.user.is_authenticated)})
        return initial

    def get(self, request, *args, **kwargs):
        response = CreateView.get(self, request, *args, **kwargs)
        if self.request.user.is_authenticated:
            logout(request)

        return response


class SolicitacaoDetailView(PermissionRequiredMixin,
                            CrispyLayoutFormMixin,
                            DetailView):
    model = Solicitacao
    template_name = 'ouvidoria/denuncia_anonima_detail.html'
    permission_required = 'ouvidoria.detail_solicitacao'
    layout_key = 'DenunciaAnonimaDetailLayout'

    @property
    def extras_url(self):
        return [
            (reverse('cmj.ouvidoria:solicitacao_manage_list'),
             'btn-default',
             _('Listar outras Solcitações')
             )
        ]

    def has_permission(self):
        self.object = self.get_object()

        if self.object.owner == self.request.user:
            return True
        elif super().has_permission():
            is_operador = self.object.areatrabalho.operadores.filter(
                pk=self.request.user.pk).exists()

            if is_operador:
                return True
        raise Http404()

    def get(self, request, *args, **kwargs):
        self.object.notificacoes.unread().filter(
            user=request.user).update(
                read=True,
                modified=timezone.now())

        if self.object.owner:
            return redirect(
                reverse_lazy('cmj.ouvidoria:solicitacao_interact',
                             kwargs=kwargs))

        return DetailView.get(self, request, *args, **kwargs)


class SolicitacaoListMixin:
    model = Solicitacao
    paginate_by = 10
    no_entries_msg = _('Nenhum registro encontrado.')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        count = self.object_list.count()
        context = super().get_context_data(**kwargs)
        context['count'] = count

        # pagination
        if self.paginate_by:
            page_obj = context['page_obj']
            paginator = context['paginator']
            context['page_range'] = make_pagination(
                page_obj.number, paginator.num_pages)

        # rows
        object_list = context['object_list']
        context['NO_ENTRIES_MSG'] = self.no_entries_msg
        context['subnav_template_name'] = 'ouvidoria/subnav_list.yaml'

        return context


class SolicitacaoManageListView(SolicitacaoListMixin,
                                PermissionRequiredMixin,
                                ListView):
    template_name = 'ouvidoria/solicitacao_manage_list.html'
    permission_required = 'ouvidoria.list_solicitacao'

    def get_queryset(self):
        qs = ListView.get_queryset(self)

        qs = qs.filter(
            notificacoes__user=self.request.user
        ).order_by('notificacoes__read', '-created')
        return qs


class SolicitacaoListView(SolicitacaoListMixin, ListView):
    template_name = 'ouvidoria/solicitacao_minhas_list.html'

    @property
    def extras_url(self):
        return [
            (reverse('cmj.ouvidoria:solicitacao_create'),
             'btn-success',
             _('Abrir Nova Solicitação')
             ),
            (reverse('cmj.ouvidoria:denuncia_form'),
             'btn-danger',
             _('Fazer uma Denúncia Anônima')
             )
        ]

    def get_queryset(self):
        qs = ListView.get_queryset(self)

        qs = qs.filter(owner=self.request.user).order_by(
            'notificacoes__read', '-created')
        return qs


@method_decorator(login_required, name='dispatch')
class SolicitacaoFormView(FormMessagesMixin, CreateView):
    form_valid_message, form_invalid_message = (
        _('Sua solicitação foi encaminha...'),
        _('Houve um erro no envio de sua mensagem.'))
    model = Solicitacao
    form_class = SolicitacaoForm
    template_name = 'ouvidoria/solicitacao_form.html'

    def get_context_data(self, **kwargs):
        context = CreateView.get_context_data(self, **kwargs)

        tipo = int(self.request.GET.get('tipo', '10'))

        tipos = Solicitacao.TIPO_SOLICITACAO_CHOICE

        context['title'] = _(
            'Registar uma Solicitação: (%s)') % tipos.triple_map[tipo]['text']

        context['bg_title'] = opts_bg[tipo]

        return context

    def get_initial(self):
        initial = CreateView.get_initial(self)
        initial.update({'owner':
                        self.request.user})

        tipo = self.request.GET.get('tipo', '10')

        initial.update({'tipo': tipo})

        return initial

    def get_success_url(self):
        return reverse_lazy(
            'cmj.ouvidoria:solicitacao_interact',
            kwargs={'pk': self.object.id})


class SolicitacaoMensagemRedirect(RedirectView):
    pattern_name = 'cmj.ouvidoria:solicitacao_interact'

    def get_redirect_url(self, *args, **kwargs):
        try:
            msg = MensagemSolicitacao.objects.get(pk=kwargs['pk'])
            kwargs['pk'] = msg.solicitacao.pk
        except:
            raise Http404()

        return RedirectView.get_redirect_url(self, *args, **kwargs)


class SolicitacaoInteractionView(PermissionRequiredMixin, FormView):

    form_class = MensagemSolicitacaoForm
    template_name = 'ouvidoria/solicitacao_interact.html'
    permission_required = ('ouvidoria.detail_mensagemsolicitacao')

    def dispatch(self, request, *args, **kwargs):
        try:
            self.object = Solicitacao.objects.get(pk=self.kwargs['pk'])
        except:
            raise Http404()

        return super().dispatch(request, *args, **kwargs)

    def has_permission(self):

        if self.object.owner == self.request.user:
            return True
        elif super().has_permission():
            is_operador = self.object.areatrabalho.operadores.filter(
                pk=self.request.user.pk).exists()

            if is_operador:
                return True
        raise Http404()

    def get_initial(self):

        initial = FormView.get_initial(self)
        initial.update({'owner':
                        self.request.user})
        initial.update({'solicitacao':
                        self.object})

        return initial

    def get_context_data(self, **kwargs):

        context = FormView.get_context_data(self, **kwargs)
        context['solicitacao'] = self.object

        self.object.notificacoes.filter(
            user=self.request.user).update(read=True)

        for ms in self.object.mensagemsolicitacao_set.all():
            ms.notificacoes.filter(
                user=self.request.user).update(read=True)

        context['bg_title'] = opts_bg[self.object.tipo]
        context['subnav_template_name'] = 'ouvidoria/subnav_list.yaml'
        return context

    def get_success_url(self):
        return reverse_lazy(
            'cmj.ouvidoria:solicitacao_interact', kwargs=self.kwargs)

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


class OuvidoriaPaginaInicialView(LoginView):
    template_name = 'ouvidoria/pagina_inicial.html'
    authentication_form = LoginForm

    def get_success_url(self):

        return reverse_lazy(
            'cmj.ouvidoria:ouvidoria_pagina_inicial', kwargs=self.kwargs)

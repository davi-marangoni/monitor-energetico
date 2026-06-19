from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from aplicativos.energia.models import ConfiguracaoEnergetica
from aplicativos.maquinas.models import Maquina

from .auth_utils import armazenar_tokens_jwt_na_sessao, limpar_tokens_jwt_da_sessao
from .forms import CadastroForm, LoginForm, MaquinaEditForm, PerfilForm
from .services import (
    listar_maquinas_com_status,
    montar_contexto_dashboard,
    montar_contexto_maquina,
    obter_maquina_do_usuario,
    obter_ou_criar_configuracao,
)


class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        armazenar_tokens_jwt_na_sessao(self.request, self.request.user)
        return response


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        limpar_tokens_jwt_da_sessao(request)
        return super().dispatch(request, *args, **kwargs)


class CadastroView(CreateView):
    template_name = 'pages/cadastro.html'
    form_class = CadastroForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'Conta criada com sucesso. Faça login para continuar.')
        return super().form_valid(form)


@login_required
def dashboard_view(request):
    context = montar_contexto_dashboard(request.user)
    return render(request, 'pages/dashboard.html', context)


@login_required
def maquinas_list_view(request):
    maquinas = listar_maquinas_com_status(request.user)
    return render(request, 'pages/machines_list.html', {'maquinas': maquinas})


@login_required
def maquina_detail_view(request, pk):
    maquina = get_object_or_404(Maquina, pk=pk, usuario=request.user)
    context = montar_contexto_maquina(maquina)
    return render(request, 'pages/machine.html', context)


@login_required
def maquina_edit_view(request, pk):
    maquina = get_object_or_404(Maquina, pk=pk, usuario=request.user)

    if request.method == 'POST':
        form = MaquinaEditForm(request.POST, instance=maquina)
        if form.is_valid():
            form.save()
            messages.success(request, 'Máquina atualizada com sucesso.')
            return redirect('maquina_detail', pk=maquina.pk)
    else:
        form = MaquinaEditForm(instance=maquina)

    return render(request, 'pages/machine_edit.html', {'form': form, 'machine': maquina})


@login_required
def configuracao_energetica_view(request, pk):
    maquina = get_object_or_404(Maquina, pk=pk, usuario=request.user)
    config = obter_ou_criar_configuracao(maquina)
    return render(request, 'pages/configuration.html', {'machine': maquina, 'config': config})


@login_required
def configuracoes_global_view(request):
    configs = ConfiguracaoEnergetica.objects.filter(
        maquina__usuario=request.user
    ).select_related('maquina').order_by('-atualizado_em')
    return render(request, 'pages/configurations_list.html', {'configs': configs})


class PerfilView(LoginRequiredMixin, UpdateView):
    template_name = 'pages/profile.html'
    form_class = PerfilForm
    success_url = reverse_lazy('perfil')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Perfil atualizado com sucesso.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['maquinas_count'] = Maquina.objects.filter(usuario=self.request.user).count()
        return context

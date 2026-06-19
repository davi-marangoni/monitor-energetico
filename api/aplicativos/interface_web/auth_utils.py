from rest_framework_simplejwt.tokens import RefreshToken


def armazenar_tokens_jwt_na_sessao(request, user):
    refresh = RefreshToken.for_user(user)
    request.session['jwt_access'] = str(refresh.access_token)
    request.session['jwt_refresh'] = str(refresh)


def limpar_tokens_jwt_da_sessao(request):
    request.session.pop('jwt_access', None)
    request.session.pop('jwt_refresh', None)

from rest_framework import status, authentication, exceptions
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.authentication import get_authorization_header

from applications.users.auth.authentication import ExpiringTokenAuthentication
from applications.users.models import User

#NO SIRVE

'''
class Authentication(authentication.BaseAuthentication):
    user = None

    def get_user(self, request):
        token = get_authorization_header(request).split()
        if token:
            try:
                token = token[1].decode()
            except:
                return None
            token_expire = ExpiringTokenAuthentication()
            user = token_expire.authenticate_credentials(token)
            if user is not None:
                self.user = user
                return user

        return None

    def authenticate(self, request):
        user_login = None
        token_logout = None
        try:
            user_login = request.data['username']
        except:
            pass
        try:
            token_logout = request.data['token']
        except:
            pass
        if user_login is None and token_logout is None:
            self.get_user(request)
            if self.user is None:
                raise exceptions.AuthenticationFailed('No se han enviado las credendiales')
        return self.user, None

'''


class NewAuthentication(authentication.BaseAuthentication):

    user = None

    def get_user(self, username):
        try:
            self.user = User.objects.filter(username=username).first()
        except:
            pass
        if self.user is not None:
            return user

        return None

    def authenticate(self, request):
        try:
            if request.data['username'] and request.data['password']:
                self.get_user(request.data['username'])
        except:
            pass

        if self.user is not None:
            return self.user, None

        return None, None


'''
Método cuando se ejecuta una clase de tipo object

    def dispatch(self, request, *args, **kwargs):
        user = self.get_user(request)
        if user is not None:
            return super().dispatch(request, *args, **kwargs)

        response = Response(
            {
                'error': 'No se han enviado las credenciales.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = 'application/json'
        response.renderer_context = {}
        return response
'''

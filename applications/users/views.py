# from datetime import datetime

from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.auth import login

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from applications.users.auth.serializers import LoginSerializer, LogoutSerializer, \
    CustomTokenRefreshSerializer

'''
class UserToken(APIView):

    def get(self, request, *args, **kwargs):
        try:
            user_token = Token.objects.get(user=request.user)
            user = UserTokenSerializer(request.user)
            return Response(
                {
                    'token': user_token.key,
                    'user': user.data
                },
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {
                    'error': 'Las credenciales enviadas son incorrectas.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
'''

'''
class Login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        login_serializer = self.serializer_class(data=request.data, context={'request': request})
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            if user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                user_serializer = UserTokenSerializer(user)
                if created:
                    return Response(
                        {
                            'token': token.key,
                            'user': user_serializer.data,
                            'message': 'Inicio de Sesión Exitoso'
                        },
                        status=status.HTTP_201_CREATED
                    )
                else:
                    all_sessions = Session.objects.filter(expire_date__gte=timezone.now())
                    if all_sessions.exists():
                        for session in all_sessions:
                            session_data = session.get_decoded()
                            if user.id == int(session_data.get('_auth_user_id')):
                                session.delete()
                    token.delete()
                    token = Token.objects.create(user=user)
                    return Response(
                        {
                            'token': token.key,
                            'user': user_serializer.data,
                            'message': 'Inicio de Sesión Exitoso'
                        },
                        status=status.HTTP_202_ACCEPTED
                    )
            else:
                return Response(
                    {
                        'error': 'Este usuario no puede iniciar sesión.'
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )
        else:
            return Response(
                {
                    'error': 'Nombre de usuario o contraseña incorrecta.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
'''

'''
class Logout(APIView):

    def post(self, request, *args, **kwargs):

        try:
            token = request.data['token']
            token = Token.objects.filter(key=token).first()
            if token:
                all_sessions = Session.objects.filter(expire_date__gte=timezone.now())
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()
                token.delete()

                session_message = 'Sesiones de usuario eliminadas'
                token_message = 'Token eliminado'
                return Response(
                    {
                        'session_message': session_message,
                        'token_message': token_message
                    }
                )

            return Response(
                {
                    'error': 'No se ha encontrado un usuario con estas credenciales.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except:
            return Response(
                {
                    'error': 'No se ha encontrado el token en la petición.'
                },
                status=status.HTTP_409_CONFLICT
            )
'''


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    '''
    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)
'''

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(
                {
                    'ok': True,
                    'conon_data': serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'ok': False,
                'error': 'No se ha encontrado un usuario con estas credenciales.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class LogoutView(GenericAPIView):

    """
    TODO: Investigar y hacer mas eficiente el eliminado de Sesiones
        por usuario, y evitar que entre en ese bucle
    """

    serializer_class = LogoutSerializer

    def post(self, request, *args):
        data_serializer = self.get_serializer(data=request.data)
        if data_serializer.is_valid():
            all_sessions = Session.objects.filter(expire_date__gte=timezone.now())
            if all_sessions.exists():
                for session in all_sessions:
                    session_data = session.get_decoded()
                    if request.user.id == int(session_data.get('_auth_user_id')):
                        session.delete()
            data_serializer.save()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {
                'ok': False,
                'detail': 'No se ha encontrado el token en la petición.'
            },
            status=status.HTTP_409_CONFLICT
        )


class RefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args):

        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                return Response(
                    {
                        'ok': True,
                        'conon_data': serializer.data
                    },
                    status=status.HTTP_200_OK
                )
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(
            {
                'ok': False,
                'detail': 'Token incorrecto.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

# from datetime import datetime

from django.contrib.sessions.models import Session
from django.utils import timezone

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from applications.users.api.api_user.serializers import UserTokenSerializer
from applications.users.auth.authentication_mixins import Authentication


# TODO: Mejorar el borrado de las sesiones
#   y hacer uso del método user_logged_in() de signals


# Create your views here.
class UserToken(APIView, Authentication):

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

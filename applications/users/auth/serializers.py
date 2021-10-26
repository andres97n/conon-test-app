from django.contrib import auth

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.state import token_backend

from applications.users.models import User


# TODO: Resolver el duplicado al momento de
#   hacer el logout y el token pase al Blackilist table

# TODO: Crea un serializador para el envío de la contraseña al correo
#   de cada usuario.


class LoginSerializer(serializers.ModelSerializer):
    uid = serializers.IntegerField(
        read_only=True
    )
    username = serializers.CharField(
        min_length=3,
        max_length=100,
    )
    email = serializers.EmailField(
        max_length=200,
        read_only=True
    ),
    type = serializers.IntegerField(
        read_only=True
    )
    password = serializers.CharField(
        max_length=50,
        write_only=True
    )

    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'uid',
            'username',
            'email',
            'type',
            'password',
            'tokens'
        ]

    # Get Tokens
    def get_tokens(self, obj):
        user = User.objects.get(username=obj['username'])

        return dict(
            access=user.get_tokens()['access'],
            refresh=user.get_tokens()['refresh'],
        )

    # Validate the user data and create a session
    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        # filtered_user_by_username = User.objects.filter(username=username)
        user = auth.authenticate(
            self.context.get('request'),
            username=username,
            password=password
        )

        '''
        if not filtered_user_by_username.exists():
            raise AuthenticationFailed(
                detail='Por favor ingrese un nombre de usuario válido.'
            )
        '''

        if not user:
            raise AuthenticationFailed(
                detail='Credenciales inválidas, por favor ingrese de nuevo los datos de usuario.'
            )
        if not user.is_active:
            raise AuthenticationFailed(
                detail='Cuenta deshabilitada, contacte con el administrador.'
            )

        if user is not None:
            auth.login(
                self.context.get('request'),
                user
            )

        return {
            'uid': user.id,
            'username': user.username,
            'email': user.email,
            'type': user.type,
            'tokens': user.get_tokens
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': 'Token expiró o es inválido'
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')

        # auth.logout(self.context.get('request'))


class CustomTokenRefreshSerializer(TokenRefreshSerializer):

    # Extract the user_id and return user data with the tokens
    def validate(self, attrs):
        data = super(CustomTokenRefreshSerializer, self).validate(attrs)
        decoded_payload = token_backend.decode(data['access'], verify=True)
        user_uid = decoded_payload['user_id']
        user = User.objects.filter(id=user_uid).first()
        data.update({
            'uid': user_uid,
            'username': user.username,
            'email': user.email,
            'type': user.type
        })
        # add filter query
        return data

    # Get data
    def to_representation(self, instance):
        return {
            'uid': instance['uid'],
            'username': instance['username'],
            'email': instance['email'],
            'type': instance['type'],
            'tokens': {
                'access': instance['access'],
                'refresh': instance['refresh']
            }
        }

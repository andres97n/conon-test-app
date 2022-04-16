
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from applications.users.models import User
from .serializers import UpdateUserSerializer
from applications.users.auth.serializers import PasswordSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def is_username_valid(request, username):
    if request.method == 'GET':
        if username:
            user = User.objects.get_user_by_username(username=username)
            if user is not None:
                user_serializer = UpdateUserSerializer(user)
                return Response(
                    {
                        'ok': True,
                        'conon_data': user_serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'Este Usuario no existe.'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se envío el Nombre de Usuario.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(
            {
                'ok': False,
                'detail': 'Método no permitido.'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def change_user_password(request, user):
    if request.method == 'POST':
        if user:
            user = User.objects.get_user_detail_data(pk=user)
            if user is not None:
                password_serializer = PasswordSerializer(data=request.data)
                if password_serializer.is_valid():
                    user.set_password(password_serializer.validated_data['password'])
                    user.save()
                    return Response({
                        'ok': True,
                        'message': 'Contraseña actualizada correctamente.'
                    })
                return Response({
                    'ok': False,
                    'detail': password_serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'Este Usuario no existe.'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se envío el Usuario.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(
            {
                'ok': False,
                'detail': 'Método no permitido.'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
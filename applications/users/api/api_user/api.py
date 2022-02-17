
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from applications.users.models import User


@api_view(['GET'])
@permission_classes([AllowAny])
def is_username_valid(request, username):
    if request.method == 'GET':
        if username:
            username_exists = User.objects.exists_username(username)
            if username_exists:
                return Response(
                    {
                        'ok': True,
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

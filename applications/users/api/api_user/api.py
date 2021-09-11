from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser

from applications.users.models import User
from applications.users.api.api_user.serializers import UserSerializer


# Create or Get all active users records
@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def user_api_view(request):
    if request.method == 'GET':
        users = User.objects.filter(is_active=True)
        user_serializer = UserSerializer(users, many=True)
        return Response(
            user_serializer.data,
            status=status.HTTP_200_OK
        )
    elif request.method == 'POST':
        user_serializer = UserCreateSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(
                {
                    'message': 'Usuario creado correctamente!!'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            user_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    else:
        return Response(
            {
                'error': 'Método no permitido'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def user_detail_api_view(request, pk=None):
    user = User.objects.filter(id=pk).first()

    if user:

        if request.method == 'GET':
            user_serializer = UserSerializer(user)
            return Response(
                user_serializer.data,
                status=status.HTTP_200_OK
            )
        elif request.method == 'PUT':
            user_serializer = UserSerializer(user, data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(
                    user_serializer.data,
                    status=status.HTTP_200_OK
                )
            return Response(
                user_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        elif request.method == 'DELETE':
            user.is_active = False
            user.auth_state = 'I'
            user.save()
            return Response(
                {
                    'message': 'Usuario eliminado correctamente.'
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'error': 'Método no permitido'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    return Response(
        {
            'error': 'No existe este Usuario.'
        },
        status=status.HTTP_400_BAD_REQUEST
    )

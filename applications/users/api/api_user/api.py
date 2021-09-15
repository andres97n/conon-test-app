from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser

from applications.users.models import User
from applications.users.paginations import CononPagination
from applications.users.api.api_user.serializers import UserSerializer, UserListSerializer


# Get all active users records
# Create a normal User
@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def user_api_view(request):

    # User List
    if request.method == 'GET':
        paginator = CononPagination()
        users = User.objects.user_list()
        context = paginator.paginate_queryset(users, request)
        user_serializer = UserListSerializer(context, many=True)

        return paginator.get_paginated_response(user_serializer.data)

    # Create User
    elif request.method == 'POST':
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()

            return Response(
                {
                    'message': 'Usuario creado correctamente.'
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


# Detail, Update and Delete of a normal User
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def user_detail_api_view(request, pk=None):
    user = User.objects.filter(id=pk).first()
    if user:

        # User Detail
        if request.method == 'GET':
            user_serializer = UserListSerializer(user)

            return Response(
                user_serializer.data,
                status=status.HTTP_200_OK
            )

        # Update User
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

        # Delete User
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

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser

from applications.users.models import User
from applications.users.api.serializers import UserSerializer


# Create or Get all active users records
@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def user_api_view(request):
    if request == 'GET':
        users = User.objects.filter(is_active=True)
        user_serializer = UserSerializer(users, many=True)
        return Response(
            user_serializer.data,
            status=status.HTTP_200_OK
        )
    elif request == 'POST':
        user_serializer = UserSerializer(data=request.data)
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

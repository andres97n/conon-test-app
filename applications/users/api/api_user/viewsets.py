from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from applications.base.paginations import CononPagination
from .serializers import UserSerializer


# TODO: API provisonal del Usuario, en un
#   futuro se espera cambiarlo


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = ([IsAdminUser])
    serializer_class = UserSerializer
    pagination_class = CononPagination

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_user_data()
        return self.get_serializer().Meta.model.objects.get_user_detail_data(pk)

    # Create User
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Usuario creado correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            user_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update User
    def update(self, request, pk=None, *args, **kwargs):
        user = self.get_queryset(pk)
        if user:
            # Send information to serializer referencing the instance
            user_serializer = self.serializer_class(user, data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()

                return Response(
                    {
                        'ok': True,
                        'conon_data': user_serializer.data
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'ok': False,
                    'detail': user_serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Usuario.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail User data
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            user_serializer = self.serializer_class(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': user_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Usuario.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete User
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        user = self.get_queryset(pk)
        if user:
            user.is_active = False
            user.auth_state = 'I'
            user.save()

            return Response(
                {
                    'ok': True,
                    'detail': 'Usuario eliminado correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Usuario.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )


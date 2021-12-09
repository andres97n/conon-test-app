from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_tracking.mixins import LoggingMixin

from applications.base.permissions import IsTeacher
from applications.base.paginations import CononPagination
from .serializers import UserSerializer, UpdateUserSerializer


# TODO: API provisonal del Usuario, en un
#   futuro se espera cambiarlo


class UserViewSet(LoggingMixin, viewsets.ModelViewSet):
    permission_classes = ([IsTeacher])
    serializer_class = UserSerializer
    pagination_class = CononPagination
    logging_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    sensitive_fields = {'access', 'refresh'}

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_user_data()
        return self.get_serializer().Meta.model.objects.get_user_detail_data(pk)

    # Get User List
    def list(self, request, *args, **kwargs):
        user_queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(user_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        user_serializer = self.get_serializer(user_queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': user_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create User
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        user_serializer = self.get_serializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()

            return Response(
                {
                    'ok': True,
                    'id': user_serializer.data['id'],
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
            user_serializer = UpdateUserSerializer(user, data=request.data)
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
            user_serializer = self.get_serializer(self.get_queryset(pk))

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
                    'message': 'Usuario eliminado correctamente.'
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

    # Delete Many Users
    @action(detail=False, methods=(['DELETE']), url_path='destroy-users')
    def destroy_users(self, request):
        users = self.get_serializer().Meta.model.objects.get_many_users(request.data['users'])
        if users:
            for user in users:
                user.is_active = False
                user.auth_state = 'I'

            self.get_serializer().Meta.model.objects.bulk_update(users, ['auth_state', 'is_active'])

            return Response(
                {
                    'ok': True,
                    'message': 'Usuarios eliminados correctamente.'
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'ok': False,
                'detail': 'Ocurrió un error con el proceso, consulte con el Administrador.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

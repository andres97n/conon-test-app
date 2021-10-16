from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from .serializers import DuaSerializer
from applications.base.permissions import IsOwnerAndTeacher


class DuaViewSet(viewsets.ModelViewSet):
    serializer_class = DuaSerializer
    permission_classes = ([IsOwnerAndTeacher])

    # Return DUA Data
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_dua_list()
        return self.get_serializer().Meta.model.objects.get_dua_by_id(pk)

    # Get DUA List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        dua_serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': dua_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create DUA
    def create(self, request, *args, **kwargs):
        dua_serializer = self.get_serializer(data=request.data)
        if dua_serializer.is_valid():
            dua_serializer.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Tema creado correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'ok': False,
                'detail': dua_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update DUA
    def update(self, request, pk=None, *args, **kwargs):
        dua = self.get_queryset(pk)
        if dua:
            # Send information to serializer referencing the instance
            dua_serializer = self.get_serializer(dua, data=request.data)
            if dua_serializer.is_valid():
                dua_serializer.save()

                return Response(
                    {
                        'ok': True,
                        'conon_data': dua_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'ok': False,
                    'detail': dua_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Tema de Estudio.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail DUA
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            dua_serializer = self.get_serializer(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': dua_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Tema de Estudio.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete DUA
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        dua = self.get_queryset(pk)
        if dua:
            dua.auth_state = 'I'
            dua.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Tema eliminado correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Tema de Estudio.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

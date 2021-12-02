from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework_tracking.mixins import LoggingMixin

from .serializers import GlossarySerializer
from applications.base.permissions import IsTeacher
from applications.base.paginations import CononPagination
from applications.school.models import GlossaryDetail


# The Teacher enable the Glosary for to add terms
class GlossaryViewSet(LoggingMixin, viewsets.ModelViewSet):
    permission_classes = ([IsTeacher])
    serializer_class = GlossarySerializer
    pagination_class = CononPagination
    logging_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    sensitive_fields = {'access', 'refresh'}

    # Return Glossary Data
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_glosary_list()
        return self.get_serializer().Meta.model.objects.get_glosary_by_id(pk)

    # Get Glossary List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        glossary_serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': glossary_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create a Glossary
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        glossary_serializer = self.get_serializer(data=request.data)
        if glossary_serializer.is_valid():
            glossary_serializer.save()

            return Response(
                {
                    'ok': True,
                    'id': glossary_serializer.data['id'],
                    'message': 'Glosario creado correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'ok': False,
                'detail': glossary_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Glossary
    def update(self, request, pk=None, *args, **kwargs):
        glossary = self.get_queryset(pk)
        if glossary:
            # Send information to serializer referencing the instance
            glossary_serializer = self.get_serializer(glossary, data=request.data)
            if glossary_serializer.is_valid():
                glossary_serializer.save()

                return Response(
                    {
                        'ok': True,
                        'conon_data': glossary_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'ok': False,
                    'detail': glossary_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Glosario.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Glossary Data
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            glossary_serializer = self.get_serializer(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': glossary_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Glosario.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Glossary
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        glossary = self.get_queryset(pk)
        if glossary:
            glossary.state = False
            glossary.auth_state = 'I'
            glossary.save()

            glossary_details = GlossaryDetail.objects.get_glossary_detail_by_glossary(pk=pk)
            if glossary_details is not None:

                for glossary_detail in glossary_details:
                    glossary_detail.state = 0
                    glossary_detail.auth_state = 'I'
                    glossary_detail.save()

                return Response(
                    {
                        'ok': True,
                        'message': 'Glosario eliminado correctamente.'
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se pudo eliminar por completo el detalle del glosario.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Glosario.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

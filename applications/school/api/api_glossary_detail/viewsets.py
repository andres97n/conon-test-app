from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import GlossaryDetailSerializer
from applications.base.permissions import IsTeacherOrIsStudent, IsTeacher
from applications.base.paginations import CononPagination


class GlossaryDetailViewSet(LoggingMixin, viewsets.ModelViewSet):
    serializer_class = GlossaryDetailSerializer
    pagination_class = CononPagination
    logging_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    sensitive_fields = {'access', 'refresh'}
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['glossary', 'state']

    # Set Permissions
    def get_permissions(self):
        if self.action == 'destroy':
            permission_classes = [IsTeacher]
        else:
            permission_classes = [IsTeacherOrIsStudent]
        return [permission() for permission in permission_classes]

    # Return Glossary Detail Data
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_glosary_detail_list()
        return self.get_serializer().Meta.model.objects.get_glosary_detail_by_id(pk)

    # Get Terms List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        glossary_detail_serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': glossary_detail_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create a Term
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        glossary_detail_serializer = self.get_serializer(data=request.data)
        if glossary_detail_serializer.is_valid():
            glossary_detail_serializer.save()

            return Response(
                {
                    'ok': True,
                    'id': glossary_detail_serializer.data['id'],
                    'message': 'Término creado correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'ok': False,
                'detail': glossary_detail_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Term
    def update(self, request, pk=None, *args, **kwargs):
        term = self.get_queryset(pk)
        if term:
            # Send information to serializer referencing the instance
            glossary_detail_serializer = self.get_serializer(term, data=request.data)
            if glossary_detail_serializer.is_valid():
                glossary_detail_serializer.save()

                return Response(
                    {
                        'ok': True,
                        'conon_data': glossary_detail_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'ok': False,
                    'detail': glossary_detail_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Término.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Term
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            glossary_detail_serializer = self.get_serializer(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': glossary_detail_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Término.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Term
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        term = self.get_queryset(pk)
        if term:
            term.state = 0
            term.auth_state = 'I'
            term.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Término eliminado correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Término.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['DELETE'], url_path='destroy-terms')
    def destroy_glossaries_detail(self, request):
        if request.data:
            terms = self.get_serializer().Meta.model.objects.get_many_glossaries_detail(
                terms=request.data['terms']
            )
            if terms is not None:
                for glossary_detail in terms:
                    glossary_detail.state = 0
                    glossary_detail.auth_state = 'I'

                self.get_serializer().Meta.model.objects.bulk_update(
                    terms, ['state', 'auth_state']
                )

                return Response(
                    {
                        'ok': True,
                        'message': 'Términos elimnados correctamente.'
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'ok': False,
                    'detail': 'No se encontraron los términos a envíar.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            
            return Response(
                {
                    'ok': False,
                    'detail': 'No se enviaron los términos a eliminar.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    # Block Glossary Detail
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_glossary_detail(self, request, pk=None):
        glossary_detail = self.get_queryset(pk)
        if glossary_detail:
            glossary_detail.state = 0
            glossary_detail.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Término bloqueado correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Término.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

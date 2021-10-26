from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework_tracking.mixins import LoggingMixin

from applications.base.paginations import CononPagination
from .serializers import PersonSerializer


class PersonViewSet(LoggingMixin, viewsets.ModelViewSet):
    permission_classes = ([IsAdminUser])
    serializer_class = PersonSerializer
    pagination_class = CononPagination
    logging_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    sensitive_fields = {'access', 'refresh'}

    # Return Person data
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_person_list()
        return self.get_serializer().Meta.model.objects.get_person_detail_data(pk)

    # Get Person List
    def list(self, request, *args, **kwargs):
        person_queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(person_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        person_serializer = self.get_serializer(person_queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': person_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Person
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        person_serializer = self.get_serializer(data=request.data)
        if person_serializer.is_valid():
            person_serializer.save()

            return Response(
                {
                    'ok': True,
                    'id': person_serializer.data['id'],
                    'message': 'Persona creada correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'ok': False,
                'detail': person_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Person
    def update(self, request, pk=None, *args, **kwargs):
        person = self.get_queryset(pk)
        if person:
            # Send information to serializer referencing the instance
            person_serializer = self.get_serializer(person, data=request.data)
            if person_serializer.is_valid():
                person_serializer.save()

                return Response(
                    {
                        'ok': True,
                        'conon_data': person_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'ok': False,
                    'detail': person_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Persona.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Person data
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            person_serializer = self.get_serializer(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': person_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Persona.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Person
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        person = self.get_queryset(pk)
        if person:
            person.auth_state = 'I'
            person.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Persona eliminada correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Persona.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from applications.base.paginations import CononPagination
from .serializers import PersonSerializer


class PersonViewSet(viewsets.ModelViewSet):
    permission_classes = ([IsAdminUser])
    serializer_class = PersonSerializer
    pagination_class = CononPagination

    # Return Person data
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_person_list()
        return self.get_serializer().Meta.model.objects.get_person_detail_data(pk)

    # Create Person
    def create(self, request, *args, **kwargs):

        # Send information to serializer
        person_serializer = self.serializer_class(data=request.data)
        if person_serializer.is_valid():
            person_serializer.save()

            return Response(
                {
                    'message': 'Persona creada correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            person_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Person
    def update(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):

            # Send information to serializer referencing the instance
            person_serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if person_serializer.is_valid():
                person_serializer.save()

                return Response(
                    person_serializer.data,
                    status=status.HTTP_200_OK
                )

            return Response(
                person_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'error': 'No existe esta Persona.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Person data
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            person_serializer = self.serializer_class(self.get_queryset(pk))

            return Response(
                person_serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'error': 'No existe esta Persona.'
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
                    'message': 'Persona eliminada correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'error': 'No existe esta Persona.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

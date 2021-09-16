from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser

from applications.users.models import Person
from applications.users.paginations import CononPagination
from applications.users.api.api_person.serializers import PersonSerializer, PersonListSerializer


# TODO: Aplicar permisos para que el Docente
#   utilizar la API

# Get all active person records
# Create a person
@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def person_api_view(request):

    # Person List
    if request.method == 'GET':
        paginator = CononPagination()
        persons = Person.objects.filter(auth_state='A').order_by('last_name')
        context = paginator.paginate_queryset(persons, request)
        person_serializer = PersonListSerializer(context, many=True)

        return paginator.get_paginated_response(person_serializer.data)

    # Create Person
    elif request.method == 'POST':
        person_serializer = PersonSerializer(data=request.data)
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
    else:
        return Response(
            {
                'error': 'Método no permitido.'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


# Detail, Update and Delete of a Person
@api_view(['GET', 'PUT', 'DELETE'])
def person_detail_api_view(request, pk=None):
    person = Person.objects.filter(id=pk).first()

    if person:

        # Person Detail
        if request.method == 'GET':
            person_serializer = PersonListSerializer(person)

            return Response(
                person_serializer.data,
                status=status.HTTP_200_OK
            )

        # Update Person
        elif request.method == 'PUT':
            person_serializer = PersonSerializer(person, data=request.data)
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

        # Delete Person
        elif request.method == 'DELETE':
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
                'error': 'Método no permitido.'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    return Response(
        {
            'error': 'No existe esta Persona.'
        },
        status=status.HTTP_400_BAD_REQUEST
    )


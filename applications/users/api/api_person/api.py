from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from applications.users.models import Person
from applications.users.api.api_person.serializers import PersonSerializer, PersonCreateSerializer


@api_view(['GET', 'POST'])
def person_api_view(request):
    if request.method == 'GET':
        persons = Person.objects.filter(auth_state='A')
        person_serializer = PersonSerializer(persons, many=True)
        return Response(
            person_serializer.data,
            status=status.HTTP_200_OK
        )
    elif request.method == 'POST':
        person_serializer = PersonCreateSerializer(data=request.data)
        if person_serializer.is_valid():

            person_serializer.save()
            return Response(
                {
                    'message': 'Persona creada correctamente!!'
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
                'error': 'Método no permitido'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(['GET', 'PUT', 'DELETE'])
def person_detail_api_view(request, pk=None):
    person = Person.objects.filter(id=pk).first()

    if person:

        if request.method == 'GET':
            print(person)
            person_serializer = PersonSerializer(person)
            return Response(
                person_serializer.data,
                status=status.HTTP_200_OK
            )
        elif request.method == 'PUT':
            person_serializer = PersonCreateSerializer(person, data=request.data)
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
                'error': 'Método no permitido'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    return Response(
        {
            'error': 'No existe esta Persona.'
        },
        status=status.HTTP_400_BAD_REQUEST
    )


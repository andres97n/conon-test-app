
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from applications.users.models import Person
from applications.topic.models import Topic
from applications.school.models import SchoolPeriod
from applications.topic.api.api_topic.serializers import TopicSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_topics_list_by_student(request, user):
    if request.method == 'GET':
        if user:
            person = Person.objects.get_person_by_user(user)
            print(person.student.id)
            if person and person.student:
                school_period = SchoolPeriod.objects.get_period_active()
                topics = Topic.objects.get_topics_by_students(person.student.id, school_period.id)
                print(school_period)
                topic_serializer = TopicSerializer(topics, many=True)

                return Response(
                    {
                        'ok': True,
                        'conon_data': topic_serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se encontró la información del Usuario.'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se envío el Usuario.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(
            {
                'ok': False,
                'detail': 'Método no permitido.'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

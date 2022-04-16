from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from applications.base.permissions import IsStudent
from applications.dua.models import ActivityStudent, Answer
from .serializers import ActivityStudentByActivityAndOwnerSerializer
from applications.dua.api.api_answer.serializers import AnswerByActivityStudentSerializer


@api_view(['GET'])
@permission_classes([IsStudent])
def get_student_activity_with_details(request, activity, owner):
    if request.method == 'GET':
        if activity and owner:
            activity_student_dua = ActivityStudent.objects.activity_student_by_activity_and_owner(
                activity=activity, owner=owner
            )
            print(activity_student_dua)
            if activity_student_dua is not None:
                activity_student_with_answers = []
                if not activity_student_dua:
                    activity_student_with_answers = [{
                        "activity_student": {},
                        "answers": []
                    }]
                else:
                    activity_student_serializer = ActivityStudentByActivityAndOwnerSerializer(
                        activity_student_dua.first()
                    )
                    activity_student_answers = Answer.objects.get_answers_by_activity_student(
                        activity_student=activity_student_serializer.data['id']
                    )
                    if activity_student_answers is not None:
                        questions_serializer = AnswerByActivityStudentSerializer(
                            activity_student_answers, many=True
                        )
                        activity_student_with_answers.append({
                            "activity_student": activity_student_serializer.data,
                            "answers": questions_serializer.data
                        })
                    else:
                        activity_student_with_answers.append({
                            "activity_student": activity_student_serializer.data,
                            "answers": []
                        })
                return Response(
                    {
                        'ok': True,
                        'conon_data': activity_student_with_answers
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se pudo encontrar la Actividad realizada por el Estudiante.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se enviaron los valores correspondientes para la consulta.'
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


@api_view(['GET'])
@permission_classes([IsStudent])
def get_is_student_activity_exists(request, activity, owner):
    if request.method == 'GET':
        if activity and owner:
            activity_student_dua = ActivityStudent.objects.\
                is_activity_student_exists_by_activity_and_owner(activity=activity, owner=owner)
            if activity_student_dua:
                return Response(
                    {
                        'ok': True,
                        'conon_data': activity_student_dua
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': True,
                        'conon_data': activity_student_dua
                    },
                    status=status.HTTP_200_OK
                )

        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se enviaron los valores correspondientes para la consulta.'
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

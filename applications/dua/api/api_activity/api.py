from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from applications.base.permissions import IsTeacher
from applications.dua.models import Activity, Question
from .serializers import ActivityByDuaSerializer
from applications.dua.api.api_question.serializers import QuestionByActivitySerializer


@api_view(['GET'])
@permission_classes([IsTeacher])
def get_activity_with_questions(request, dua):
    if request.method == 'GET':
        if dua:
            activity_dua = Activity.objects.get_activity_by_dua(dua=dua)
            if activity_dua is not None:
                activity_with_questions = []
                if not activity_dua:
                    activity_with_questions = [{
                        "activity": {},
                        "questions": []
                    }]
                else:
                    activity_serializer = ActivityByDuaSerializer(
                        activity_dua.first()
                    )
                    activity_questions = Question.objects.get_questions_by_activity(
                        activity=activity_serializer.data['id']
                    )
                    if activity_questions is not None:
                        questions_serializer = QuestionByActivitySerializer(
                            activity_questions, many=True
                        )
                        activity_with_questions.append({
                            "activity": activity_serializer.data,
                            "questions": questions_serializer.data
                        })
                    else:
                        activity_with_questions.append({
                            "activity": activity_serializer.data,
                            "questions": []
                        })
                return Response(
                    {
                        'ok': True,
                        'conon_data': activity_with_questions
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se pudo encontrar la metodología DUA enviada.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se envío la Metodología DUA.'
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

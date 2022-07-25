
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from applications.base.permissions import IsTeacherOrIsStudent
from applications.ac.models import StudentEvaluationAc, StudentEvaluationDetailAc
from .serializers import StudentEvaluationAcShortListSerializer
from applications.ac.api.api_student_evaluation_detail_ac.serializers import \
    StudentEvaluationDetailAcShortListSerializer


@api_view(['GET'])
@permission_classes([IsTeacherOrIsStudent])
def get_evaluation_ac_with_details(request, rubric, team_detail_ac):
    if request.method == 'GET':
        if rubric and team_detail_ac:
            evaluation_ac = StudentEvaluationAc.objects.get_evaluation_ac_by_rubric_and_team_detail(
                rubric=rubric, team_detail=team_detail_ac
            )
            if evaluation_ac is not None:
                evaluation_with_details = []
                if not evaluation_ac:
                    evaluation_with_details = [{
                        "evaluation": {},
                        "details": []
                    }]
                else:
                    evaluation_ac_serializer = StudentEvaluationAcShortListSerializer(
                        evaluation_ac.first()
                    )
                    evaluation_details = StudentEvaluationDetailAc.objects. \
                        get_evaluation_details_by_evaluation_ac(
                            evaluation=evaluation_ac_serializer.data['id']
                        )
                    if evaluation_details is not None:
                        evaluation_detail_serializer = StudentEvaluationDetailAcShortListSerializer(
                            evaluation_details, many=True
                        )
                        evaluation_with_details.append({
                            "evaluation": evaluation_ac_serializer.data,
                            "details": evaluation_detail_serializer.data
                        })
                    else:
                        evaluation_with_details.append({
                            "evaluation": evaluation_ac_serializer.data,
                            "details": []
                        })
                return Response(
                    {
                        'ok': True,
                        'conon_data': evaluation_with_details
                    },
                    status=status.HTTP_200_OK
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se enviaron los valores necesarios para la consulta.'
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
@permission_classes([IsTeacherOrIsStudent])
def get_student_evaluation_ac_with_details(request, ac, team_detail_ac):
    if request.method == 'GET':
        if ac and team_detail_ac:
            evaluation_ac = StudentEvaluationAc.objects.\
                get_student_evaluation_ac_by_ac_and_team_detail(ac=ac, team_detail=team_detail_ac)
            if evaluation_ac is not None:
                evaluation_with_details = []
                if not evaluation_ac:
                    evaluation_with_details = [{
                        "evaluation": {},
                        "details": []
                    }]
                else:
                    evaluation_ac_serializer = StudentEvaluationAcShortListSerializer(
                        evaluation_ac.first()
                    )
                    evaluation_details = StudentEvaluationDetailAc.objects. \
                        get_evaluation_details_by_evaluation_ac(
                            evaluation=evaluation_ac_serializer.data['id']
                        )
                    if evaluation_details is not None:
                        evaluation_detail_serializer = StudentEvaluationDetailAcShortListSerializer(
                            evaluation_details, many=True
                        )
                        evaluation_with_details.append({
                            "evaluation": evaluation_ac_serializer.data,
                            "details": evaluation_detail_serializer.data
                        })
                    else:
                        evaluation_with_details.append({
                            "evaluation": evaluation_ac_serializer.data,
                            "details": []
                        })
                return Response(
                    {
                        'ok': True,
                        'conon_data': evaluation_with_details
                    },
                    status=status.HTTP_200_OK
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se enviaron los valores necesarios para la consulta.'
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

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from applications.base.permissions import IsTeacherOrIsStudent
from applications.abp.models import EvaluationAbp, EvaluationDetailAbp
from .serializers import EvaluationAbpByAbpSerializer
from applications.abp.api.api_evaluation_detail_abp.serializers import \
    EvaluationDetailAbpListByEvaluationSerializer


@api_view(['GET'])
@permission_classes([IsTeacherOrIsStudent])
def get_evaluation_apb_with_details(request, abp, team_detail_abp):
    if request.method == 'GET':
        if abp and team_detail_abp:
            evaluation_abp = EvaluationAbp.objects.get_evaluation_abp_by_abp_and_team_detail(
                abp=abp, team_detail=team_detail_abp
            )
            if evaluation_abp is not None:
                evaluation_with_details = []
                if not evaluation_abp:
                    evaluation_with_details = [{
                        "evaluation": {},
                        "details": []
                    }]
                else:
                    evaluation_abp_serializer = EvaluationAbpByAbpSerializer(
                        evaluation_abp.first()
                    )
                    evaluation_details = EvaluationDetailAbp.objects. \
                        get_evaluation_details_by_evaluations(
                            evaluation=evaluation_abp_serializer.data['id']
                        )
                    if evaluation_details is not None:
                        evaluation_detail_serializer = EvaluationDetailAbpListByEvaluationSerializer(
                            evaluation_details, many=True
                        )
                        evaluation_with_details.append({
                            "evaluation": evaluation_abp_serializer.data,
                            "details": evaluation_detail_serializer.data
                        })
                    else:
                        evaluation_with_details.append({
                            "evaluation": evaluation_abp_serializer.data,
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
                        'detail': 'No se pudo encontrar la Evaluación.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
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

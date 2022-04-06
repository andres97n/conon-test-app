from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from applications.ac.models import TeamAc, TeamDetailAc
from .serializers import TeamAcShortListSerializer
from applications.ac.api.api_team_detail_ac.serializers import TeamDetailAcShortListSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_student_team_abp(request, ac, user):
    if request.method == 'GET':
        if ac and user:
            team_ac = TeamAc.objects.team_ac_by_ac(ac=ac, user=user)
            if team_ac is not None:
                current_team_ac = []
                if not team_ac:
                    current_team_ac.append({
                        "team_ac": {},
                        "team_detail_ac": []
                    })
                else:
                    team_ac_serializer = TeamAcShortListSerializer(team_ac.first())
                    team_detail_ac = TeamDetailAc.objects.get_team_detail_by_team_ac(
                        team=team_ac_serializer.data['id']
                    )
                    if team_detail_ac is not None:
                        team_detail_ac_serializer = TeamDetailAcShortListSerializer(
                            current_team_ac, many=True
                        )
                        current_team_ac.append({
                            "team_ac": team_ac_serializer.data,
                            "team_detail_ac": team_detail_ac_serializer.data
                        })
                    else:
                        return Response(
                            {
                                'ok': False,
                                'detail': 'No se pudo encontrar a los estudiantes del grupo.'
                            },
                            status=status.HTTP_404_NOT_FOUND
                        )
                return Response(
                    {
                        'ok': True,
                        'conon_data': current_team_ac
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se encontró el grupo del estudiante enviado.'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se enviaron los valores necesarios para procesar.'
                },
                status=status.HTTP_404_NOT_FOUND
            )
    else:
        return Response(
            {
                'ok': False,
                'detail': 'Método no permitido.'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

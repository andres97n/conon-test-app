
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from applications.ac.models import TeamDetailAc
from applications.ac_roles.models import ProblemResolutionGroupAc
from .serializers import ProblemResolutionGroupAcSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_team_featured_information(request, team_detail):
    if request.method == 'GET':
        if team_detail:
            team_detail_ac = TeamDetailAc.objects.get_team_ac_active_object_queryset(pk=team_detail)
            if team_detail_ac is not None:
                problem_resolution = ProblemResolutionGroupAc.objects. \
                    get_problem_resolution_by_team()
                if problem_resolution is not None:
                    problem_resolution_serializer = ProblemResolutionGroupAcSerializer(
                        problem_resolution.first()
                    )

                    return Response(
                        {
                            'ok': True,
                            'conon_data': problem_resolution_serializer.data
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {
                            'ok': False,
                            'detail': 'No se pudo encontrar la solución del problema.'
                        },
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se pudo encontrar el integrante.'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se envio la información necesaria.'
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

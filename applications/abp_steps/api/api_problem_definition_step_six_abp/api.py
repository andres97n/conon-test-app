
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from applications.base.permissions import IsStudent
from applications.abp_steps.models import (ProblemDefinitionStepSixAbp,
                                           ProblemDefinitionReferenceStepSixAbp)
from .serializers import ProblemDefinitionStepSixAbpListSerializer
from applications.abp_steps.api.api_problem_definition_reference_step_six_abp.serializers import \
    ProblemDefinitionReferenceStepSixAbpByTeamSerializer


@api_view(['GET'])
@permission_classes([IsStudent])
def get_problem_definition_with_references(request, team):
    if request.method == 'GET':
        if team:
            problem_team = ProblemDefinitionStepSixAbp.objects.\
                get_problem_definition_by_team(team)
            if problem_team is not None:
                team_definition_and_references = []
                if not problem_team:
                    team_definition_and_references = [{
                        "problem_definition": {},
                        "references": []
                    }]
                else:
                    problem_team_serializer = ProblemDefinitionStepSixAbpListSerializer(
                        problem_team.first()
                    )
                    definition_references = ProblemDefinitionReferenceStepSixAbp.objects.\
                        get_definition_reference_by_team(team, reference_active=True)
                    if definition_references is not None:
                        reference_serializer = ProblemDefinitionReferenceStepSixAbpByTeamSerializer(
                            definition_references, many=True
                        )
                        team_definition_and_references.append({
                            "problem_definition": problem_team_serializer.data,
                            "references": reference_serializer.data
                        })
                    else:
                        team_definition_and_references.append({
                            "problem_definition": problem_team_serializer.data,
                            "references": []
                        })
                return Response(
                    {
                        'ok': True,
                        'conon_data': team_definition_and_references
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se encontró el problema del equipo, revise la referencia '
                                  'del equipo.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se envió el Equipo.'
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

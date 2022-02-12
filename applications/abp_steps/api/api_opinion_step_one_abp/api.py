
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from applications.base.permissions import IsStudent
from applications.abp.models import TeamDetailAbp
from applications.abp_steps.models import OpinionStepOneAbp
from applications.abp_steps.api.api_opinion_step_one_abp.serializers import \
    OpinionAbpByTeamAbpSerializer
from applications.abp_steps.api.api_interaction_step_one_abp.serializers import \
    InteractionStepOneByOpinionSerializer


@api_view(['GET'])
@permission_classes([IsStudent])
def get_opinions_by_team_and_user(request, team, user):
    if request.method == 'GET':
        if team and user:
            opinions = TeamDetailAbp.objects.get_opinions_step_one_by_user(team, user)
            if opinions is not None:
                opinion_serializer = OpinionAbpByTeamAbpSerializer(opinions, many=True)
                return Response(
                    {
                        'ok': False,
                        'conon_data': opinion_serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se encontró ningún valor.'
                    },
                    status=status.HTTP_404_NOT_FOUND
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
@permission_classes([IsStudent])
def get_opinions_and_interactions_by_team_and_user(request, team, user):
    if request.method == 'GET':
        if team and user:
            opinions = TeamDetailAbp.objects.get_opinions_step_one_exclude_user(team, user)
            if opinions is not None:
                opinions_data = []
                opinion_serializer = OpinionAbpByTeamAbpSerializer(opinions, many=True)
                for opinion in opinion_serializer.data:
                    interactions = OpinionStepOneAbp.objects.\
                        get_interactions_step_one_abp_by_opinion(opinion.id)
                    if interactions:
                        interaction_serializer = InteractionStepOneByOpinionSerializer(
                            interactions, many=True
                        )
                        opinions_data.append({interaction_serializer.data, opinion})
                return Response(
                    {
                        'ok': False,
                        'conon_data': opinions_data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se encontró ningún valor.'
                    },
                    status=status.HTTP_404_NOT_FOUND
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

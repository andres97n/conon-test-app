
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from applications.base.permissions import IsStudent
from applications.abp.models import TeamDetailAbp
from applications.abp_steps.models import OpinionStepOneAbp, InteractionStepOneAbp
from applications.abp_steps.api.api_opinion_step_one_abp.serializers import \
    OpinionAbpByTeamAbpSerializer, OpinionStepOneAbpSerializer
from applications.abp_steps.api.api_interaction_step_one_abp.serializers import \
    InteractionStepOneByOpinionSerializer


@api_view(['GET'])
@permission_classes([IsStudent])
def get_opinions_by_team_detail(request, team_detail):
    if request.method == 'GET':
        if team_detail:
            opinions = TeamDetailAbp.objects.get_opinions_step_one_by_user(team_detail)
            if opinions is not None:
                opinion_serializer = OpinionAbpByTeamAbpSerializer(opinions, many=True)
                return Response(
                    {
                        'ok': True,
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
            opinions = TeamDetailAbp.objects.\
                get_opinions_step_one_exclude_user(team, user)
            if opinions is not None:
                opinions_data = []
                opinion_serializer = OpinionAbpByTeamAbpSerializer(opinions, many=True)
                for opinion in opinion_serializer.data:
                    interactions = InteractionStepOneAbp.objects.\
                        get_interaction_by_opinion(opinion['id'])
                    if interactions is not None:
                        interaction_serializer = InteractionStepOneByOpinionSerializer(
                            interactions, many=True
                        )
                        opinions_data.append(
                            {'opinion': opinion, 'interactions': interaction_serializer.data}
                        )
                    else:
                        opinions_data.append(
                            {'opinion': opinion, 'interactions': []}
                        )
                return Response(
                    {
                        'ok': True,
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


@api_view(['GET'])
@permission_classes([IsStudent])
def get_opinions_step_one_count(request, team):
    if request.method == 'GET':
        if team:
            opinions_count = OpinionStepOneAbp.objects.get_opinion_count_by_team_detail(team)
            if opinions_count is not None:
                return Response(
                    {
                        'ok': True,
                        'conon_data': opinions_count
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se encontró el estudiante enviado.'
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
def get_team_opinions_and_interactions(request, team):
    if request.method == 'GET':
        if team:
            team_opinions = OpinionStepOneAbp.objects.get_team_opinions_abp_list(team)
            if team_opinions is not None:
                team_opinions_and_interactions = []
                team_opinions_serializer = OpinionStepOneAbpSerializer(team_opinions, many=True)
                for opinion in team_opinions_serializer.data:
                    interactions = InteractionStepOneAbp.objects.get_interaction_by_opinion(
                        opinion['id']
                    )
                    if interactions is not None:
                        interactions_serializer = InteractionStepOneByOpinionSerializer(
                            interactions, many=True
                        )
                        team_opinions_and_interactions.append({
                            'opinion': opinion,
                            'interactions': interactions_serializer.data
                        })
                    else:
                        team_opinions_and_interactions.append({
                            'opinion': opinion,
                            'interactions': []
                        })
                return Response(
                    {
                        'ok': True,
                        'conon_data': team_opinions_and_interactions
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se encontró información con el equipo enviado.'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se envío el grupo correspondiente.'
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

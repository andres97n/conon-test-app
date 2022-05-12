from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from applications.ac.models import TeamAc, TeamDetailAc
from .serializers import TeamAcShortListSerializer
from applications.ac.api.api_team_detail_ac.serializers import (TeamDetailAcShortListSerializer,
                                                                TeamDetailAcSerializer)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_student_team_abc(request, ac, user):
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
                            team_detail_ac, many=True
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_team_detail_ac_by_user(request, ac, user):
    if request.method == 'GET':
        if ac and user:
            user_data = TeamDetailAc.objects.get_team_detail_ac_by_ac_and_owner(ac=ac, owner=user)
            if user_data is not None:
                user_data_serializer = TeamDetailAcSerializer(user_data)
                return Response(
                    {
                        'ok': True,
                        'conon_data': user_data_serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se pudo encontrar la información del Usuario.'
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_team_ac_with_students(request, ac):
    if request.method == 'GET':
        if ac:
            team_ac = TeamAc.objects.get_team_ac_by_ac(ac=ac)
            if team_ac is not None:
                team_details_abp = []
                for team in team_ac:
                    team_detail_ac = TeamDetailAc.objects.get_team_detail_ac_by_team(team=team)
                    if team_detail_ac is not None:
                        team_ac_serializer = TeamAcShortListSerializer(team)
                        team_detail_ac_serializer = TeamDetailAcShortListSerializer(
                            team_detail_ac, many=True
                        )
                        team_details_abp.append({
                            'team_ac': team_ac_serializer.data,
                            'details': team_detail_ac_serializer.data
                        })
                return Response(
                    {
                        'ok': True,
                        'conon_data': team_details_abp
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se encontró el grupo, por favor revise la referencia enviada.'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se envío el Ac.'
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_team_ac_finished(request, team):
    if request.method == 'GET':
        if team:
            team = TeamAc.objects.is_team_ac_finished(team=team)
            if team is not None:
                is_team_finished_work = team.exists()
                return Response(
                    {
                        'ok': True,
                        'conon_data': is_team_finished_work
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se encontró el integrante del equipo.'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se envío el Equipo.'
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
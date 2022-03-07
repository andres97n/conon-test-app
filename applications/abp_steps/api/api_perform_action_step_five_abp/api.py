from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from applications.base.permissions import IsStudent
from applications.abp_steps.models import (PerformActionStepFiveAbp, RatePerformActionStepFiveAbp)
from .serializers import (PerformActionStepFiveAbpListByTeamDetailSerializer,
                          PerformActionStepFiveAbpListSerializer)
from applications.abp_steps.api.api_rate_perform_action_step_five_abp.serializers import \
    RatePerformActionStepFiveAbpListSerializer, RatePerformActionStepFiveAbpByActionListSerializer


@api_view(['GET'])
@permission_classes([IsStudent])
def get_student_actions_by_team_detail(request, team_detail):
    if request.method == 'GET':
        if team_detail:
            student_actions = PerformActionStepFiveAbp.objects. \
                get_student_perform_action_by_team_detail(team_detail)
            if student_actions is not None:
                student_action_serializer = PerformActionStepFiveAbpListByTeamDetailSerializer(
                    student_actions, many=True
                )
                return Response(
                    {
                        'ok': True,
                        'conon_data': student_action_serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se encontró la acción o estrategia del estudiante.'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se envió el Estudiante.'
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
def get_student_actions_and_rates_by_team_and_user(request, team, user):
    if request.method == 'GET':
        if team and user:
            student_actions = PerformActionStepFiveAbp.objects. \
                get_actions_by_team_exclude_user(team, user)
            if student_actions is not None:
                team_actions_and_rates = []
                student_actions_serializer = PerformActionStepFiveAbpListByTeamDetailSerializer(
                    student_actions, many=True
                )
                for student_action in student_actions_serializer.data:
                    rate_student_action = RatePerformActionStepFiveAbp.objects. \
                        get_rate_perform_action_list_by_action(student_action['id'], active=True)
                    if rate_student_action is not None:
                        rate_student_action_serializer = \
                            RatePerformActionStepFiveAbpByActionListSerializer(
                                rate_student_action, many=True
                            )
                        team_actions_and_rates.append({
                            'perform_action': student_action,
                            'rates': rate_student_action_serializer.data
                        })
                    else:
                        team_actions_and_rates.append({
                            'perform_action': student_action,
                            'rates': []
                        })
                return Response(
                    {
                        'ok': True,
                        'conon_data': team_actions_and_rates
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se pudo encontrar las acciones del equipo.'
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
def get_student_actions_and_rates_by_team(request, team):
    if request.method == 'GET':
        if team:
            team_actions = PerformActionStepFiveAbp.objects. \
                get_student_actions_by_team(team)
            if team_actions is not None:
                team_actions_rates = []
                team_actions_serializer = PerformActionStepFiveAbpListSerializer(
                    team_actions, many=True
                )
                for action in team_actions_serializer.data:
                    action_rates = RatePerformActionStepFiveAbp.objects. \
                        get_rate_perform_action_list_by_action(action['id'], active=True)
                    if action_rates is not None:
                        rate_student_action_serializer = RatePerformActionStepFiveAbpListSerializer(
                            action_rates, many=True
                        )
                        team_actions_rates.append({
                            'perform_action': action,
                            'rates': rate_student_action_serializer.data
                        })
                    else:
                        team_actions_rates.append({
                            'perform_action': action,
                            'rates': []
                        })
                return Response(
                    {
                        'ok': True,
                        'conon_data': team_actions_rates
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se pudo encontrar la información del equipo, por favor revise '
                                  'la referencia del equipo.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se envío el grupo.'
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

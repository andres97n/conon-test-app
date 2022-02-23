
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from applications.base.permissions import IsStudent
from applications.abp.models import TeamDetailAbp
from applications.abp_steps.models import StudentIdeaStepTwoAbp, RateStudentIdeaStepTwoAbp
from .serializers import StudentIdeaStepTwoAbpByTeamDetailSerializer, \
    TeamStudentIdeasStepTwoAbpSerializer
from applications.abp_steps.api.api_rate_student_idea_step_two_abp.serializers import \
    RateStudentIdeaByIdeaSerializer


@api_view(['GET'])
@permission_classes([IsStudent])
def get_student_ideas_by_team_detail(request, team_detail):
    if request.method == 'GET':
        if team_detail:
            student_ideas = StudentIdeaStepTwoAbp.objects.\
                get_student_ideas_abp_by_team_detail(team_detail)
            print(team_detail)
            if student_ideas is not None:
                student_idea_serializer = StudentIdeaStepTwoAbpByTeamDetailSerializer(
                    student_ideas, many=True
                )
                return Response(
                    {
                        'ok': True,
                        'conon_data': student_idea_serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'Ocurrió un error en la búsqueda, revise la referencia del usuario.'
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
def get_student_ideas_and_rates_by_team_and_user(request, team, user):
    if request.method == 'GET':
        if team and user:
            team_student_ideas = TeamDetailAbp.objects.\
                get_team_student_idea_step_two_exclude_user(team, user)
            if team_student_ideas is not None:
                team_student_ideas_data = []
                team_student_ideas = TeamStudentIdeasStepTwoAbpSerializer(
                    team_student_ideas, many=True
                )
                for student_idea in team_student_ideas.data:
                    rate_student_idea = RateStudentIdeaStepTwoAbp.objects.\
                        get_rate_student_ideas_by_idea(student_idea['id'])
                    if rate_student_idea is not None:
                        rate_idea_serializer = RateStudentIdeaByIdeaSerializer(
                            rate_student_idea, many=True
                        )
                        team_student_ideas_data.append(
                            {
                                'student_idea': student_idea,
                                'rate_student_ideas': rate_idea_serializer.data
                            }
                        )
                    else:
                        team_student_ideas_data.append(
                            {'student_idea': student_idea, 'rate_student_ideas': []}
                        )
                return Response(
                    {
                        'ok': True,
                        'conon_data': team_student_ideas_data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'Ocurrió un error, no se puedo encontrar ningún registro.'
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

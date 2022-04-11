from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from applications.school.models import Classroom
from applications.abp.models import TeamAbp, TeamDetailAbp
from applications.base.permissions import IsOwnerAndTeacher
from .serializers import StudentsInTeamAbpSerializer, TeamAbpShortListSerializer
from applications.school.api.api_classroom.serializers import StudentsByClassroomForGroupsSerializer
from applications.abp.api.api_team_detail_abp.serializers import TeamDetailAbpShortListSerializer

# TODO: When the team is deleted o changed the state all the teams
#  detail will be change the active field


@api_view(['GET'])
@permission_classes([IsOwnerAndTeacher])
def get_students_by_classroom_for_to_group(request, classroom, abp):
    if request.method == 'GET':
        if classroom and abp:
            students = Classroom.objects.get_students_by_classroom_id(pk=classroom)
            if students:
                students_by_classroom_serializer = \
                    StudentsByClassroomForGroupsSerializer(students, many=True)
                # students_in_abp = []
                detail_students = []
                teams_abp = TeamAbp.objects.get_team_abp_list_by_abp(abp)
                if teams_abp:
                    ids_teams = [team_abp.id for team_abp in teams_abp]
                    print(ids_teams, 'teams')
                    for team_id in ids_teams:
                        ids_users = TeamAbp.objects.get_ids_team_detail_abp_by_team_abp(team_id)
                        if ids_users:
                            for user in ids_users:
                                detail_students.append(user['teamdetailabp__user_id'])
                                """
                                user_result = Student.objects.\
                                    get_student_by_user(user['teamdetailabp__user_id'])
                                if user_result:
                                    # user_result_serializer = StudentListByUserSerializer(user_result)
                                    detail_students.append(user_result)
                                """
                    students_in_abp = [
                        student for student in students_by_classroom_serializer.data
                        if student['user'] not in detail_students
                    ]
                else:
                    students_in_abp = students_by_classroom_serializer.data
                return Response(
                    {
                        'ok': True,
                        'conon_data': students_in_abp
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se encontró el aula.'
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
def get_student_team_abp(request, abp, user):
    if request.method == 'GET':
        if abp and user:
            team_abp_id = TeamAbp.objects.get_team_by_user_and_abp(abp, user)
            if team_abp_id:
                team_abp = TeamAbp.objects.get_detail_by_team_abp(team_abp_id['id'])
                if team_abp:
                    team_serializer = StudentsInTeamAbpSerializer(team_abp, many=True)
                    return Response(
                        {
                            'ok': True,
                            'conon_data': team_serializer.data
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
def get_team_abp_with_students(request, abp):
    if request.method == 'GET':
        if abp:
            team_abp = TeamAbp.objects.get_team_abp_list_by_abp(abp_id=abp)
            if team_abp is not None:
                team_details_abp = []
                for team in team_abp:
                    team_detail_abp = TeamDetailAbp.objects.get_team_detail_by_team(team=team)
                    if team_detail_abp is not None:
                        team_abp_serializer = TeamAbpShortListSerializer(team)
                        team_detail_abp_serializer = TeamDetailAbpShortListSerializer(
                            team_detail_abp, many=True
                        )
                        team_details_abp.append({
                            'team_abp': team_abp_serializer.data,
                            'details': team_detail_abp_serializer.data
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
                    'detail': 'No se envío el Abp.'
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

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from applications.school.models import Classroom
from applications.abp.models import TeamAbp
from applications.base.permissions import IsOwnerAndTeacher
from applications.school.api.api_classroom.serializers import StudentsByClassroomForGroupsSerializer

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
                    'detail': 'No se enviaron los los valores necesarios para procesar.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

    else:
        return Response(
            {
                'ok': False,
                'detail': 'Método no permitido'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

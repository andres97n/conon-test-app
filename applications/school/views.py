from rest_framework import status
from rest_framework.decorators import api_view

from applications.school.models import KnowledgeArea
from applications.users.api.api_teacher.serializers import TeacherByAreaListSerializer


@api_view(['GET'])
def get_teachers_by_area_view(request, pk=None):

    if request.method == 'GET':
        teachers = KnowledgeArea.objects.get_teachers_by_area_id(pk=pk)
        if teachers:
            teacher_serializer = TeacherByAreaListSerializer(teachers, many=True)

            return Response(
                {
                    'ok': True,
                    'conon_data': teacher_serializer.data
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se encontró el Área de Conocimiento.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(
            {
                'ok': False,
                'detail': 'No se permite el presente Método.'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

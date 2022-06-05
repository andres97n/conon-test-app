from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from applications.school.models import KnowledgeArea
from .serializers import KnowledgeAreaTeachersSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_teachers_by_knowledge_area(request, area):
    if request.method == 'GET':
        if area:
            teachers = KnowledgeArea.objects.get_teachers_by_area_id(pk=area)
            if teachers:
                area_serializer = KnowledgeAreaTeachersSerializer(teachers, many=True)
                return Response(
                    {
                        'ok': True,
                        'conon_data': area_serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se encontraron los Docentes del área.'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se envío el aŕea requerida.'
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

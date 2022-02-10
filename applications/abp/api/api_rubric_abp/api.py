from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from applications.abp.models import RubricAbp
from applications.abp.api.api_rubric_abp.serializers import RubricDetailSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_rubric_abp_detail_list_by_abp(request, abp):
    if request.method == 'GET':
        if abp:
            rubric_abp = RubricAbp.objects.get_rubric_detail_by_abp(abp)
            if rubric_abp:
                rubric_serializer = RubricDetailSerializer(rubric_abp, many=True)
                return Response(
                    {
                        'ok': True,
                        'conon_data': rubric_serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se encontró esta Rúbrica.'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se envío el valor necesario para procesar este pedido.'
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



from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from applications.ac.models import RubricAc, RubricDetailAc
from .serializers import RubricAcShortListSerializer
from applications.ac.api.api_rubric_detail_ac.serializers import RubricDetailAcShortListSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_rubric_abp_detail_list_by_abp(request, ac):
    if request.method == 'GET':
        if ac:
            rubric_ac = RubricAc.objects.get_rubric_ac_by_ac(ac=ac)
            if rubric_ac is not None:
                current_rubric_ac = []
                if not rubric_ac:
                    current_rubric_ac.append({
                        "rubric_ac": {},
                        "rubric_detail_ac": []
                    })
                else:
                    rubric_serializer = RubricAcShortListSerializer(rubric_ac.first())
                    rubric_ac_detail = RubricDetailAc.objects.get_rubric_detail_ac_by_rubric_ac(
                        rubric=rubric_serializer.data['id']
                    )
                    if rubric_ac_detail is not None:
                        rubric_ac_detail_serializer = RubricDetailAcShortListSerializer(
                            rubric_ac_detail, many=True
                        )
                        current_rubric_ac.append({
                            "rubric_ac": rubric_serializer.data,
                            "rubric_detail_ac": rubric_ac_detail_serializer.data
                        })
                    else:
                        return Response(
                            {
                                'ok': False,
                                'detail': 'No se encontró los detalles de la Rúbrica.'
                            },
                            status=status.HTTP_404_NOT_FOUND
                        )
                return Response(
                    {
                        'ok': True,
                        'conon_data': current_rubric_ac
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
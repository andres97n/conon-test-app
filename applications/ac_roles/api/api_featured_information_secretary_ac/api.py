
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from applications.ac_roles.models import FeaturedInformationSecretaryAc
from .serializers import FeaturedInformationSecretaryAcListSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_team_featured_information(request, team_detail, member):
    if request.method == 'GET':
        if team_detail and member:
            secretary_information = FeaturedInformationSecretaryAc.objects.\
                get_featured_information_secretary_by_team_detail(team_detail=team_detail,
                                                                  member=member)
            if secretary_information is not None:
                secretary_serializer = FeaturedInformationSecretaryAcListSerializer(
                    secretary_information, many=True
                )
                return Response(
                    {
                        'ok': True,
                        'conon_data': secretary_serializer.data
                    }, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se pudo encontrar la información del Secretario.'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se envio la información necesaria.'
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

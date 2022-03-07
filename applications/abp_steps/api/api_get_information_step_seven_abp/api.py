
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from applications.base.permissions import IsStudent
from applications.abp_steps.models import (GetInformationStepSevenAbp,
                                           InformationReferenceStepSevenAbp)
from .serializers import GetInformationStepSevenAbpListSerializer
from applications.abp_steps.api.api_information_reference_step_seven_abp.serializers import \
    InformationReferenceStepSevenAbpByTeamSerializer


@api_view(['GET'])
@permission_classes([IsStudent])
def get_information_model_with_references(request, team):
    if request.method == 'GET':
        if team:
            get_information_data = GetInformationStepSevenAbp.objects.\
                get_information_model_by_team(team)
            if get_information_data is not None:
                get_information_abp_and_references = []
                if not get_information_data:
                    get_information_abp_and_references = [{
                        "information": {},
                        "references": []
                    }]
                else:
                    get_information_serializer = GetInformationStepSevenAbpListSerializer(
                        get_information_data.first()
                    )
                    information_references = InformationReferenceStepSevenAbp.objects. \
                        get_information_reference_by_team(team, reference_active=True)
                    if information_references is not None:
                        reference_serializer = InformationReferenceStepSevenAbpByTeamSerializer(
                            information_references, many=True
                        )
                        get_information_abp_and_references.append({
                            "information": get_information_serializer.data,
                            "references": reference_serializer.data
                        })
                    else:
                        get_information_abp_and_references.append({
                            "information": get_information_serializer.data,
                            "references": []
                        })
                return Response(
                    {
                        'ok': True,
                        'conon_data': get_information_abp_and_references
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se encontró el problema del equipo, revise la referencia '
                                  'del equipo.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se envió el Equipo.'
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

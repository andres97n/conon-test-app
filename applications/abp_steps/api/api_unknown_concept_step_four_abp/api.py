from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from applications.base.permissions import IsStudent
from applications.abp_steps.models import (UnknownConceptStepFourAbp,
                                           UnknownConceptReferenceStepFourAbp)
from .serializers import SmallUnknownConceptStepFourAbpListSerializer
from applications.abp_steps.api.api_unknown_concept_reference_step_four_abp.serializers import \
    SmallUnknownConceptReferenceStepFourAbpListSerializer


@api_view(['GET'])
@permission_classes([IsStudent])
def get_unknown_concepts_with_references(request, team):
    if request.method == 'GET':
        if team:
            unknown_concepts = UnknownConceptStepFourAbp.objects.\
                get_unknown_concepts_by_team(team)
            if unknown_concepts is not None:
                unknown_concepts_and_references = []
                for concept in unknown_concepts:
                    unknown_concept_serializer = SmallUnknownConceptStepFourAbpListSerializer(concept)
                    concept_references = UnknownConceptReferenceStepFourAbp.objects. \
                        get_unknown_concept_reference_by_concept(concept.id, active=True)
                    if concept_references is not None:
                        unknown_concept_reference_serializer = \
                            SmallUnknownConceptReferenceStepFourAbpListSerializer(
                                concept_references, many=True
                            )
                        unknown_concepts_and_references.append({
                            'unknown_concept': unknown_concept_serializer.data,
                            'references': unknown_concept_reference_serializer.data
                        })
                    else:
                        unknown_concepts_and_references.append({
                            'unknown_concept': unknown_concept_serializer.data,
                            'references': []
                        })
                return Response(
                    {
                        'ok': True,
                        'conon_data': unknown_concepts_and_references
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'Ocurrió un error en la búsqueda, revise la referencia del equipo.'
                    },
                    status=status.HTTP_404_NOT_FOUND
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

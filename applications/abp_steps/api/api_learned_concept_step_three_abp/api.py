from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from applications.base.permissions import IsStudent
from applications.abp_steps.models import (LearnedConceptStepThreeAbp,
                                           LearnedConceptReferenceStepThreeAbp)
from .serializers import SmallLearnedConceptAbpDataSerializer
from applications.abp_steps.api.api_learned_concept_reference_step_three_abp.serializers import \
    SmallLearnedConceptReferenceAbpDataSerializer


@api_view(['GET'])
@permission_classes([IsStudent])
def get_learned_concepts_with_references(request, team):
    if request.method == 'GET':
        if team:
            learned_concepts = LearnedConceptStepThreeAbp.objects. \
                get_learned_concepts_by_team(team)
            if learned_concepts is not None:
                learned_concepts_and_references = []
                for concept in learned_concepts:
                    learned_concept_serializer = SmallLearnedConceptAbpDataSerializer(concept)
                    concept_references = LearnedConceptReferenceStepThreeAbp.objects. \
                        get_learned_concepts_references_by_concept(concept.id)
                    if concept_references is not None:
                        learned_concept_reference_serializer = \
                            SmallLearnedConceptReferenceAbpDataSerializer(
                                concept_references, many=True
                            )
                        learned_concepts_and_references.append({
                            'learned_concept': learned_concept_serializer.data,
                            'references': learned_concept_reference_serializer.data
                        })
                    else:
                        learned_concepts_and_references.append({
                            'learned_concept': learned_concept_serializer.data,
                            'references': []
                        })
                return Response(
                    {
                        'ok': True,
                        'conon_data': learned_concepts_and_references
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


from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from applications.school.models import Glossary, GlossaryDetail
from .serializers import GlossarySerializer
from applications.school.api.api_glossary_detail.serializers import GlossaryDetailSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_glossary_with_detail(request, classroom, active):
    if request.method == 'GET':
        if classroom and active:
            glossary = Glossary.objects.get_glossary_by_classroom(classroom=classroom)
            if glossary is not None:
                educative_terms = {
                    'glossary': {},
                    'details': []
                }
                if glossary:
                    glossary_details = None
                    if active == 1:
                        glossary_details = GlossaryDetail.objects. \
                            get_glossary_detail_by_glossary(glossary.first().id, active=active)
                    else:
                        glossary_details = GlossaryDetail.objects. \
                            get_glossary_detail_by_glossary(glossary.first().id, active=active)
                    glossary_serializer = GlossarySerializer(glossary.first())
                    if glossary_details is not None:
                        details_serializer = GlossaryDetailSerializer(glossary_details, many=True)
                        educative_terms['glossary'] = glossary_serializer.data
                        educative_terms['details'] = details_serializer.data
                    else:
                        educative_terms['glossary'] = glossary_serializer.data
                return Response(
                    {
                        'ok': True,
                        'conon_data': educative_terms
                    }
                )
            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se encontró el correspondiente Glosario.'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se envío el Aula requerida.'
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

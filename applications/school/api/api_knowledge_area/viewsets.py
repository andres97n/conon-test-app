from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework_tracking.mixins import LoggingMixin

from applications.school.api.api_knowledge_area.serializers import KnowledgeAreaSerializer


class KnowledgeAreaViewSet(LoggingMixin, viewsets.ModelViewSet):
    permission_classes = ([IsAdminUser])
    serializer_class = KnowledgeAreaSerializer
    logging_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    sensitive_fields = {'access', 'refresh'}

    # Get Knowledge Area Data
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_area_list()
        return self.get_serializer().Meta.model.objects.get_are_by_id(pk)

    # Get KnowledgeArea List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        conversation_detail_serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': conversation_detail_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Knowledge Area
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        knowledge_area_serializer = self.get_serializer(data=request.data)
        if knowledge_area_serializer.is_valid():
            knowledge_area_serializer.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Área de Conocimiento creada correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'ok': False,
                'detail': knowledge_area_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Knowledge Area
    def update(self, request, pk=None, *args, **kwargs):
        knowledge_area = self.get_queryset(pk)
        if knowledge_area:
            # Send information to serializer referencing the instance
            knowledge_area_serializer = self.get_serializer(knowledge_area, data=request.data)
            if knowledge_area_serializer.is_valid():
                knowledge_area_serializer.save()

                return Response(
                    {
                        'ok': True,
                        'conon_data': knowledge_area_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'ok': False,
                    'detail': knowledge_area_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Área de Conocimiento.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Knowledge Area
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            knowledge_area_serializer = self.get_serializer(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': knowledge_area_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Área de Conocimiento.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Knowledge Area
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        knowledge_area = self.get_queryset(pk)
        if knowledge_area:
            knowledge_area.auth_state = 'I'
            knowledge_area.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Área de Conocimiento eliminada correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Área de Conocimiento.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

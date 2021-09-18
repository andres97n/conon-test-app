from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from applications.school.api_knowledge_area.serializers import KnowledgeAreaSerializer


class KnowledgeAreaViewSet(viewsets.ModelViewSet):
    permission_classes = ([IsAdminUser])
    serializer_class = KnowledgeAreaSerializer

    # Get Knowledge Area Data
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_area_list()
        return self.get_serializer().Meta.model.objects.get_are_by_id(pk)

    # Create Knowledge Area
    def create(self, request, *args, **kwargs):

        # Send information to serializer
        knowledge_area_serializer = self.serializer_class(data=request.data)
        if knowledge_area_serializer.is_valid():
            knowledge_area_serializer.save()

            return Response(
                {
                    'message': 'Período Lectivo creado correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            knowledge_area_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Knowledge Area
    def update(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):

            # Send information to serializer referencing the instance
            knowledge_area_serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if knowledge_area_serializer.is_valid():
                knowledge_area_serializer.save()

                return Response(
                    knowledge_area_serializer.data,
                    status=status.HTTP_200_OK
                )

            return Response(
                knowledge_area_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'error': 'No existe este Período Lectivo.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Knowledge Area
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            knowledge_area_serializer = self.serializer_class(self.get_queryset(pk))

            return Response(
                knowledge_area_serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'error': 'No existe este Período Lectivo.'
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
                    'message': 'Período Lectivo eliminado correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'error': 'No existe este Período Lectivo.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

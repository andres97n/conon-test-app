from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from .serializers import AsignatureSerializer


class AsignatureViewSet(viewsets.ModelViewSet):
    permission_classes = ([IsAdminUser])
    serializer_class = AsignatureSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_asignature_list()
        return self.get_serializer().Meta.model.objects.get_asignature_by_id(pk)


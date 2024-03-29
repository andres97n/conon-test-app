from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import TeamAbpSerializer, StudentsInTeamAbpSerializer
from applications.base.permissions import IsOwnerAndTeacher
from applications.base.paginations import CononPagination


class TeamAbpViewSet(viewsets.ModelViewSet):
    serializer_class = TeamAbpSerializer
    permission_classes = [IsOwnerAndTeacher]
    pagination_class = CononPagination

    # Return Team ABP
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_team_abp_list()
        return self.get_serializer().Meta.model.objects.get_team_abp_by_id(pk)

    # Get Team ABP List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        team_abp_serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': team_abp_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Team ABP
    def create(self, request, *args, **kwargs):
        team_abp_serializer = self.get_serializer(data=request.data)
        if team_abp_serializer.is_valid():
            team_abp_serializer.save()

            return Response(
                {
                    'ok': True,
                    'id': team_abp_serializer.data['id'],
                    'message': 'Grupo creado correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'ok': False,
                'detail': team_abp_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Team ABP
    def update(self, request, pk=None, *args, **kwargs):
        team_abp = self.get_queryset(pk)
        if team_abp:
            # Send information to serializer referencing the instance
            team_abp_serializer = self.get_serializer(team_abp, data=request.data)
            if team_abp_serializer.is_valid():
                team_abp_serializer.save()

                return Response(
                    {
                        'ok': True,
                        'conon_data': team_abp_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'ok': False,
                    'detail': team_abp_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Grupo.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Team ABP
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            team_abp_serializer = self.get_serializer(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': team_abp_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Grupo.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Team ABP
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        team_abp = self.get_queryset(pk)
        if team_abp:
            team_abp.auth_state = 'I'
            team_abp.state = 0
            team_abp.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Grupo eliminado correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Grupo.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Get Users Detail in Team ABP
    @action(detail=True, methods=['GET'], url_path='detail')
    def get_detail_by_team_abp(self, request, pk=None):
        detail_team_abp = self.get_serializer().Meta.model.objects.get_detail_by_team_abp(pk)

        if detail_team_abp:
            team_abp_serializer = StudentsInTeamAbpSerializer(detail_team_abp, many=True)
            return Response(
                {
                    'ok': True,
                    'detail': team_abp_serializer.data
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se encontró este Grupo.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

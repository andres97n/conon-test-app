from rest_framework import viewsets, status
from rest_framework.response import Response

from .serializers import TeamDetailAbpSerializer
from applications.base.permissions import IsOwnerAndTeacher


class TeamDetailAbpViewSet(viewsets.ModelViewSet):
    serializer_class = TeamDetailAbpSerializer
    permission_classes = [IsOwnerAndTeacher]

    # Return Team Detail ABP
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_team_detail_abp_list()
        return self.get_serializer().Meta.model.objects.get_team_detail_abp_by_id(pk)

    # Get Team Detail ABP List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        team_detail_abp_serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': team_detail_abp_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Team Detail ABP
    def create(self, request, *args, **kwargs):
        team_detail_abp_serializer = self.get_serializer(data=request.data)
        if team_detail_abp_serializer.is_valid():
            team_detail_abp_serializer.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Estudiante agregado correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'ok': False,
                'detail': team_detail_abp_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Team Detail ABP
    def update(self, request, pk=None, *args, **kwargs):
        team_detail_abp = self.get_queryset(pk)
        if team_detail_abp:
            # Send information to serializer referencing the instance
            team_detail_abp_serializer = self.get_serializer(team_detail_abp, data=request.data)
            if team_detail_abp_serializer.is_valid():
                team_detail_abp_serializer.save()

                return Response(
                    {
                        'ok': True,
                        'conon_data': team_detail_abp_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'ok': False,
                    'detail': team_detail_abp_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'ok': False,
                'detail': 'No se encontró al estudiante.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Team Detail ABP
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            team_detail_abp_serializer = self.get_serializer(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': team_detail_abp_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este estudiante.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Team Detail ABP
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        team_detail_abp = self.get_queryset(pk)
        if team_detail_abp:
            team_detail_abp.auth_state = 'I'
            team_detail_abp.active = False
            team_detail_abp.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Estudiante eliminado con éxito.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este estudiante.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

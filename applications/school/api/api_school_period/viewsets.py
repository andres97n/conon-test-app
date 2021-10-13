from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework_tracking.mixins import LoggingMixin

from .serializers import SchoolPeriodSerializer


class SchoolPeriodViewSet(LoggingMixin, viewsets.ModelViewSet):
    permission_classes = ([IsAdminUser])
    serializer_class = SchoolPeriodSerializer
    logging_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    sensitive_fields = {'access', 'refresh'}

    # Get School Period Data
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_period_list()
        return self.get_serializer().Meta.model.objects.get_period_by_pk(pk)

    # Get SchoolPeriod List
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

    # Create School Period
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        school_period_serializer = self.get_serializer(data=request.data)
        if school_period_serializer.is_valid():
            school_period_serializer.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Período Lectivo creado correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'ok': False,
                'detail': school_period_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update School Period
    def update(self, request, pk=None, *args, **kwargs):
        school_period = self.get_queryset(pk)
        if school_period:
            # Send information to serializer referencing the instance
            school_period_serializer = self.get_serializer(school_period, data=request.data)
            if school_period_serializer.is_valid():
                school_period_serializer.save()

                return Response(
                    {
                        'ok': True,
                        'conon_data': school_period_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'ok': False,
                    'detail': school_period_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Período Lectivo.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail School Period
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            school_period_serializer = self.get_serializer(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': school_period_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Período Lectivo.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete School Period
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        school_period = self.get_queryset(pk)
        if school_period:
            school_period.state = 0
            school_period.auth_state = 'I'
            school_period.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Período Lectivo eliminado correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe este Período Lectivo.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
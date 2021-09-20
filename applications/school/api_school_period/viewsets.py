from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from .serializers import SchoolPeriodSerializer


class SchoolPeriodViewSet(viewsets.ModelViewSet):
    permission_classes = ([IsAdminUser]),
    serializer_class = SchoolPeriodSerializer

    # Get School Period Data
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_period_list()
        return self.get_serializer().Meta.model.objects.get_period_by_pk(pk)

    # Create School Period
    def create(self, request, *args, **kwargs):

        # Send information to serializer
        school_period_serializer = self.serializer_class(data=request.data)
        if school_period_serializer.is_valid():
            school_period_serializer.save()

            return Response(
                {
                    'message': 'Período Lectivo creado correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            school_period_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update School Period
    def update(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):

            # Send information to serializer referencing the instance
            school_period_serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if school_period_serializer.is_valid():
                school_period_serializer.save()

                return Response(
                    school_period_serializer.data,
                    status=status.HTTP_200_OK
                )

            return Response(
                school_period_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'error': 'No existe este Período Lectivo.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail School Period
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            school_period_serializer = self.serializer_class(self.get_queryset(pk))

            return Response(
                school_period_serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'error': 'No existe este Período Lectivo.'
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

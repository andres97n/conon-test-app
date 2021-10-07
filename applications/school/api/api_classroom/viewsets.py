from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from applications.school.api.api_classroom.serializers import ClassroomSerializer
from applications.base.paginations import CononPagination


class ClassroomViewSet(viewsets.ModelViewSet):
    permission_classes = ([IsAdminUser])
    serializer_class = ClassroomSerializer
    pagination_class = CononPagination

    # Get Classroom Data
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_classroom_list()
        return self.get_serializer().Meta.model.objects.get_classroom_by_id(pk)

    # Create Classroom
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        classroom_serializer = self.serializer_class(data=request.data)
        if classroom_serializer.is_valid():
            classroom_serializer.save()

            return Response(
                {
                    'message': 'Aula creada correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            classroom_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Classroom
    def update(self, request, pk=None, *args, **kwargs):
        classroom = self.get_queryset(pk)
        if classroom:
            # Send information to serializer referencing the instance
            classroom_serializer = self.serializer_class(classroom, data=request.data)
            if classroom_serializer.is_valid():
                classroom_serializer.save()

                return Response(
                    classroom_serializer.data,
                    status=status.HTTP_200_OK
                )

            return Response(
                classroom_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'error': 'No existe esta Aula.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Classroom Data
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            classroom_serializer = self.serializer_class(self.get_queryset(pk))

            return Response(
                classroom_serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'error': 'No existe esta Aula.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Classroom
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        classroom = self.get_queryset(pk)
        if classroom:
            classroom.auth_state = 'I'
            classroom.save()

            return Response(
                {
                    'message': 'Aula eliminada correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'error': 'No existe esta Aula.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )


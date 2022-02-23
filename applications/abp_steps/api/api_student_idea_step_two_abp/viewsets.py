from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_tracking.mixins import LoggingMixin
from django_filters.rest_framework import DjangoFilterBackend


from applications.base.permissions import IsStudent
from applications.base.paginations import CononPagination
from .serializers import StudentIdeaStepTwoAbpSerializer


class StudentIdeaStepTwoAbpViewSet(LoggingMixin, viewsets.GenericViewSet):
    serializer_class = StudentIdeaStepTwoAbpSerializer
    permission_classes = ([IsStudent])
    pagination_class = CononPagination
    logging_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    sensitive_fields = {'access', 'refresh'}
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['team_detail_abp', 'active']

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_student_idea_abp_list()
        return self.get_serializer().Meta.model.objects.get_student_idea_abp_by_pk(pk)

    # Get Student Idea ABP List
    def list(self, request, *args, **kwargs):
        student_idea_queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(student_idea_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        student_idea_serializer = self.get_serializer(student_idea_queryset, many=True)
        return Response(
            {
                'ok': True,
                'conon_data': student_idea_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Student Idea ABP
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        is_many = True if isinstance(request.data, list) else False
        student_idea_serializer = self.get_serializer(data=request.data, many=is_many)
        if student_idea_serializer.is_valid():
            student_idea_serializer.save()
            return Response(
                {
                    'ok': True,
                    'student_idea':
                        student_idea_serializer.data if isinstance(student_idea_serializer.data, list)
                        else student_idea_serializer.data['id'],
                    'message':
                        'Ideas creadas correctamente' if isinstance(student_idea_serializer.data, list)
                        else 'Idea creada correctamente'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'ok': False,
                'detail': student_idea_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Student Idea ABP
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        student_idea_abp = self.get_queryset(pk)
        if student_idea_abp:
            student_idea_abp.active = False
            student_idea_abp.auth_state = 'I'
            student_idea_abp.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Idea eliminada correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No se encontró la Idea enviada.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Block Student Idea ABP
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_student_idea_abp(self, request, pk=None):
        student_idea_abp = self.get_queryset(pk)
        if student_idea_abp:
            student_idea_abp.active = False
            student_idea_abp.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Idea bloqueada correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No se encontró la Idea enviada.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

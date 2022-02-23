
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from applications.base.permissions import IsStudent
from applications.base.paginations import CononPagination
from.serializers import RateStudentIdeaStepTwoAbpSerializer, RateStudentIdeaListSerializer


class RateStudentIdeaStepTwoAbpViewSet(viewsets.GenericViewSet):
    permission_classes = ([IsStudent])
    serializer_class = RateStudentIdeaStepTwoAbpSerializer
    list_serializer_class = RateStudentIdeaListSerializer
    pagination_class = CononPagination
    queryset = None
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student_idea_step_two_abp', 'active']

    def get_object(self, pk=None):
        return get_object_or_404(self.serializer_class.Meta.model, id=pk)

    def get_queryset(self):
        return self.list_serializer_class().Meta.model.objects.\
            get_rate_student_idea_abp_list()

    # Get Rate Student Idea List
    def list(self, request):
        rate_student_idea_queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(rate_student_idea_queryset)
        if page is not None:
            serializer = self.list_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        rate_student_idea_serializer = self.list_serializer_class(
            rate_student_idea_queryset, many=True
        )

        return Response(
            {
                'ok': True,
                'conon_data': rate_student_idea_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Update Rating ABP
    def update(self, request, pk=None):
        rate_abp = self.get_object(pk)
        # Send information to serializer referencing the instance
        rate_student_idea_serializer = self.serializer_class(rate_abp, data=request.data)
        if rate_student_idea_serializer.is_valid():
            rate_student_idea_serializer.save()
            return Response(
                {
                    'ok': True,
                    'conon_data': rate_student_idea_serializer.data,
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'ok': False,
                'detail': rate_student_idea_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Rate Student Idea Abp
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        rate_student_idea_abp = self.get_object(pk)
        rate_student_idea_abp.active = False
        rate_student_idea_abp.auth_state = 'I'
        rate_student_idea_abp.save()

        return Response(
            {
                'ok': True,
                'message': 'Calificación eliminada correctamente.'
            },
            status=status.HTTP_200_OK
        )

    # Block Student Idea ABP
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_student_idea_abp(self, request, pk=None):
        rate_student_idea_abp = self.get_object(pk)
        rate_student_idea_abp.active = False
        rate_student_idea_abp.save()

        return Response(
            {
                'ok': True,
                'message': 'Calificación bloqueada correctamente.'
            },
            status=status.HTTP_200_OK
        )

"""
    # Create Rate Student Idea
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        is_many = True if isinstance(request.data, list) else False
        rate_student_idea_serializer = self.get_serializer(data=request.data, many=is_many)
        if rate_student_idea_serializer.is_valid():
            rate_student_idea_serializer.save()

            return Response(
                {
                    'ok': True,
                    'rate_student_idea':
                        rate_student_idea_serializer.data
                        if len(rate_student_idea_serializer.data) > 1
                        else rate_student_idea_serializer.data['id'],
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'ok': False,
                'detail': rate_student_idea_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )
"""
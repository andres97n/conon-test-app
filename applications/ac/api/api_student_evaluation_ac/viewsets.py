
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import StudentEvaluationAcSerializer, StudentEvaluationAcListSerializer
from applications.base.permissions import IsTeacher
from applications.base.paginations import CononPagination


class StudentEvaluationAcViewSet(viewsets.GenericViewSet):
    serializer_class = StudentEvaluationAcSerializer
    list_serializer_class = StudentEvaluationAcListSerializer
    permission_classes = [IsTeacher]
    pagination_class = CononPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rubric_ac', 'team_detail_ac', 'state']

    # Return Single Object
    def get_object(self, pk=None):
        return get_object_or_404(
            self.serializer_class.Meta.model.objects.
            get_student_evaluation_ac_active_queryset(),
            id=pk
        )

    # Return Student Evaluation Ac List
    def get_queryset(self):
        return self.serializer_class().Meta.model.objects.get_student_evaluation_ac_list()

    # Get Student Evaluation Ac List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.list_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        student_evaluation_ac_serializer = self.list_serializer_class(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': student_evaluation_ac_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Student Evaluation Ac
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        student_evaluation_ac_serializer = self.get_serializer(data=request.data)
        if student_evaluation_ac_serializer.is_valid():
            student_evaluation_ac_serializer.save()
            return Response(
                {
                    'ok': True,
                    'id': student_evaluation_ac_serializer.data['id'],
                    'message': 'Calificación generada correctamente.'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'ok': False,
                'detail': student_evaluation_ac_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Evaluation AC
    def update(self, request, pk=None, *args, **kwargs):
        evaluation_ac = self.get_object(pk)
        # Send information to serializer referencing the instance
        evaluation_ac_serializer = self.get_serializer(evaluation_ac, data=request.data)
        if evaluation_ac_serializer.is_valid():
            evaluation_ac_serializer.save()

            return Response(
                {
                    'ok': True,
                    'conon_data': evaluation_ac_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': evaluation_ac_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Block Student Evaluation Ac
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_student_evaluation_ac(self, request, pk=None):
        student_evaluation_ac = self.get_object(pk)
        student_evaluation_ac.state = 0
        student_evaluation_ac.save()

        return Response(
            {
                'ok': True,
                'message': 'Nota Final bloqueada correctamente.'
            },
            status=status.HTTP_200_OK
        )

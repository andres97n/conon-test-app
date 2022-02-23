from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from applications.base.paginations import CononPagination
from applications.base.permissions import IsStudent
from .serializers import QuestionStepOneAbpSerializer


# TODO: Reformar este viewset a uno que no sea model viewset
class QuestionStepOneAbpViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionStepOneAbpSerializer
    permission_classes = [IsStudent]
    pagination_class = CononPagination

    # Get Question ABP Data
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_question_abp_list()
        return self.get_serializer().Meta.model.objects.get_question_abp_by_pk(pk)

    # Get Question ABP List
    def list(self, request, *args, **kwargs):
        question_abp_queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(question_abp_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        question_abp_serializer = self.get_serializer(question_abp_queryset, many=True)
        return Response(
            {
                'ok': True,
                'conon_data': question_abp_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Question ABP
    def create(self, request, *args, **kwargs):
        # Send information to serializer
        question_abp_serializer = self.get_serializer(data=request.data)
        if question_abp_serializer.is_valid():
            question_abp_serializer.save()
            return Response(
                {
                    'ok': True,
                    'id': question_abp_serializer.data['id'],
                    'message': 'Pregunta generada correctamente.'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'ok': False,
                'detail': question_abp_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Question ABP
    def update(self, request, pk=None, *args, **kwargs):
        question_abp = self.get_queryset(pk)
        if question_abp:
            # Send information to serializer referencing the instance
            question_abp_serializer = self.get_serializer(question_abp, data=request.data)
            if question_abp_serializer.is_valid():
                question_abp_serializer.save()
                return Response(
                    {
                        'ok': True,
                        'conon_data': question_abp_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {
                    'ok': False,
                    'detail': question_abp_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {
                'ok': False,
                'detail': 'No se encontró el Grupo enviado.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Question ABP Data
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            question_abp_serializer = self.serializer_class(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': question_abp_serializer.data,
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'ok': False,
                'detail': 'No se encontró el Grupo enviado.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Question ABP
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        question_abp = self.get_queryset(pk)
        if question_abp:
            question_abp.active = False
            question_abp.auth_state = 'I'
            question_abp.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Pregunta eliminada correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No se encontró el Grupo enviado.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Block Question ABP
    @action(detail=True, methods=['DELETE'], url_path='block')
    def block_interaction_abp(self, request, pk=None):
        question_abp = self.get_queryset(pk)
        if question_abp:
            question_abp.active = False
            question_abp.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Pregunta bloqueada correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No se encontró el Grupo enviado.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Create Many Questions ABP
    @action(detail=False, methods=(['POST']), url_path='create-many')
    def create_many_question_abp(self, request):
        is_many = True if isinstance(request.data, list) else False
        question_abp_serializer = self.get_serializer(data=request.data, many=is_many)
        if question_abp_serializer.is_valid():
            question_abp_serializer.save()
            return Response(
                {
                    'ok': True,
                    'questions': question_abp_serializer.data,
                    'message': 'Preguntas generadas correctamente.'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'ok': False,
                'detail': question_abp_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )
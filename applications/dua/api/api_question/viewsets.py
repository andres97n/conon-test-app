from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from .serializers import QuestionSerializer
from applications.base.permissions import IsOwnerAndTeacher


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    permission_classes = ([IsOwnerAndTeacher])

    # Return Question Data
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_question_list()
        return self.get_serializer().Meta.model.objects.get_question_by_id(pk)

    # Get Question List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        question_serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': question_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Question
    def create(self, request, *args, **kwargs):
        question_serializer = self.get_serializer(data=request.data)
        if question_serializer.is_valid():
            question_serializer.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Pregunta creada correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'ok': False,
                'detail': question_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Question
    def update(self, request, pk=None, *args, **kwargs):
        question = self.get_queryset(pk)
        if question:
            # Send information to serializer referencing the instance
            question_serializer = self.get_serializer(question, data=request.data)
            if question_serializer.is_valid():
                question_serializer.save()

                return Response(
                    {
                        'ok': True,
                        'conon_data': question_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'ok': False,
                    'detail': question_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Pregunta.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Question
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            question_serializer = self.get_serializer(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': question_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Pregunta.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Question
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        question = self.get_queryset(pk)
        if question:
            question.active = False
            question.auth_state = 'I'
            question.save()

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
                'detail': 'No existe esta Pregunta.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

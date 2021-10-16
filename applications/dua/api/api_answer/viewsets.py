from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from .serializers import AnswerSerializer
from applications.base.permissions import IsOwnerAndStudent


class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    permission_classes = ([IsOwnerAndStudent])

    # Return Answer
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_answer_list()
        return self.get_serializer().Meta.model.objects.get_answer_by_id(pk)

    # Get Answer List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        answer_serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': answer_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Answer
    def create(self, request, *args, **kwargs):
        answer_serializer = self.get_serializer(data=request.data)
        if answer_serializer.is_valid():
            answer_serializer.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Respuesta creada correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'ok': False,
                'detail': answer_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Answer
    def update(self, request, pk=None, *args, **kwargs):
        answer = self.get_queryset(pk)
        if answer:
            # Send information to serializer referencing the instance
            answer_serializer = self.get_serializer(answer, data=request.data)
            if answer_serializer.is_valid():
                answer_serializer.save()

                return Response(
                    {
                        'ok': True,
                        'conon_data': answer_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'ok': False,
                    'detail': answer_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Respuesta.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Answer
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            answer_serializer = self.get_serializer(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': answer_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Respuesta.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Answer
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        answer = self.get_queryset(pk)
        if answer:
            answer.auth_state = 'I'
            answer.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Respuesta eliminada correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Respuesta.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

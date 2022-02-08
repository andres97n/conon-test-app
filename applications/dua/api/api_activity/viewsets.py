from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import ActivitySerializer, ActivityDetailSerializer
from applications.base.permissions import IsOwnerAndTeacher


class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    permission_classes = ([IsOwnerAndTeacher])
    logging_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    sensitive_fields = {'access', 'refresh'}

    # Return Activity Data
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.get_activity_list()
        return self.get_serializer().Meta.model.objects.get_activity_by_id(pk)

    # Get DUA List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        activity_serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                'ok': True,
                'conon_data': activity_serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Create Activity
    def create(self, request, *args, **kwargs):
        activity_serializer = self.get_serializer(data=request.data)
        if activity_serializer.is_valid():
            activity_serializer.save()

            return Response(
                {
                    'ok': True,
                    'id': activity_serializer.data['id'],
                    'message': 'Actividad creada correctamente.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'ok': False,
                'detail': activity_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Activity
    def update(self, request, pk=None, *args, **kwargs):
        activity = self.get_queryset(pk)
        if activity:
            # Send information to serializer referencing the instance
            activity_serializer = self.get_serializer(activity, data=request.data)
            if activity_serializer.is_valid():
                activity_serializer.save()

                return Response(
                    {
                        'ok': True,
                        'conon_data': activity_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'ok': False,
                    'detail': activity_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Actividad.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Detail Activity
    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            activity_serializer = self.get_serializer(self.get_queryset(pk))

            return Response(
                {
                    'ok': True,
                    'conon_data': activity_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Actividad.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Activity
    def destroy(self, request, pk=None, *args, **kwargs):
        # Get instance
        activity = self.get_queryset(pk)
        if activity:
            activity.auth_state = 'I'
            activity.save()

            return Response(
                {
                    'ok': True,
                    'message': 'Actividad eliminado correctamente.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'ok': False,
                'detail': 'No existe esta Actividad.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # TODO: Probar url
    @action(detail=True, methods=['GET'], url_path='questions')
    def get_activity_detail(self, pk=None):
        if pk:
            questions = self.get_serializer().Meta.model.objects.get_questions_by_activity(pk)
            if questions:
                question_serializer = ActivityDetailSerializer(questions, many=True)
                return Response(
                    {
                        'ok': False,
                        'conon_data': question_serializer.data
                    },
                    status=status.HTTP_200_OK
                )

            else:
                return Response(
                    {
                        'ok': False,
                        'detail': 'No se encontraron preguntas sobre esta Actividad.'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

        else:
            return Response(
                {
                    'ok': False,
                    'detail': 'No se encontró la Actividad.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

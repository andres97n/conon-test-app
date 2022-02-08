from rest_framework import serializers

from applications.topic.models import Topic
from applications.users.models import Student, User
from applications.school.models import Classroom, Asignature
# from applications.users.api.api_student.serializers import StudentShortListSerializer


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        exclude = [
            'updated_at',
            'auth_state'
        ]

    """
    def get_students(self, students=None):
        student_serializer = StudentListManyToMany(students, many=True)
        return student_serializer.data
    """

    def get_user_name(self, pk=None):
        return User.objects.get_user_detail_data(pk=pk)

    def validate_type(self, value):
        if value == 0 or value > 3:
            raise serializers.ValidationError(
                detail='Error, no existe esta Metodología.'
            )
        return value

    # Validate Students
    def validate_students(self, value):
        if value:
            for student in value:
                if not Student.objects.is_active(student.id):
                    raise serializers.ValidationError(
                        {
                            'students': 'Error, el siguiente Estudiante no existe.'
                        }
                    )
        return value

    def validate(self, attrs):
        if attrs['start_at'] >= attrs['end_at']:
            raise serializers.ValidationError(
                {
                    'start_at': 'Error: la Fecha de Inicio no puede ser la misma o mayor '
                                'que la Fecha Final del Tema de Estudio.'
                }
            )
        return attrs

    # Create a Topic
    def create(self, validated_data):
        if not User.objects.type_user_exists(validated_data['owner'].id, 1):
            raise serializers.ValidationError(
                {
                    'owner': 'Error, el siguiente Usuario no existe.'
                }
            )
        if not Classroom.objects.exists_classroom(validated_data['classroom'].id):
            raise serializers.ValidationError(
                {
                    'classroom': 'Error, no se pudo encontrar el Aula.'
                }
            )
        if not Asignature.objects.exists_asignature(validated_data['asignature'].id):
            raise serializers.ValidationError(
                {
                    'asignature': 'Error, no se pudo encontrar la Asignatura.'
                }
            )
        topic = Topic(**validated_data)
        topic.save()
        return topic

    # Update Topic
    def update(self, instance, validated_data):
        if instance.owner != validated_data['owner']:
            raise serializers.ValidationError(
                {
                    'owner': 'Error, no se puede cambiar el Usuario.'
                }
            )
        if instance.classroom != validated_data['classroom']:
            raise serializers.ValidationError(
                {
                    'classroom': 'Error, no se puede cambiar el Aula.'
                }
            )
        if instance.asignature != validated_data['asignature']:
            raise serializers.ValidationError(
                {
                    'asignature': 'Error, no se puede cambiar la Asignatura.'
                }
            )
        update_topic = super().update(instance, validated_data)
        update_topic.save()
        return update_topic

    def to_representation(self, instance):
        """
        name = self.get_user_name(pk=instance.owner.id).person
        if name is None:
            name = 'No existe'
        else:
            name = self.get_user_name(pk=instance.owner.id).__str__()
        """

        return {
            'id': instance.id,
            'title': instance.title,
            'description': instance.description,
            'objective': instance.objective,
            'type': instance.type,
            'start_at': instance.start_at,
            'end_at': instance.end_at,
            'owner': {
                'id': instance.owner.id,
                'name': instance.owner.__str__(),
            },
            'classroom': {
                'id': instance.classroom.id,
                'name': instance.classroom.__str__(),
            },
            'asignature': {
                'id': instance.asignature.id,
                'name': instance.asignature.__str__(),
            },
            'active': instance.active,
            'observations': instance.observations,
            'created_at': instance.created_at
            # 'students': self.get_students(instance.students),
        }


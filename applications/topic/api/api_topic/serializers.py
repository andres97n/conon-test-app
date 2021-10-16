from rest_framework import serializers

from applications.topic.models import Topic
from applications.users.models import Student, User
from applications.users.api.api_student.serializers import StudentListManyToMany


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        exclude = [
            'updated_at',
            'auth_state'
        ]

    def get_students(self, students=None):
        student_serializer = StudentListManyToMany(students, many=True)
        return student_serializer.data

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
                        detail='Error, el siguiente Estudiante no existe.'
                    )
        return value

    def validate(self, attrs):
        if attrs['start_at'] >= attrs['end_at']:
            raise serializers.ValidationError(
                detail='Error: la Fecha de Inicio no puede ser la misma o mayor que la Fecha '
                       'Final del Tema de Estudio.'
            )
        return attrs

    # Create a Topic
    def create(self, validated_data):
        if not User.objects.user_exists(validated_data['owner'].id):
            raise serializers.ValidationError(
                detail='Error, el siguiente Usuario no existe.'
            )
        topic = Topic(**validated_data)
        topic.save()
        return topic

    # Update Topic
    def update(self, instance, validated_data):
        if instance.owner != validated_data['owner']:
            raise serializers.ValidationError(
                detail='Error, no se puede cambiar el Usuario.'
            )
        update_topic = super().update(instance, validated_data)
        update_topic.save()
        return update_topic

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'title': instance.title,
            'description': instance.description,
            'objective': instance.objective,
            'type': instance.type,
            'start_at': instance.start_at,
            'end_at': instance.end_at,
            'active': instance.active,
            'observations': instance.observations,
            'owner': {
                'id': instance.owner.id,
                'name': instance.owner.__str__()
            },
            'students': self.get_students(instance.students),
            'created_at': instance.created_at
        }

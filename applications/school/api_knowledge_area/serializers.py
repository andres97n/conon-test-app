from rest_framework import serializers

from applications.school.models import KnowledgeArea
from applications.users.models import Teacher
from applications.users.api.api_teacher.serializers import TeacherByAreaListSerializer

# TODO: Investigar la manera de retornar los datos de los
#   profesores dentro de la lista del área


class KnowledgeAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeArea
        exclude = [
            'created_at',
            'updated_at',
            'auth_state'
        ]

    # Validate Teachers
    def validate_teachers(self, value):
        if value:
            for teacher in value:
                if not Teacher.objects.is_active(teacher.id):
                    raise serializers.ValidationError(f'Error, este Docente [{teacher}] no existe.')
        return value

    def validate(self, attrs):
        if attrs['coordinator'].id == attrs['sub_coordinator'].id:
            raise serializers.ValidationError('Error, el Coordinador no puede ser el mismo que el Sub coordinador.')

        return attrs

    def get_teachers(self, teachers=None):
        teacher_serializer = TeacherByAreaListSerializer(teachers, many=True)
        return teacher_serializer.data

    # Get Knowledge Area Data
    def to_representation(self, instance):

        return dict(
            id=instance.id,
            name=instance.name,
            coordinator=dict(
                name=instance.coordinator.person.name,
                last_name=instance.coordinator.person.last_name
            ),
            sub_coordinator=dict(
                name=instance.sub_coordinator.person.name,
                last_name=instance.sub_coordinator.person.last_name
            ),
            objective=instance.objective,
            observations=instance.observations,
            teachers=self.get_teachers(instance.teachers),
        )

    # Create a Knowledge Area
    def create(self, validated_data):
        if not KnowledgeArea.objects.is_name_exists(validated_data['name']):
            raise serializers.ValidationError('Error, esta Área de Conocimiento ya existe.')
        knowledge_area = KnowledgeArea(**validated_data)
        knowledge_area.save()
        return knowledge_area

    # Update Knowledge Area
    def update(self, instance, validated_data):
        if instance.name != validated_data['name']:
            if not KnowledgeArea.objects.is_name_exists(validated_data['name']):
                raise serializers.ValidationError('Error, esta Área de Conocimiento ya existe.')
        update_knowledge_area = super().update(instance, validated_data)
        update_knowledge_area.save()
        return update_knowledge_area

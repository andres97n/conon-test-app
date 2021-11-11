from rest_framework import serializers

from applications.school.models import KnowledgeArea
from applications.users.models import Teacher
from applications.users.api.api_teacher.serializers import TeacherByAreaListSerializer


class KnowledgeAreaSerializer(serializers.ModelSerializer):
    """
    teachers_data = serializers.HyperlinkedRelatedField(
        view_name='teachers-by-area',
        read_only=True,
        lookup_field='pk',
        lookup_url_kwarg='pk'
    )
    """

    class Meta:
        model = KnowledgeArea
        fields = [
            'id',
            'name',
            'coordinator',
            'sub_coordinator',
            'objective',
            'observations',
            'created_at',
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

    '''
    def get_teachers(self, teachers=None):
        teacher_serializer = TeacherByAreaListSerializer(teachers, many=True)
        return teacher_serializer.data'''

    # Create a Knowledge Area
    def create(self, validated_data):
        if KnowledgeArea.objects.is_name_exists(validated_data['name']):
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

    # Get Knowledge Area Data
    def to_representation(self, instance):

        # data = super().to_representation(instance)

        return {
            'id': instance.id,
            'name': instance.name,
            'coordinator': {
                'id': instance.coordinator.person.id,
                'name': instance.coordinator.person.full_name()
            },
            'sub_coordinator': {
                'id': instance.sub_coordinator.person.id,
                'name': instance.sub_coordinator.person.full_name()
            },
            'objective': instance.objective,
            'observations': instance.observations,
            # 'teachers': data['teachers'],
            'created_at': instance.created_at
        }


class KnowledgeAreaByAsignature(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeArea
        fields = [
            'id',
            'name'
        ]

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name
        }

from rest_framework import serializers

from applications.school.models import AsignatureClassroom, Classroom, Asignature, \
                                    Teacher, KnowledgeArea


class AsignatureClassroomSerializer(serializers.ModelSerializer):
        class Meta:
            model = AsignatureClassroom
            exclude = [
                'created_at',
                'updated_at',
                'auth_state'
            ]

        # Validate if the teacher and asignature bellows to the same knowledge area
        def validate(self, attrs):
            asignature_knowledge_area_id = Asignature.objects.get_asignature_by_id(attrs['asignature'].id)
            if asignature_knowledge_area_id is None:
                raise serializers.ValidationError(
                    {
                        'asignature': 'Error, no se encontró la Asignatura ingresada.'
                    }
                )
            print(KnowledgeArea.objects.get_teachers_ids_by_area(asignature_knowledge_area_id.knowledge_area.id))
            area = KnowledgeArea.objects.get_teachers_ids_by_area(asignature_knowledge_area_id.knowledge_area.id)
            # if area.teachers.count() != 0:
            is_teacher_valid = False
            print(attrs['teacher'].id)
            print(area)
            for teacher in area:
                if teacher['teachers__id'] == attrs['teacher'].id:
                    is_teacher_valid = True
            if not is_teacher_valid:
                raise serializers.ValidationError(
                    {
                        'teacher': 'Error, el Docente no fue asignado a la misma área de conocimiento '
                                   'que la asignatura.'
                    }
                )
            if AsignatureClassroom.objects.get_asignature_classroom_by_classroom_teacher_and_asignature(
                asignature=attrs['asignature'].id,
                teacher=attrs['teacher'].id,
                classroom=attrs['classroom'].id
            ) is not None:
                raise serializers.ValidationError(
                    {
                        'teacher': 'Error, ya existe una asignación para estos valores en el presente '
                                   'Período Lectivo.'
                    }
                )
            return attrs

        # Create a AsignatureClassroom Data
        def create(self, validated_data):
            if not Classroom.objects.is_active(validated_data['classroom'].id):
                raise serializers.ValidationError(
                    {
                        'classroom': 'Error, Aula inexistente o inactiva.'
                    }
                )
            if not Asignature.objects.is_active(validated_data['asignature'].id):
                raise serializers.ValidationError(
                    {
                        'asignature': 'Error, esta Asignatura no existe.'
                    }
                )
            if not Teacher.objects.is_active(validated_data['teacher'].id):
                raise serializers.ValidationError(
                    {
                        'teacher': 'Error, este Docente no existe.'
                    }
                )
            asignature_classroom = AsignatureClassroom(**validated_data)
            asignature_classroom.save()
            return asignature_classroom

        # Update AsignatureClassroom
        def update(self, instance, validated_data):
            if instance.classroom != validated_data['classroom']:
                if not Classroom.objects.is_active(validated_data['classroom'].id):
                    raise serializers.ValidationError(
                        {
                            'classroom': 'Error, Aula inexistente o inactiva.'
                        }
                    )
            if instance.asignature != validated_data['asignature']:
                raise serializers.ValidationError(
                    {
                        'asignature': 'Error, una vez ingresada la Asignatura no se puede cambiar el mismo.'
                    }
                )
            if instance.teacher != validated_data['teacher']:
                raise serializers.ValidationError(
                    {
                        'teacher': 'Error, una vez ingresado el Docente no se puede cambiar el mismo.'
                    }
                )
            update_asignature_classroom = super().update(instance, validated_data)
            update_asignature_classroom.save()
            return update_asignature_classroom

        # Return Data
        def to_representation(self, instance):
            return {
                'id': instance.id,
                'classroom': {
                    'id': instance.classroom.id,
                    'name': instance.classroom.name,
                },
                'asignature': {
                    'id': instance.asignature.id,
                    'name': instance.asignature.name,
                    'type': instance.asignature.get_area_type()
                },
                'teacher': {
                    'id': instance.teacher.id,
                    'name': instance.teacher.__str__(),
                },
                'observations': instance.observations
            }


class AsignatureClassroomByAsignature(serializers.ModelSerializer):
    class Meta:
        model = AsignatureClassroom
        include = [
            'id',
            'classroom',
            'teacher',
            'created_at'
        ]

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'classroom': {
                'id': instance.classroom.id,
                'name': instance.classroom.name,
            },
            'teacher': {
                'id': instance.teacher.id,
                'name': instance.teacher.__str__()
            },
            'created_at': instance.created_at
        }

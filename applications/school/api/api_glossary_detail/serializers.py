from rest_framework import serializers

from applications.school.models import GlossaryDetail, Glossary


class GlossaryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlossaryDetail
        exclude = [
            'auth_state'
        ]

    # Create a Term
    def create(self, validated_data):
        if not Glossary.objects.glosary_exists(validated_data['glossary'].id):
            raise serializers.ValidationError(
                {
                    'glossary': 'Error, el Glosario enviado no existe.'
                }
            )
        if GlossaryDetail.objects.title_exists(
                validated_data['glossary'].id, validated_data['title']
        ):
            raise serializers.ValidationError(
                {
                    'title': 'Error, este Glosario ya contiene este título.'
                }
            )
        glossary_detail = GlossaryDetail(**validated_data)
        glossary_detail.save()
        return glossary_detail

    # Update Glosary Detail
    def update(self, instance, validated_data):
        if instance.glossary != validated_data['glossary']:
            raise serializers.ValidationError(
                {
                    'glossary': 'Error, no se puede cambiar la relación de este registro; '
                }
            )
        if instance.title != validated_data['title']:
            if GlossaryDetail.objects.title_exists(instance.glossary.id, instance.title):
                raise serializers.ValidationError(
                    {
                        'title': 'Error, este Glosario ya contiene este título.'
                    }
                )
        update_glossary_detail = super().update(instance, validated_data)
        update_glossary_detail.save()
        return update_glossary_detail

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'title': instance.title,
            'description': instance.description,
            'image': instance.image,
            'url': instance.url,
            'state': instance.state,
            'observation': instance.observation,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at
        }

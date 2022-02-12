from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import OpinionStepOneAbp, InteractionStepOneAbp


@receiver(post_save, sender=OpinionStepOneAbp)
def post_save_opinion_step_one_abp(sender, instance, created, *args, **kwargs):
    print(instance)
    print(created)
    if created:
        new_interaction = InteractionStepOneAbp()
        new_interaction.opinion_step_one_abp = instance
        new_interaction.user = instance.team_detail_abp.user
        new_interaction.opinion_interaction = 0
        new_interaction.active = True
        new_interaction.save()

        
# post_save.connect(post_save_opinion_step_one_abp, sender=OpinionStepOneAbp)

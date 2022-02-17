from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import OpinionStepOneAbp, InteractionStepOneAbp
from applications.abp.models import TeamAbp
from applications.users.models import User


@receiver(post_save, sender=OpinionStepOneAbp)
def post_save_opinion_step_one_abp(sender, instance, created, *args, **kwargs):
    if created:
        team_detail_ids = TeamAbp.objects.get_ids_team_detail_abp_by_team_abp_exclude_active(
            instance.team_detail_abp.team_abp.id
        )
        valid_students = [
            student for student in team_detail_ids
            if student['teamdetailabp__user'] != instance.team_detail_abp.user.id
        ]
        if team_detail_ids:
            for team_detail in valid_students:
                current_user = User.objects.get_user_detail_data(
                    team_detail['teamdetailabp__user']
                )
                if current_user is not None:
                    new_interaction = InteractionStepOneAbp()
                    new_interaction.opinion_step_one_abp = instance
                    new_interaction.user = current_user
                    new_interaction.opinion_interaction = 0
                    new_interaction.active = True
                    new_interaction.save()

        
# post_save.connect(post_save_opinion_step_one_abp, sender=OpinionStepOneAbp)

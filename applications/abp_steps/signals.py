from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import (OpinionStepOneAbp, InteractionStepOneAbp,
                     StudentIdeaStepTwoAbp, RateStudentIdeaStepTwoAbp,
                     PerformActionStepFiveAbp, RatePerformActionStepFiveAbp)
from applications.abp.models import TeamAbp, TeamDetailAbp
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
        if team_detail_ids is not None:
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
    else:
        if not instance.active and instance.auth_state == 'A':
            interactions_abp = InteractionStepOneAbp.objects.\
                get_interaction_by_opinion(instance.id)
            if interactions_abp is not None:
                for interaction in interactions_abp:
                    interaction.active = False
                    interaction.save()


def post_save_student_idea_step_two_abp(sender, instance, created, *args, **kwargs):
    if created:
        team_details = TeamDetailAbp.objects.get_team_detail_list_by_team_exclude_user(
            instance.team_detail_abp.team_abp.id, instance.team_detail_abp.user.id
        )
        if team_details is not None:
            for student in team_details:
                new_rate_student_idea = RateStudentIdeaStepTwoAbp()
                new_rate_student_idea.student_idea_step_two_abp = instance
                new_rate_student_idea.user = student.user
                new_rate_student_idea.rate_student_idea = 0
                new_rate_student_idea.active = True
                new_rate_student_idea.save()
    else:
        if not instance.active and instance.auth_state == 'A':
            rates_student_idea = RateStudentIdeaStepTwoAbp.objects.\
                get_any_rate_student_ideas_by_idea(instance.id)
            if rates_student_idea is not None:
                for rating in rates_student_idea:
                    rating.active = False
                    rating.save()


def post_save_perform_action_step_five_abp(sender, instance, created, *args, **kwargs):
    if created:
        team_details = TeamDetailAbp.objects.get_team_detail_list_by_team_exclude_user(
            instance.team_detail_abp.team_abp.id, instance.team_detail_abp.user.id
        )
        if team_details is not None:
            for student in team_details:
                new_rate_perform_action = RatePerformActionStepFiveAbp()
                new_rate_perform_action.perform_action_step_five_abp = instance
                new_rate_perform_action.user = student.user
                new_rate_perform_action.rate_perform_action = 0
                new_rate_perform_action.active = True
                new_rate_perform_action.save()


post_save.connect(post_save_student_idea_step_two_abp, sender=StudentIdeaStepTwoAbp)
post_save.connect(post_save_perform_action_step_five_abp, sender=PerformActionStepFiveAbp)


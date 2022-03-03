# Generated by Django 3.2.7 on 2022-03-02 02:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('abp_steps', '0002_getinformationstepsevenabp_learnedconceptreferencestepthreeabp_learnedconceptstepthreeabp_performact'),
    ]

    operations = [
        migrations.CreateModel(
            name='RatePerformActionStepFiveAbp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('auth_state', models.CharField(default='A', max_length=3)),
                ('active', models.BooleanField(blank=True, default=True)),
                ('rate_perform_action', models.PositiveSmallIntegerField(choices=[(0, 'Nothing'), (1, 'Disagree'), (2, 'Agree')])),
                ('perform_action_step_five_abp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='abp_steps.performactionstepfiveabp')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'RatePerformActionStepFiveAbp',
                'db_table': 'rate_perform_action_step_five_abp',
            },
        ),
    ]

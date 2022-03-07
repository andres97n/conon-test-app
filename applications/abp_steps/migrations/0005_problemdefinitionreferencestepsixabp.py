# Generated by Django 3.2.7 on 2022-03-03 21:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('abp', '0012_alter_teamabp_step'),
        ('abp_steps', '0004_alter_rateperformactionstepfiveabp_rate_perform_action'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProblemDefinitionReferenceStepSixAbp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('auth_state', models.CharField(default='A', max_length=3)),
                ('active', models.BooleanField(blank=True, default=True)),
                ('problem_reference', models.URLField()),
                ('team_abp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='abp.teamabp')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'ProblemDefinitionReferenceStepSixAbp',
                'db_table': 'problem_definition_reference_step_six_abp',
            },
        ),
    ]
# Generated by Django 3.2.7 on 2022-02-21 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abp_steps', '0002_getinformationstepsevenabp_learnedconceptreferencestepthreeabp_learnedconceptstepthreeabp_performact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ratestudentideasteptwoabp',
            name='rate_student_idea',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]

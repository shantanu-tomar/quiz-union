# Generated by Django 3.0.8 on 2020-10-18 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0010_auto_20201018_1126'),
        ('users', '0005_profile_quizzes_taken'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='attempted_questions',
            field=models.ManyToManyField(to='quiz.AnsweredQuestion'),
        ),
    ]
# Generated by Django 3.0.8 on 2020-10-18 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0007_auto_20201018_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answeredquestion',
            name='answer_status',
            field=models.CharField(choices=[('c', 'Correct'), ('w', 'Wrong')], max_length=1),
        ),
    ]

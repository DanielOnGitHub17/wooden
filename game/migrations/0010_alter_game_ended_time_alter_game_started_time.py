# Generated by Django 5.0.6 on 2024-06-21 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0009_alter_game_ended_time_alter_game_started_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='ended_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='started_time',
            field=models.DateTimeField(null=True),
        ),
    ]
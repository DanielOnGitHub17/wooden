# Generated by Django 5.0.6 on 2024-06-21 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0008_alter_game_max_hits'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='ended_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='game',
            name='started_time',
            field=models.DateTimeField(),
        ),
    ]

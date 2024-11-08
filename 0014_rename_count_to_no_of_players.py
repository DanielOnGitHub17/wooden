from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('game', '0013_game_passcode'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='no_of_players',
            new_name='no_of_players',
        ),
    ]

# Generated by Django 4.2.3 on 2023-08-21 23:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_profile_avatar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='avatar',
            new_name='image',
        ),
    ]

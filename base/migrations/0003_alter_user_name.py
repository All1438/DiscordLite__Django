# Generated by Django 4.2.3 on 2023-08-06 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_user_avatar_user_bio_user_name_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]

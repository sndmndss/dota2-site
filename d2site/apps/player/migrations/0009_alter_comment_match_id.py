# Generated by Django 4.2.7 on 2023-12-23 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0008_alter_comment_author_uid_alter_comment_match_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='match_id',
            field=models.BigIntegerField(),
        ),
    ]
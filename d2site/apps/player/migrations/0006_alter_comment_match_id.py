# Generated by Django 4.2.7 on 2023-12-22 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0005_alter_comment_match_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='match_id',
            field=models.CharField(max_length=30),
        ),
    ]

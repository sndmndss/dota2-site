# Generated by Django 4.2.7 on 2023-12-17 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_alter_steamuser_steamid3'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='steamuser',
            name='id',
        ),
        migrations.AlterField(
            model_name='steamuser',
            name='steamID3',
            field=models.CharField(max_length=15, primary_key=True, serialize=False),
        ),
    ]

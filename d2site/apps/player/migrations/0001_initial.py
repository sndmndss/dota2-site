# Generated by Django 4.2.7 on 2023-12-14 23:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0004_alter_steamuser_steamid3'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('match_id', models.CharField(max_length=30)),
                ('author_uid', models.CharField(max_length=30)),
                ('steam_users', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.steamuser')),
            ],
        ),
    ]

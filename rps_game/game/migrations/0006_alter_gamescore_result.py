# Generated by Django 4.2.3 on 2023-07-23 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_alter_gamescore_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamescore',
            name='result',
            field=models.PositiveIntegerField(default=0),
        ),
    ]

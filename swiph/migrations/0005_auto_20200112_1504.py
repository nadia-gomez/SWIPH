# Generated by Django 2.0.5 on 2020-01-12 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swiph', '0004_auto_20200111_2104'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulation',
            name='nLoops',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='simulation',
            name='nModBoil',
            field=models.IntegerField(default=6),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='A_aperture',
            field=models.FloatField(default=26.4),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='GeomEffects',
            field=models.FloatField(default=0.632),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='I_bn_des',
            field=models.FloatField(default=950),
        ),
    ]

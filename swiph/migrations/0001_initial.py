# Generated by Django 2.0.5 on 2020-01-11 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='simulation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True)),
                ('industry', models.CharField(default='unknown', max_length=60)),
                ('process', models.CharField(default='unknown', max_length=80)),
                ('size', models.CharField(default='unknown', max_length=20)),
            ],
        ),
    ]

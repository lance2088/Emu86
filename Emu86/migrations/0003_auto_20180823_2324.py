# Generated by Django 2.0.7 on 2018-08-23 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Emu86', '0002_site'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='name',
            field=models.CharField(max_length=128),
        ),
    ]

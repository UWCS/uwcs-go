# Generated by Django 2.2.16 on 2020-10-06 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redirect', '0002_auto_20190918_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redirect',
            name='source',
            field=models.CharField(max_length=50),
        ),
    ]

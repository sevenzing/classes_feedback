# Generated by Django 3.1 on 2020-10-21 18:54

from django.db import migrations, models
import surveys.models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0005_auto_20201021_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='id',
            field=models.BigIntegerField(default=surveys.models.ten_digits_id, primary_key=True, serialize=False),
        ),
    ]

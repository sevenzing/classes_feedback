# Generated by Django 3.1.1 on 2020-11-07 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0010_auto_20201024_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_data',
            field=models.TextField(default='Sample choice 1; Sample choice 2', verbose_name='Content of question'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_data', models.TextField(verbose_name='Content of answer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='surveys.question')),
            ],
        ),
    ]
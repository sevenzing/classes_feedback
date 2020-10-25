# Generated by Django 3.1 on 2020-10-21 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0004_auto_20201011_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='number',
            field=models.IntegerField(default=1, verbose_name='Order of question'),
        ),
        migrations.AddField(
            model_name='question',
            name='question_data',
            field=models.TextField(default="['Sample choice 1', 'Sample choice 2']", verbose_name='Content of question'),
        ),
        migrations.AddField(
            model_name='question',
            name='question_type',
            field=models.SmallIntegerField(choices=[(0, 'Single choice'), (1, 'Multichoice'), (2, 'Rate question'), (3, 'Input text')], default=0, verbose_name='Question type'),
        ),
        migrations.AddField(
            model_name='question',
            name='required',
            field=models.BooleanField(default=False, verbose_name='Required'),
        ),
        migrations.AlterField(
            model_name='course',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='surveys.subject'),
        ),
        migrations.AlterField(
            model_name='coursegroup',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coursegroups', to='surveys.course'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.CharField(default='Sample question text', max_length=200, verbose_name='Text of question'),
        ),
        migrations.AlterField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='surveys.survey'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='surveys', to='surveys.course'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='survey_short_name',
            field=models.CharField(max_length=100, verbose_name='Short name for survey'),
        ),
    ]

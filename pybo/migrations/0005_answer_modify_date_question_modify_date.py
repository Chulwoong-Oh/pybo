# Generated by Django 4.1.4 on 2022-12-25 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0004_alter_answer_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='modify_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='modify_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
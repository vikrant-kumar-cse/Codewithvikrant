# Generated by Django 5.0.6 on 2024-10-10 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_testresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='quesmodel',
            name='question_no',
            field=models.IntegerField(max_length=30, null=True),
        ),
    ]
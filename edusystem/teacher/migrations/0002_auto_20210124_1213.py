# Generated by Django 3.1.4 on 2021-01-24 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teacher',
            old_name='ter_id',
            new_name='tea_id',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='id',
        ),
        migrations.AlterField(
            model_name='teacher',
            name='tea_no',
            field=models.CharField(max_length=8, primary_key=True, serialize=False),
        ),
    ]

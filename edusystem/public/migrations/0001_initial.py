# Generated by Django 3.1.4 on 2021-01-23 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Checkcode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(max_length=40)),
                ('session_data', models.CharField(max_length=5)),
                ('expire_date', models.DateTimeField()),
            ],
        ),
    ]

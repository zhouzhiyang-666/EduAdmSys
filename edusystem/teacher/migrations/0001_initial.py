# Generated by Django 3.1.4 on 2021-01-24 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tea_no', models.CharField(max_length=8)),
                ('tea_name', models.CharField(max_length=30)),
                ('tea_sex', models.CharField(choices=[(1, '男'), (2, '女')], default=2, max_length=1)),
                ('tea_degree', models.CharField(choices=[(1, '本科'), (1, '硕士'), (1, '博士'), (1, '其他')], default=1, max_length=2)),
                ('tea_title', models.CharField(choices=[(1, '教授'), (1, '副教授'), (1, '讲师'), (1, '助教')], default=1, max_length=3)),
                ('tea_birth', models.DateField()),
                ('ter_id', models.CharField(max_length=18)),
                ('tea_tel', models.CharField(max_length=11)),
                ('tea_pol', models.CharField(choices=[(1, '共青团员'), (2, '共产党员'), (3, '入党积极分子'), (4, '其他党派'), (5, '群众')], default=1, max_length=6)),
                ('tea_dpt', models.CharField(max_length=2)),
                ('tea_wkt', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'tbl_teacher',
                'managed': True,
            },
        ),
    ]

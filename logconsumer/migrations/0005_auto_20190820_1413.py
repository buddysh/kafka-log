# Generated by Django 2.1.3 on 2019-08-20 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logconsumer', '0004_auto_20190820_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginfo',
            name='status',
            field=models.SmallIntegerField(choices=[(1, 'running'), (0, 'stop')], default=0, verbose_name='任务状态'),
        ),
    ]

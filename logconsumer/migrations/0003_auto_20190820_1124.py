# Generated by Django 2.1.3 on 2019-08-20 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logconsumer', '0002_loginfo_task_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='loginfo',
            name='detail',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='任务详细信息'),
        ),
        migrations.AddField(
            model_name='loginfo',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'running'), (1, 'stop')], default=0, verbose_name='任务状态'),
        ),
    ]

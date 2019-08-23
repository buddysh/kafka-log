from django.db import models
from django.utils import timezone
# Create your models here.

class LogInfo(models.Model):
    task_status=(
        (0,'running'),
        (1,'stop'),
    )
    service_name=models.CharField(max_length=32,blank=True,null=True,unique=True,verbose_name="服务名称")
    kafka=models.CharField(max_length=32,blank=True,null=True,verbose_name="kafka服务器地址")
    topic=models.CharField(max_length=32,blank=True,null=True,unique=True,verbose_name="kafka topic")
    log_path=models.CharField(max_length=256,blank=True,null=True,verbose_name="日志路径")
    task_id=models.CharField(max_length=128,blank=True,null=True,verbose_name="task id")
    status=models.SmallIntegerField(choices=task_status,default=1,verbose_name="任务状态")
    detail=models.CharField(max_length=512,blank=True,null=True,verbose_name="任务详细信息")
    create_time = models.DateTimeField(default=timezone.now, verbose_name="申请时间")
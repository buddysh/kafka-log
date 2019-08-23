
from celery.app.task import Task

from celery import Celery
from django.conf import settings
from kafka import KafkaConsumer

from logconsumer import models
from logconsumer import views

import json
celery_app = Celery('tasks', backend='redis://localhost:6379/1', broker='redis://localhost:6379/0')
# this is celery settings



class MyKafka:
    def __init__(self,topic,servers,log):
        self.topic=topic
        self.servers=servers
        self.log=log

    def consumer(self,mycon):
        for message in mycon:
            with open(self.log,'ab') as f:
                msg=message.value.decode('utf8')
                nmsg=json.loads(msg)
                f.write((nmsg.get('agent').get('hostname')+": " +nmsg.get('message')).encode('utf8'))
                f.write(b'\n')



class MyTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """
        任务失败时执行
        """
        loginfo=models.LogInfo.objects.filter(task_id=task_id).last()
        loginfo.status=1
        loginfo.detail = exc
        loginfo.save()

    def on_success(self, retval, task_id, args, kwargs):
        """
        任务成功时执行
        """
        loginfo=models.LogInfo.objects.filter(task_id=task_id).last()
        loginfo.status = 1
        loginfo.detail = retval
        loginfo.save()

# this is a function about need some period
@celery_app.task
def add(a, b):
    # time.sleep(5)
    print('hello')
    return a + b


#消费kafka日志任务
@celery_app.task(base=MyTask,bind=True)
def online(self,mytopic,server,logPath,id):

    models.LogInfo.objects.filter(id=id).update(task_id=self.request.id)
    # models.LogInfo.objects.filter(id=id).update(status=0)

    tkafka = MyKafka(mytopic, server, logPath)
    loginfo=models.LogInfo.objects.filter(topic=mytopic).last()
    status=loginfo.status
    myconsumer = KafkaConsumer(tkafka.topic,bootstrap_servers=[tkafka.servers])
    if status == 1:
        loginfo.status=0
        loginfo.save()
        print(11111111)
        tkafka.consumer(myconsumer)
        return mytopic



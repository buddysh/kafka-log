from celery import Celery
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

import json
from kafka import KafkaConsumer

from LogCollection import celery
from logconsumer import task
from logconsumer.models import LogInfo
from logconsumer.task import add, celery_app


# class MyKafka:
#     def __init__(self,topic,servers,log):
#         self.topic=topic
#         self.servers=servers
#         self.log=log
#
#     def consumer(self,mycon):
#         for message in mycon:
#             with open(self.log,'ab') as f:
#                 msg=message.value.decode('utf8')
#                 nmsg=json.loads(msg)
#                 f.write((nmsg.get('agent').get('hostname')+": " +nmsg.get('message')).encode('utf8'))
#                 f.write(b'\n')

    # def activate(self):
    #     return self.topic+" is active"
#
# mykafka=MyKafka('tomcat','192.168.44.128:9092','test.log')
#
# myconsumer=KafkaConsumer(mykafka.topic,bootstrap_servers=[mykafka.servers])
#
# mykafka.consumer(myconsumer)


def index(request):
    loginfos=LogInfo.objects.all()
    return render(request,'index.html',locals())


def addlog(request):
    loginfo=LogInfo()
    serviceName=request.GET.get("serviceName")
    mytopic=request.GET.get("topic")
    logPath=request.GET.get("logPath")

    server=settings.KAFKA_RUL
    loginfo.service_name=serviceName
    loginfo.kafka=server
    loginfo.topic=mytopic
    loginfo.log_path=logPath
    loginfo.save()

    # 异步执行
    res = task.online.delay(mytopic,server,logPath,loginfo.pk)

    response_data={
        "status":0,
    }
    return JsonResponse(response_data)


# def getstat(request):
#     data=request.GET.get('data')
#     celery_app.control.revoke("73327e4c-2214-49ad-8b68-28c1a8003ef3", terminate=True)
#     result = celery_app.AsyncResult("73327e4c-2214-49ad-8b68-28c1a8003ef3")
#     response_data={
#         "status":0,
#     }
#     return JsonResponse(response_data)


def deletetask(request):
    taskid = request.GET.get('taskid')
    celery_app.control.revoke(taskid, terminate=True)
    LogInfo.objects.filter(task_id=taskid).delete()

    response_data={
        "status":0,
    }
    return JsonResponse(response_data)

def resettask(request):
    taskid=request.GET.get('taskid')
    loginfo=LogInfo.objects.filter(task_id=taskid).last()

    celery_app.control.revoke(taskid,terminate=True)
    loginfo.status=1
    loginfo.save()
    result=celery_app.AsyncResult(taskid)
    status=result.status
    res = task.online.delay(loginfo.topic, loginfo.kafka, loginfo.log_path, loginfo.pk)

    response_data={
        "status":status,
    }
    return JsonResponse(response_data)
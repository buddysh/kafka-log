from django.urls import path

from logconsumer import views

app_name = 'logconsumer'
urlpatterns=[
    path('',views.index,name='index'),
    path('addlog/',views.addlog,name='addlog'),
    # path('getstat/',views.getstat,name='getstat'),
    path('deletetask/',views.deletetask,name='deletetask'),
    path('resettask/',views.resettask,name='resettask'),
]
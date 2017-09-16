from django.db import models

# Create your models here.
#发布会前端页面


class Event(models.Model):
    name = models.CharField(max_length=100)
    limit = models.IntegerField()
    status = models.BooleanField()
    address = models.CharField(max_length=200)
    start_time = models.DateTimeField('events time')
    create_time = models.DateTimeField(auto_now=True)#创建时间自动，当前时间

    def __str__(self):
        return self.name

#嘉宾表


class Guest(models.Model):
    event = models.ForeignKey(Event)
    realname = models.CharField(max_length=64)
    phone = models.CharField(max_length=16)
    email = models.EmailField()
    sign = models.BooleanField()
    create_time = models.DateTimeField(auto_now=True)

    class Meta:#内部类，用来定义Guest模型的一些行为特性
        unique_together = ("event", "phone")#unique_together用于设置两个字段为联合主键

    def __str__(self):
        return self.realname
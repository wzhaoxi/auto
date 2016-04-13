#coding: utf-8

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Admin(models.Model):
    username = models.OneToOneField('auth.User')
#    passwd = models.CharField(max_length = 50)
    email = models.CharField(max_length = 50)
    phone = models.CharField(max_length = 20,null = True)


    class Meta:
        ordering = ('username',)


class Deploy(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    appversion = models.CharField(max_length = 50)
    codeversion =  models.CharField(max_length = 50)
    startTime = models.DateTimeField()
    status = models.BooleanField()
    number = models.IntegerField(null = True)
    admin = models.ForeignKey(Admin)

    class Meta:
        ordering = ('created',)


class JenkinsConfig(models.Model):
    id = models.IntegerField(primary_key=True, default=1)
    url = models.CharField(max_length=100)
    jobName= models.CharField(max_length=50)
    user =  models.CharField(max_length=50, null = True,  blank=True, default='')
    password =  models.CharField(max_length=100, null = True , blank=True, default='')

    def get_config(self):
        config = {'url': self.url, 'jobName': self.jobName, 'user': self.user, 'password': self.password}
        return config

    class Meta:
        ordering = ('user',)

class DeployConfig(models.Model):
    id = models.IntegerField(primary_key=True, default=1)
    sourcepath = models.CharField(max_length=200)
    dest_path = models.CharField(max_length=100)
    release_dir = models.CharField(max_length=100)
    webapp_name =  models.CharField(max_length=100)
    war_name = models.CharField(max_length=100)

    request_domain = models.CharField(max_length=100)
    request_uri = models.CharField(max_length=100)
    current_link = models.CharField(max_length=50)
    host_string = models.CharField(max_length=100, null = True, blank=True, default='')
    host_passwd = models.CharField(max_length=100, null = True, blank=True, default='')

    def get_config(self):
        config = {'sourcepath': self.sourcepath, 'dest_path': self.dest_path, 'release_dir': self.release_dir, 'webapp_name': self.webapp_name, \
                  'war_name': self.war_name, 'request_domain': self.request_domain, 'request_uri': self.request_uri, 'current_link': self.current_link, \
                  'host_string': self.host_string, 'host_passwd': self.host_passwd}
        return config



class Log(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    deploy = models.ForeignKey(Deploy)
    message = models.TextField()
#    buildnum = models.IntegerField()

    class Meta:
        ordering = ('created',)

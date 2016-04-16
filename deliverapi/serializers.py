#coding: utf-8

from rest_framework import serializers
from deliverapi.models import Admin, Deploy, Log, JenkinsConfig, DeployConfig
from django.contrib.auth.models import User

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ('id', 'username', 'email','phone')

class DeploySerializer(serializers.ModelSerializer):
#    appversion = serializers.CharField()
#    codeversion= serializers.CharField()
#    time = serializers.DateTimeField()
#    status = serializers.BooleanField()
#    number = serializers.IntegerField()
#    admin = serializers.CharField()
#
#    def create(self, validated_data):
#        """
#        Create and return a new `Deployment` instance, given the validated data.
#        """
#        return Admin.objects.create(**validated_data)

    class Meta:
        model = Deploy
        fields = ('id', 'created','appversion', 'codeversion', 'startTime', 'status', 'logID','admin')

class JenkinsConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = JenkinsConfig
        fields = ('id', 'url','jobName', 'user', 'password')



class DeployConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeployConfig
        fields = ('id', 'sourcepath','dest_path', 'release_dir', 'webapp_name', 'war_name', 'request_domain', 'request_uri' ,'current_link', 'host_string', 'host_passwd')





class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ('id', 'created','deploy', 'message')


class LoginSerializer(serializers.ModelSerializer):

    username = serializers.CharField(required=False, max_length=1024)
    password = serializers.CharField(required=False, max_length=1024)

    class Meta:
        model = User
        fields = ('id', 'username', 'password')

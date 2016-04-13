#codeing: utf-8
from django.shortcuts import render,render_to_response

from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view

from deliverapi.models import Admin, Deploy, Log, JenkinsConfig, DeployConfig
from deliverapi.serializers import AdminSerializer, DeploySerializer, LogSerializer,JenkinsConfigSerializer,DeployConfigSerializer

from django.contrib.auth.models import User
import urllib, urllib2, datetime
import json, os


from deliverapi.integration import Integration
from deliverapi.deploy import Deployment
# Create your views here.



class AdminAuth(APIView):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

    def post(self, request):
        try:
            print "test"
            name = request.data.get('name')
            passwd = request.data.get('passwd')
            admin = Admin.objects.get(name__iexact=name)
            if admin.check_password(passwd):
                print admin
                serializer = LoginSerializer({'id': admin.id, 'name': admin.name})
                return Response(serializer.data)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        except Admin.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class DeployList(APIView):
    """
    List all Deployments, or create a new deployment.
    """
    def get_admin(self,username):
        user = User.objects.get(username=username)
        admin = Admin.objects.get(username=user)
        return  admin.id

    def get(self, request, format=None):
        deploys = Deploy.objects.all()
        serializer = DeploySerializer(deploys, many=True)
        return Response(serializer.data)

    def get_jenkinsConfig(self):
        try:
            config = JenkinsConfig.objects.get(id=1)
            return config.get_config()
        except JenkinsConfig.DoesNotExist:
            return False

    def get_deployConfig(self):
        try:
            config = DeployConfig.objects.get(id=1)
            return config.get_config()
        except DeployConfig.DoesNotExist:
            return False

    def post(self, request, format=None):
        admin =  self.get_admin(unicode(request.user))
        startTime = datetime.datetime.now()
        depInfo = {'appversion': request.data['appversion'] , 'codeversion': request.data['codeversion'], \
                   'startTime': startTime, 'status': False, 'number':None, 'admin':admin}
        integrate = Integration(self.get_jenkinsConfig())
        integrate.start_build(depInfo['codeversion'])
        if not integrate.is_good():
            if serializer.is_valid():
                serializer.save()
#            Response( {'error': 'build error'}, status=status.HTTP_400_BAD_REQUEST)
        num = integrate.get_number()
        dep = Deployment(self.get_deployConfig(), depInfo['appversion'],num)
        dep.start_deploy()
        depInfo['status'] = True
        depInfo['number'] = num
        serializer = DeploySerializer(data=depInfo)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class DeployDetail(APIView):
    """
    Retrieve, update or delete a deploy instance.
    """
    def get_object(self, id):
        try:
            return Deploy.objects.get(id=id)
        except Deploy.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        deploy = self.get_object(id)
        serializer = DeploySerializer(deploy)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        deploy = self.get_object(id)
        serializer = DeploySerializer(deploy, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        deploy = self.get_object(id)
        deploy.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class JenkinsConfigDetail(APIView):
    """
    List JenkinsConfig, create a new JenkinsConfig, or modify JenkinsConfig.
    """
    def get_object(self):
        try:
            return JenkinsConfig.objects.get(id=1)
        except JenkinsConfig.DoesNotExist:
            return False

    def get(self, request, format=None):
        jenkinsConfig = JenkinsConfig.objects.all()
        serializer = JenkinsConfigSerializer(jenkinsConfig, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        jenkinsConfig = self.get_object()
        if  jenkinsConfig :
            serializer = JenkinsConfigSerializer(jenkinsConfig, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else :
            print request.data
            serializer = JenkinsConfigSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DeployConfigDetail(APIView):
    """
    List DeployConfigConfig, create a new DeployConfig, or modify DeployConfig.
    """
    def get_object(self):
        try:
            return DeployConfig.objects.get(id=1)
        except DeployConfig.DoesNotExist:
            return False

    def get(self, request, format=None):
        deployConfig = DeployConfig.objects.all()
        serializer = DeployConfigSerializer(deployConfig, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        deployConfig = self.get_object()
        if  deployConfig :
            serializer = DeployConfigSerializer(deployConfig, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else :
            print request.data
            serializer = DeployConfigSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class LogDetail(APIView):
    """
    Retrieve, update or delete a deploy instance.
    """
    def get_object(self, id):
        if os.path.exists('deliverapi/file/' + str(id)) :
            file_hander = open('deliverapi/file/' + str(id), 'r')
            try:

                return file_hander.read()
            finally:
                file_hander.close()
        else:
            raise Http404

    def get(self, request, id, format=None):
        username =  unicode(request.user)
        log = self.get_object(id)
        return Response({"log": log})


    def delete(self, request, id, format=None):
        os.remove('deliverapi/file/' + str(id))
        return Response(status=status.HTTP_204_NO_CONTENT)





@api_view()
def get_tag(req):
    """
      get the remote  github tag version.
    """
    giturl =  "https://api.github.com/repos/wzhaoxi/userfor/tags"
    result = urllib2.urlopen(giturl)
    jsondata = json.loads(result.read())
    id = 0
    listVersion =[]
    for i in jsondata:
       version =  { 'id': id , "version" : i['name']}
       listVersion.append(version)
       id = id + 1
    return Response(listVersion)

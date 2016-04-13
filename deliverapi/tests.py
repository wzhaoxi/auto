from django.test import TestCase
from django.core.urlresolvers import reverse

from deliverapi.models import JenkinsConfig, DeployConfig, Admin
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import force_authenticate
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
# Create your tests here.




def createOriginData():
    user = User.objects.create_superuser(username='root',email="root@qq.com",password='123456')
    admin = Admin(username=user,email="wu.xi@menpuji.com",phone='15739576385')
    admin.save()
    DeployConfig.objects.create(
                sourcepath="/tmp/userfor.war",
                dest_path="/usr/local/",
                release_dir="app",
                webapp_name="userfor",
                war_name="userfor.war",
                request_domain="http://172.16.255.87",
                request_uri="userfor",
                current_link="tomcat",
                host_string="root@172.16.255.87",
                host_passwd="123456")
    JenkinsConfig.objects.create(url="http://127.0.0.1:8080",jobName="userfor",user="",password="")


class testJenkinsConfig(TestCase):
    def setUp(self):
        createOriginData()
        self.client.login(username="root", password="123456")
    def testGetConfig(self):
        test_config ={
            "url": "http://127.0.0.1:8080",
            "jobName": "userfor",
            "user": "",
            "password": ""
            }
        response = self.client.get('/api/jenkinsconfig/', type="application/json")
        config = JenkinsConfig.objects.get(id=1)
        self.assertEqual(config.get_config(),test_config)
        self.assertEqual(JenkinsConfig.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def testPostConfig(self):
        data ={
            "url": "http://127.0.0.1:80",
            "jobName": "jobname",
            "user": "",
            "password": ""
        }
        response = self.client.post("/api/jenkinsconfig/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        config = JenkinsConfig.objects.get(id=1)
        self.assertEqual(config.get_config(),data)
        self.assertEqual(JenkinsConfig.objects.count(), 1)




class GitHubTest(APITestCase):
    def setUp(self):
        pass
    def testGetTag(self):
        pass




class DeploymentTest(APITestCase):
    def setUp(self):
        createOriginData()
        self.client.login(username="root", password="123456")

    def testGetDeployInfo(self):
        response = self.client.get('/api/deployment/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def testPostDeployInfo(self):
        pass
#        user = User.objects.all()
#        print user
#        data = {"appversion": "v41", "codeversion": "v3.0"}
#        response = self.client.post("/api/deployment/", data, format='json')
#        print response
#        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def testDeleteDeployInfo(self):
        pass

    def tearDown(self):
        self.client.logout()

class DeployConfigTest(APITestCase):
    def setUp(self):
        createOriginData()
        self.client.login(username="root", password="123456")

    def testGetConfig(self):
        response = self.client.get('/api/deployconfig/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pass

    def testPostConfig(self):
        pass





class LogTest(APITestCase):
    def setUp(self):
        pass

    def testGetLog(self):
        pass

    def testDeletLog(self):
        pass

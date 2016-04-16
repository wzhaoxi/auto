#coding:utf-8
import sys, time, socket, urllib2
from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *
from fabric.contrib.console import confirm
from datetime import datetime as dt


class Deployment(object):


    def __init__(self, config, deploy_version, log_id):
        env.project_war_source = config['sourcepath']
        env.deploy_project_root = config['dest_path']
        env.deploy_release_dir = config['release_dir']
        env.deploy_webapp_name = config['webapp_name']
        env.project_war_name = config['war_name']
        env.deploy_version = deploy_version
        env.deploy_tomcat_folder = "tomcat-" + env.deploy_version

        env.head_request_domain = config['request_domain']
        env.head_request_uri = config['request_uri']
        env.deploy_dest_path = env.deploy_project_root + env.deploy_release_dir + "/" + env.deploy_tomcat_folder + '/webapps/' + env.head_request_uri +"/"+ env.project_war_name

        env.deploy_current_link = config['current_link']

        env.host_string = config['host_string']
        env.password= config['host_passwd']

        env.file_hander = open('deliverapi/file/' + str(log_id), 'w', 0)
        env.tomcat_old_version = ""
        self.step = 0
        self.status = False
        self.roll_status = False

    def get_current_version(self):
        with settings(warn_only = True):
            try:
                sys.stdout = open('/dev/null', 'a')
                with cd(env.deploy_project_root + env.deploy_release_dir):
                    version = run("ls -l tomcat", quiet=True)
                    alist= version.split(" ")
                    env.tomcat_old_version = alist[-1]
                    env.file_hander.write("[INFO]: tomcat old version is : "+ env.tomcat_old_version + "\n")
            except Exception as e:
                env.file_hander.write("ERROR: "+ str(e) + "\n")
                return False
            return True



    def create_new_tomcat(self):
        env.file_hander.write("[INFO] Create a new tomcat content...\n")
        with settings(warn_only = True):
            try:
                sys.stdout = open('/dev/null', 'a')
                with cd(env.deploy_project_root + env.deploy_release_dir):
                    env.deploy_tomcat_folder = "tomcat-" + env.deploy_version
                    dir_files = run("ls -l", quiet=True)
                    if env.deploy_tomcat_folder in dir_files:
                        env.file_hander.write("ERROR : version : " + env.deploy_tomcat_folder + "  is aready exicted\n")
                        return False
                    run("cp -r tomcat-ecs %s" %env.deploy_tomcat_folder, quiet=True)
                    dir = run("ls -l", quiet=True)
                    sys.stdout = sys.__stdout__
                    if env.deploy_tomcat_folder not in dir:
                        env.file_hander.write("ERROR : " + env.deploy_tomcat_folder + "created failed\n")
                        return False
                    env.file_hander.write("[INFO] " + env.deploy_tomcat_folder +" created completed\n")
                    return True
            except Exception as e :
                env.file_hander.write("ERROR: "+ str(e) + "\n")
                return False

    def put_war_package(self):
        with settings(warn_only =  True):
            with cd(env.deploy_project_root + env.deploy_release_dir + "/" + env.deploy_tomcat_folder + '/webapps'):
                env.file_hander.write("[INFO] pwd : " + run("pwd", quiet=True) + "\n")
                run("mkdir " + env.head_request_uri, quiet=True)
                dir = run("ls -l", quiet=True)
                if env.head_request_uri not in dir:
                    env.file_hander.write("ERROR : " + env.head_request_uri + "created failed\n")
                    return False
        env.file_hander.write("[INFO] upload war packge ----> product environment..\n")
        env.file_hander.write("[INFO] " + env.project_war_source + "---->" + env.deploy_dest_path + "\n")
        with settings(warn_only = True):
            try:
                sys.stdout = open('/dev/null', 'a')
                result = put(env.project_war_source, env.deploy_dest_path)
                sys.stdout =  sys.__stdout__
                if result.failed :
                    env.file_hander.write("Error :  Upload  war packge cancelled \n ")
                    return False
            except Exception as e:
                sys.stdout = sys.__stdout__
                env.file_hander.write("ERROR :  Upload  war packge error： \n" + str(e) +"\n")
                return False
        env.file_hander.write("[INFO] Upload  war packge completed\n")
        return True

    def unzip_war_package(self):
        env.file_hander.write("[INFO] Decompressing war packge ... \n")
        with settings(warn_only = True):
            with cd(env.deploy_project_root + env.deploy_release_dir + "/" + env.deploy_tomcat_folder + '/webapps/' + env.head_request_uri):
                run("unzip " + env.project_war_name, quiet=True)
                dir = run("ls -l", quiet=True)
#                run("rm -f" + env.project_war_name, quiet=True)
                run("rm -f %s" %env.project_war_name, quiet=True)
                file = run("ls -l",quiet=True)
                if env.project_war_name in file:
                    env.file_hander.write("ERROR : " + env.project_war_name + "  delete failed\n")
                    return False
        env.file_hander.write("[INFO] Decompress  war packge completed \n")
        return True

    def shutdown_tomcat(self):
        env.file_hander.write("[INFO] start shutdown_tomcat...\n")
        with settings(warn_only = True):
            tomcat_shut = False
            for try_time in range(1, 4):
                with cd(env.deploy_project_root + env.deploy_release_dir + "/" +  env.deploy_current_link + "/bin"):
                    env.file_hander.write("[INFO] pwd :" + env.deploy_project_root + env.deploy_release_dir + "/" +  env.deploy_current_link + "/bin")
                    env.file_hander.write("[INFO] the " + str(try_time) + "time , try to shutdown tomcat service ...\n")
                    run("./shutdown.sh", quiet=True)
                    env.file_hander.write("[INFO]  waiting...\n")
                    time.sleep(10)
                    pid = run("pgrep java", quiet=True)
                    if pid == '':
                        tomcat_shut = True
                        env.file_hander.write("[INFO] tomcat has shutdown \n")
                        break
                    else:
                        env.file_hander.write("ERROR : tomcat shutdown failed\n")
            return tomcat_shut

    def delete_slink(self):
        env.file_hander.write("[INFO] start delete the  Soft connection of old version...\n")
        with settings(warn_only = True):
            with cd(env.deploy_project_root + env.deploy_release_dir):
                run("rm -f %s" %env.deploy_current_link, quiet=True)
                dir_files = run('ls | grep "^tomcat$"', quiet=True)
                if env.deploy_current_link in dir_files:
                    env.file_hander.write("ERROR: old version link delete failed")
                    return False
                return True

    def create_slink(self, link):
        env.file_hander.write("[INFO] start creating the  Soft connection of new version...\n")
        with settings(warn_only = True):
            with cd(env.deploy_project_root + env.deploy_release_dir):

                run("ln -s %s %s" %(link, env.deploy_current_link), quiet=True)
                dir_files = run("ls -l", quiet=True)
                if env.deploy_current_link not in dir_files:
                    env.file_hander.write("ERROR: new version link create failed")
                    return False
                return True

    def startup_tomcat(self):
        env.file_hander.write("[INFO] startup tomcat..... \n")
        with settings(warn_only = True):
            try:
                sys.stdout = open('/dev/null', 'a')
                with cd(env.deploy_project_root + env.deploy_release_dir + "/" +  env.deploy_current_link + "/bin"):
                    env.file_hander.write("[INFO] pwd : " + run("pwd", quiet=True) + "\n")
                    run("nohup ./startup.sh", quiet=True)
                    time.sleep(10)
                    pid = run("pgrep java", quiet=True)
                    if pid == "":
                        env.file_hander.write("ERROR : startup tomcat failed \n")
                        return False
                    return True
            except Exception as e:
                env.file_hander.write("ERROR: "+ str(e) + "\n")
                return False



    def head_request(self):
        env.file_hander.write("[INFO] test the availability of tomcat service...  \n")
        socket.setdefaulttimeout(200)
#       for uri in env.head_request_uri:
        start = dt.now()
        url = env.head_request_domain + "/" + env.head_request_uri + "/"
        env.file_hander.write("[INFO] request :" + url + "\n")
        try:
            success = self.send(url)
            if not success:
                env.file_hander.write("ERROR : HEAD request failed\n")
                return False
        except Exception as e:
            env.file_hander.write("ERROR : HEAD request error：\n" + str(e) + "\n")
            return False
        end = dt.now()
        cost = (end-start).microseconds / 1000
        env.file_hander.write("[INFO]   response time: " + str(cost) +  "ms\n")
        return True


    def send(self,url):
        request = urllib2.Request(url,)
        try:
            request.get_method = lambda: 'HEAD'
            response = urllib2.urlopen(request)
            msg = response.msg
            if msg == 'OK':
                return True
            else :
                return False
        except urllib2.HTTPError,e:
            code = e.code
            env.file_hander.write("  code :" + e.code)
        except Exception,e:
            env.file_hander.write("ERROR:" + str(e))


    def call(self, func_list):
        for index, func_obj in enumerate(func_list):
            func_name = func_obj.keys()[0]
            env.file_hander.write("[INFO] ----------------------------------------------------------------------- \
                            \n[INFO]" + dt.strftime(dt.now(), '%Y-%m-%d %H:%M:%S') +"\n[INFO] step "+ str(index+1) + \
                            " : " + func_name + "  starting...  \n")
            func = eval(func_name)
            argv = func_obj[func_name]
            success = False
            if argv != '':
                success = func(argv)
            else:
                success = func()
            if not success:
                env.file_hander.write("ERROR : excute function : " + func_name )
                break
            self.step = index + 1
            env.file_hander.write(str(self.step) + "[INFO] success\n" )



    def rollback(self):
        env.file_hander.write("\n\n[INFO] start to rollback \n")
        if self.step == 4 :
            self.startup_tomcat()
        elif self.step == 5 :
            self.create_slink(env.tomcat_old_version)
            self.startup_tomcat()
        elif self.step == 6 :
            self.delete_slink()
            self.create_slink(env.tomcat_old_version)
            self.startup_tomcat()
        elif self.step > 6 :
            self.shutdown_tomcat()
            self.delete_slink()
            self.create_slink(env.tomcat_old_version)
            self.startup_tomcat()
        with settings(warn_only = True):
            try:
                sys.stdout = open('/dev/null', 'a')
                with cd(env.deploy_project_root + env.deploy_release_dir):
                    run("rm -rf %s" %env.deploy_tomcat_folder, quiet=True)
                    dir = run("ls -l",quiet=True)
                    if env.deploy_tomcat_folder in dir:
                        env.file_hander.write("ERROR : new version " + env.deploy_tomcat_folder + "  delete failed\n")
                        return False
            except Exception as e:
                env.file_hander.write("ERROR: "+ str(e) + "\n")
                return False
        if self.head_request():
            env.file_hander.write("[INFO] rollback completed \n")
            return True
        else:
            env.file_hander.write("[INFO] rollback failed \n")
            return False



    def start_deploy(self):
        func_list = [{'self.create_new_tomcat':''}, {'self.put_war_package':''},\
        			{'self.unzip_war_package':''}, {'self.shutdown_tomcat':''}, \
        			{'self.delete_slink':''}, {'self.create_slink':env.deploy_tomcat_folder}, \
                    {'self.startup_tomcat':''}, {'self.head_request':''}]
        self.get_current_version()
        self.call(func_list)
        if self.step != 8 :
            self.roll_status = self.rollback()
        else:
            self.status = True
        env.file_hander.close()


    def is_good(self):
        return self.status

    def rollback_good(self):
        return self.roll_status

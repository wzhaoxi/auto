from jenkinsapi.jenkins import Jenkins
from jenkinsapi.executor import Executor
from time import sleep
import urllib, urllib2


class Integration(Jenkins):
  def __init__(self, config):
    self.url = config['url']
    self.jobName = config['jobName']
    self.user = config['user']
    self.password = config['password']
    Jenkins.__init__(self, self.url, config['user'], config['password'])
    self.job = self.get_job(self.jobName)
    self.number = 0

  def start_build(self, codeversion):
    full_url = self.url + '/job/' + self.jobName + '/buildWithParameters?CODEVERSION=' + codeversion
#    print full_url
    req = urllib2.Request(full_url)
    urllib2.urlopen(req)
    while self.job.is_queued():
#      print "job is in queued"
      sleep(1)

    building = self.job.get_last_build()
    self.number = building.get_number()

    while self.job.is_running():
#      print building.get_console()
      sleep(1)
#    print building.get_console()

  def is_good(self):
    building = self.job.get_last_build()
    return building.is_good()

  def get_number(self):
      return self.number

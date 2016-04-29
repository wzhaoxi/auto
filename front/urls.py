from django.conf.urls import url, include
from front import views


urlpatterns = [
    url(r'^$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^auto_deploy/$', views.deployment),
    url(r'dep_history/$', views.dep_history),
    url(r'deployment_conf/$', views.deploymentConf),
    url(r'integration_conf/$', views.integretionConf),
    url(r'^detail/(?P<id>[0-9]+)/$', views.detail_status),
    url(r'^detail/(?P<id>[0-9]+)/log$', views.detail_log),
    url(r'^detail/(?P<id>[0-9]+)/delete$', views.detail_delete),

]

from django.conf.urls import url
from deliverapi import views


urlpatterns = [
    url(r'^login$', views.AdminAuth.as_view()),
    url(r'^deployment/$', views.DeployList.as_view()),
    url(r'^deployment/(?P<id>[0-9]+)/$', views.DeployDetail.as_view(),name="deploy-detail"),
    url(r'^log/(?P<id>[0-9]+)/$', views.LogDetail.as_view(),name="log-detail"),
    url(r'^githubtag/', views.get_tag),
    url(r'^jenkinsconfig', views.JenkinsConfigDetail.as_view()),
    url(r'^deployconfig', views.DeployConfigDetail.as_view()),

]

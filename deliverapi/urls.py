from django.conf.urls import url, include
from deliverapi import views


urlpatterns = [
    url(r'^doc/$', views.apiDocument),
    url(r'^deployment/$', views.DeployList.as_view(), name="deployment-list"),
    url(r'^deployment/(?P<id>[0-9]+)/$', views.DeployDetail.as_view(),name="deploy-detail"),
    url(r'^log/(?P<id>[0-9]+)/$', views.LogDetail.as_view(),name="log-detail"),
    url(r'^codeversion/', views.get_tag, name="tag-list"),
    url(r'^integrationConf/', views.JenkinsConfigDetail.as_view(), name="show-JenkinsConfig"),
    url(r'^deploymentConf/', views.DeployConfigDetail.as_view(), name="show-DeploymentConfig"),
    url(r'^doc/images/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': 'deliverapi/templates/images/' }),
    url(r'^doc/lib/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': 'deliverapi/templates/lib/' }),
    url(r'^doc/css/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': 'deliverapi/templates/css/' }),
    url(r'^doc/fonts/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': 'deliverapi/templates/fonts/' }),
#    url(r'^login/$', views.LoginViewSet.as_view()),
]

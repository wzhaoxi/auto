#coding: utf-8
from django.shortcuts import render, render_to_response, RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django import forms
from django.http import HttpRequest,HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import JsonResponse
from django.template import loader, Context

from deliverapi.models import Admin, Deploy, Log, JenkinsConfig, DeployConfig

# Create your views here.

class LoginForm(forms.Form):
    username = forms.CharField(
            required = True,
            label=u"username",
            widget=forms.TextInput(
                attrs={
                    'placeholder':u"username",
                    'id':"username",
                    'required': u"required",
                    }
                )
            )

    password = forms.CharField(
            required=True,
            label=u"password",
            widget=forms.PasswordInput(
                attrs={
                    'placeholder':u"password",
                    'id':"password",
                    'required': u"required",
                    }
                ),
            )

@csrf_exempt
def login(req):
    if req.method == "POST":
        form = LoginForm(req.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username,password=password)
            if user is not None and user.is_active:
                auth.login(req,user)
                return HttpResponse('{"auth":true}',content_type="application/json")
            else:
                return HttpResponse('{"auth":false}',content_type="application/json")

    else :
        form = LoginForm()
    return render_to_response('login.html',{'form':form},context_instance=RequestContext(req))




@login_required
def logout(req):
    auth.logout(req)
    return HttpResponseRedirect("/")


def deployment(req):
    if req.user.is_authenticated():
        return render_to_response('auto_deploy.html',context_instance=RequestContext(req))

    else:
        return HttpResponseRedirect('/')

def deploymentConf(req):
    if req.user.is_authenticated():
        return render_to_response('deploymentconf.html',context_instance=RequestContext(req))

    else:
        return HttpResponseRedirect('/')

def integretionConf(req):
    if req.user.is_authenticated():
        return render_to_response('integrationconf.html',context_instance=RequestContext(req))

    else:
        return HttpResponseRedirect('/')











def dep_history(req):
    if req.user.is_authenticated():
        return render_to_response('deploy-history.html',context_instance=RequestContext(req))

    else:
        return HttpResponseRedirect('/')


def get_next_id(id):
    gt_deploy = Deploy.objects.filter(id__gt=id)
    if gt_deploy:
        return gt_deploy[0].id
    else :
        return None

def get_last_id(id):
    lt_deploy = list(Deploy.objects.filter(id__lt=id))
    if lt_deploy:
        return lt_deploy[-1].id
    else :
        return None






def detail_log(req, id):
    if req.user.is_authenticated():
        next_id = get_next_id(id)
        last_id = get_last_id(id)
        temp = loader.get_template('detail-log.html')
        con = Context({'id': id, 'next_id': next_id, 'last_id': last_id})
        html = temp.render(con)
        response = HttpResponse(html)
        response['Access-Control-Allow-Origin'] = '*'
        return response
    #    return render_to_response('detail-log.html', {'id': id, 'next_id': next_id, 'last_id': last_id}, context_instance=RequestContext(req))
    else:
        return HttpResponseRedirect('/')


def detail_status(req, id):
    if req.user.is_authenticated():
        next_id = get_next_id(id)
        last_id = get_last_id(id)

        return render_to_response('detail-status.html', {'id': id, 'next_id': next_id, 'last_id': last_id}, context_instance=RequestContext(req))

    else:
        return HttpResponseRedirect('/')



def detail_delete(req, id):
    if req.user.is_authenticated():
        next_id = get_next_id(id)
        last_id = get_last_id(id)
        print req.user
        return render_to_response('detail-delete.html', {'id': id, 'next_id': next_id, 'last_id': last_id}, context_instance=RequestContext(req))

    else:
        return HttpResponseRedirect('/')

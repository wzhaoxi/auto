#coding: utf-8

from django.contrib import admin
from deliverapi.models import Admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# Register your models here.

#admin.site.unregister(User)
#admin.site.register(User,Admin)


class AdminInline(admin.StackedInline):
    model = Admin

class UserAdmin(UserAdmin):
    inlines = (AdminInline,)


#class AuthorAdmin(admin.ModelAdmin):
#    pass

admin.site.unregister(User)
admin.site.register(User,UserAdmin)

from django.contrib import admin
from udyam_backend.models import Event, Team, Workshop, Content, BroadCast_Email, Personal_Email, Team_List

from django.utils.safestring import mark_safe
from django.db import models
import threading
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import (send_mail, BadHeaderError, EmailMessage)
from authentication.models import User
from .sheets import addtosheet

class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run(self):
        msg1 = EmailMessage(self.subject, self.html_content, settings.EMAIL_HOST_USER, self.recipient_list[:100])
        msg1.content_subtype = "html"
        msg2 = EmailMessage(self.subject, self.html_content, settings.EMAIL_HOST_USER, self.recipient_list[100:200])
        msg2.content_subtype = "html"
        msg3 = EmailMessage(self.subject, self.html_content, settings.EMAIL_HOST_USER, self.recipient_list[200:300])
        msg3.content_subtype = "html"
        msg4 = EmailMessage(self.subject, self.html_content, settings.EMAIL_HOST_USER, self.recipient_list[300:400])
        msg4.content_subtype = "html"
        msg5 = EmailMessage(self.subject, self.html_content, settings.EMAIL_HOST_USER, self.recipient_list[400:500])
        msg5.content_subtype = "html"
        msg6 = EmailMessage(self.subject, self.html_content, settings.EMAIL_HOST_USER, self.recipient_list[500:600])
        msg6.content_subtype = "html"
        msg7 = EmailMessage(self.subject, self.html_content, settings.EMAIL_HOST_USER, self.recipient_list[600:])
        msg7.content_subtype = "html"
        try:
            msg1.send()
            msg2.send()
            msg3.send()
            msg4.send()
            msg5.send()
            msg6.send()
            msg7.send()
        except BadHeaderError:
            return HttpResponse('Invalid header found.')

class PersonalEmail(threading.Thread):
    def __init__(self, subject, html_content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run(self):
        for user in self.recipient_list:
            msg = EmailMessage(self.subject, self.html_content, settings.EMAIL_HOST_USER, [user])
            try:
                msg.send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

class BroadCast_Email_Admin(admin.ModelAdmin):
    model = BroadCast_Email

    def submit_email(self, request, obj): #`obj` is queryset, so there we only use first selection, exacly obj[0]
        list_email_user = [ p.email for p in User.objects.all() ] #: if p.email != settings.EMAIL_HOST_USER   #this for exception
        obj_selected = obj[0]
        EmailThread(obj_selected.subject, mark_safe(obj_selected.message), list_email_user).start()
    submit_email.short_description = 'Send BroadCast (1 Select Only)'
    submit_email.allow_tags = True

    actions = [ 'submit_email' ]

    list_display = ("subject", "created")
    search_fields = ['subject',]

class Personal_Email_Admin(admin.ModelAdmin):
    model = Personal_Email

    def submit_email(self, request, obj): #`obj` is queryset, so there we only use first selection, exacly obj[0]
        list_email_user = [ p.email for p in User.objects.all() ] #: if p.email != settings.EMAIL_HOST_USER   #this for exception
        obj_selected = obj[0]
        PersonalEmail(obj_selected.subject, mark_safe(obj_selected.message), list_email_user).start()
    submit_email.short_description = 'Send Personal Email (1 Select Only)'
    submit_email.allow_tags = True

    actions = [ 'submit_email' ]

    list_display = ("subject", "created")
    search_fields = ['subject',]

class Team_List_Admin(admin.ModelAdmin):
    model = Team_List

    def update_list(self, request, objects_selected):
        for obj in objects_selected:
            teamlist = Team.objects.filter(event = obj.event)
            sheetname = obj.event.eventname + " Teams"
            addtosheet(sheetname, teamlist)
    update_list.short_description = 'Update selected events team list'

    actions = [ 'update_list' ]
    list_display = ("event", )

class Team_Admin(admin.ModelAdmin):
    model = Team
    search_fields = ['event__eventname']
    list_display = ("team_name", "event")



admin.site.register(BroadCast_Email, BroadCast_Email_Admin)
admin.site.register(Personal_Email, Personal_Email_Admin)
admin.site.register(Team_List, Team_List_Admin)
admin.site.register(Event)
admin.site.register(Team, Team_Admin)
admin.site.register(Workshop)
admin.site.register(Content)
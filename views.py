# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.translation import gettext as __
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from apps.profiles.models import Doctor

@login_required
def index(request, template="site_base.html"):
    context = {}
    try:
        user_profile = request.user.get_profile()
    except:
        user_profile = None
    if user_profile:
        if user_profile.user_type == '1':
            clients = Doctor.objects.get(user=request.user).clients.all()
            show_up_quant = [[].append(client) for client in clients if client.medical_appointment.all()].__len__()
            lost_quant = [[].append(client) for client in clients if not client.medical_appointment.all()].__len__()
            print float(1)/2
            print 1/2
            context = {
                'show_up_quant': show_up_quant,
                'show_up_percent': int((float(show_up_quant)/clients.count()) * 100),
                'lost_quant': lost_quant,
                'lost_percent': int((float(lost_quant)/clients.count()) * 100),
                'total_clients': clients.count()
            }
    return render_to_response(template,
        context, context_instance=RequestContext(request))



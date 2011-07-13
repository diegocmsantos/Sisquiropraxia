# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.translation import gettext as __
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from apps.profiles.models import Doctor
from apps.service.models import TableService

@login_required
def index(request, template="site_base.html"):
    context = {}
    try:
        user_profile = request.user.get_profile()
    except:
        user_profile = None
    if user_profile:
        if user_profile.user_type == '1':
            doctor = Doctor.objects.get(user=request.user)
            total = doctor.current_month_comission()
            clients = doctor.clients.all()
            clients_count = clients.count()
            show_up_quant = [[].append(client) for client in clients if client.medical_appointment.all()].__len__()
            show_up_comission = doctor.show_up_comission()
            lost_quant = [[].append(client) for client in clients if not client.medical_appointment.all()].__len__()
            next_month_comission = doctor.next_month_comission()
            total_comission = doctor.total_comission()
            if clients_count == 0:
                clients_count = 1
            context = {
                'show_up_quant': show_up_quant,
                'show_up_comission': '%.2f' % show_up_comission,
                'show_up_percent': int((float(show_up_quant)/clients_count) * 100),
                'lost_quant': lost_quant,
                'lost_percent': int((float(lost_quant)/clients_count) * 100),
                
                'total_comission': '%.2f' % total_comission,
                'total_clients': clients.count(),
                
                'last_month_comission': '%.2f' % doctor.last_month_comission(),
                'last_month_quant_clients': doctor.last_month_quant_clients(),
                
                'current_month_quant_clients': clients_count,
                'current_month_comission': '%.2f' % total,
                
                'next_month_comission': '%.2f' % next_month_comission,
                'next_month_quant_clients': doctor.next_month_quant_clients(),
            }
    return render_to_response(template,
        context, context_instance=RequestContext(request))



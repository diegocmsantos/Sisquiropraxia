# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import gettext as __
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from forms import *
from apps.profiles.models import Client
from utils import html_email

import simplejson as json

# Views

@login_required
def doctor_make_appointment(request, client_id):
    return make_appointment(request, client_id, form_class=DoctorMakeAppointmentForm, template='make_appointment.html')
    
@login_required
def hostess_make_appointment(request, client_id):
    return make_appointment(request, client_id, form_class=HostessMakeAppointmentForm, template='make_appointment.html')
    
def make_appointment(request, client_id, form_class=DoctorMakeAppointmentForm, template='make_appointment.html'):
    client = get_object_or_404(Client, pk=client_id)
    context = {'title': 'Consulta'}
    context['client'] = client
    try:
        context['last_appointment'] = client.medical_appointment.latest('appointment_date').appointment_date
    except:
        context['last_appointment'] = 'Primeira consulta.'
    form = form_class()
    
    if request.POST:
        form = form_class(request.POST)
        if form.is_valid():
            form.save(client)
            form = form_class()
            messages.success(request,
                __('Consulta realizada com sucesso!'))
            context['css_message'] = 'message success'
        else:
            messages.error(request,
                __(u'Ocorreu um erro ao tentar salvar o perfil. Verifique os campos!'))
            context['css_message'] = 'message error'
    
    context['form'] = form
    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))
    
@login_required
def list_appointment_client(request, client_id, template="list_appointment_client.html"):
    client = get_object_or_404(Client, pk=client_id)
    context = {'title': 'Consultas de %s' % client.user.username.upper()}
    context['client'] = client
    
    evaluation = client.medical_appointment.filter(appointment_type=0)
    bed = client.medical_appointment.filter(appointment_type=1)
    quiro = client.medical_appointment.filter(appointment_type=2)
    
    context['diagnostic'] = evaluation[0].diagnostic
    context['appointment_date'] = evaluation[0].appointment_date
    context['bed_doc_advice'] = evaluation[0].section_times
    context['quiro_doc_advice'] = evaluation[1].section_times
    context['bed_sections'] = Section.objects.filter(medicalAppointment=bed)
    context['quiro_sections'] = Section.objects.filter(medicalAppointment=quiro)
    
    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))
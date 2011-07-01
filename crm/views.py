# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import gettext as __
from django.contrib import messages
from django.forms.models import model_to_dict
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

from forms import *
from utils import html_email

import simplejson as json

@login_required
def add_client(request, form_class=AddClientForm, template="add_client.html"):
    context = {'title': 'Paciente', 'active_client_sidemenu': 'current'}
    if request.method == 'POST':
        form = form_class(request.POST)

        if form.is_valid():
            user = request.user
            client = form.save()
            user_profile = request.user.get_profile()
            if user_profile.user_type == '1':
                doctor = Doctor.objects.get(user=user)
                doctor.clients.add(client)
                doctor.save()
            
            messages.success(request,
                __('Paciente \'%s\' criado com sucesso!') % (form.cleaned_data['name'],))
            form = form_class()
            context['css_message'] = 'message success'
        else:
            messages.error(request,
                __(u'Ocorreu um erro ao tentar salvar o perfil. Verifique os campos!'))
            context['css_message'] = 'message error'
    else:
        form = form_class()
    context['form'] = form
    return render_to_response(template,
                                context,
                                context_instance=RequestContext(request))
    
def add_client_doctor(request):
    return add_client(request, AddClientDoctorForm)
    
@login_required
def edit_client(request, client_id, form_class=AddClientForm, template="add_client.html"):
    client = get_object_or_404(Client, pk=client_id)
    # dictionary = model_to_dict(client, fields=[], exclude=[])
    dictionary = model_to_dict(client, fields=[field.name for field in client._meta.fields])
    context = {'title': 'Editar Paciente'}
    print dictionary
    if request.method == 'GET':
        form = form_class(dictionary)
        form.fill_client(client)
        form.fill_address(client.address)
        form.fill_phone(Phone.objects.filter(user=client.user))
    else:
        form = form_class()
        
    context['form'] = form
    return render_to_response(template,
                                context,
                                context_instance=RequestContext(request))
    
@login_required
def list_client(request, template='list_client.html'):
    context = {'title': 'Paciente', 'active_client_sidemenu': 'current'}
    user = request.user
    try:
        user_type = user.get_profile().user_type
        if user_type == '0':
            clients = Client.objects.all()
        elif user_type == '1':
            doctor = Doctor.objects.get(user=user)
            clients = doctor.clients.all()
        else:
            clients = Client.objects.all()
    except UserProfile.DoesNotExist:
        clients = Client.objects.all()
    
    result = []
    for client in clients:
        result.append([client, Phone.objects.filter(user=user)])
    context['clients'] = result
    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))
    
@login_required
def add_doctor(request, form_class=AddDoctorForm, template="add_doctor.html"):
    context = {'title': 'Médico'}
    if request.method == 'POST':
        form = form_class(request.POST)

        if form.is_valid():
            user, password = form.save()
            form = form_class()
            
            vars_dict = {'first_name': user.first_name, 'username': user.username, 'password': password}
            html_email('Cadastro no Sisquiropraxia', "add_doctor_email.html", vars_dict, 'no-reply@noreply.com', user.email)
            
            messages.success(request,
                __('Médico criado com sucesso!'))
            context['css_message'] = 'message success'
        else:
            messages.error(request,
                __(u'Ocorreu um erro ao tentar salvar o perfil. Verifique os campos!'))
            context['css_message'] = 'message error'
    else:
        form = form_class
    context['form'] = form
    return render_to_response(template,
                                context,
                                context_instance=RequestContext(request))
    
@login_required
def list_doctor(request, template='list_doctor.html'):
    context = {'title': 'Médicos', 'active_doctor_sidemenu': 'current'}
    doctors = Doctor.objects.all()
    context['doctors'] = doctors
    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))
    
@login_required
def add_hostess(request, form_class=AddHostessForm, template='add_hostess.html'):
    context = {'title': 'Recepcionista'}
    if request.method == 'POST':
        form = form_class(request.POST)

        if form.is_valid():
            hostess = form.save()
            form = form_class()
            
            messages.success(request,
                __('Recepcionista %s criado(a) com sucesso!' % (hostess.get_full_name,)))
            context['css_message'] = 'message success'
        else:
            messages.error(request,
                __(u'Ocorreu um erro ao tentar salvar o perfil. Verifique os campos!'))
            context['css_message'] = 'message error'
    else:
        form = form_class
    context['form'] = form
    return render_to_response(template,
                                context,
                                context_instance=RequestContext(request))
    
@login_required
def list_hostess(request, template='list_hostess.html'):
    context = {'title': 'Recepcionistas', 'active_hostess_sidemenu': 'current'}
    hostess = Hostess.objects.all()
    context['hostesses'] = hostess
    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))
    
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
    
@login_required
def calendar(request, template="calendar.html"):
    context = {}
    appointments = MedicalAppointment.objects.all()
    json_data = []
    for appointment in appointments:
        if appointment.appointment_type != 0:
            sections = Section.objects.filter(medicalAppointment=appointment)
            for section in sections:
                client = get_object_or_404(Client, medical_appointment=appointment.pk)
                dict = {
                    'title': '%s (%s)' % (client.user.username, appointment.appointment_type,),
                    'start': str(section.section_date),
                    'end': str(section.section_date + datetime.timedelta(minutes=30))
                    }
                json_data.append(dict)
    print json_data
    context['json_data'] = json_data
    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))
# -*- coding: utf-8 -*-

from django.db import transaction
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
@transaction.commit_on_success
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
@transaction.commit_on_success
def edit_client(request, client_id, form_class=AddClientForm, template="add_client.html"):
    client = get_object_or_404(Client, pk=client_id)
    dictionary = model_to_dict(client, fields=[field.name for field in client._meta.fields])
    context = {'title': 'Editar Paciente'}
    
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=client)
    
        if form.is_valid():
            form.save()
            messages.success(request,
                __('Paciente \'%s\' editado com sucesso!') % (form.cleaned_data['name'],))
            context['css_message'] = 'message success'
        else:
            messages.error(request,
                __(u'Ocorreu um erro ao tentar salvar o perfil. Verifique os campos!'))
            context['css_message'] = 'message error'
    else:
        form = form_class(instance=client)
        
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
@transaction.commit_on_success
def add_doctor(request, form_class=AddDoctorForm, template="add_doctor.html"):
    
    context = {'title': 'Parceiro'}
    if request.method == 'POST':
        form = form_class(request.POST)

        if form.is_valid():
            company_admin = request.user.companyadmin_set.all()[0]
            user, password = form.save(company_admin)
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
    context = {'title': 'Parceiros', 'active_doctor_sidemenu': 'current'}
    user = request.user
    if user.get_profile().user_type == '4':
        company_admin = user.companyadmin_set.all()[0]
        doctors = Doctor.objects.filter(company_admin=company_admin)
    elif user.is_superuser():
        doctors = Doctor.objects.all()
    context['doctors'] = doctors
    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))
    
@login_required
@transaction.commit_on_success
def add_hostess(request, form_class=AddHostessForm, template='add_hostess.html'):
    context = {'title': 'Recepcionista'}
    if request.method == 'POST':
        form = form_class(request.POST)

        if form.is_valid():
            company_admin = CompanyAdmin.objects.get(user=request.user)
            hostess = form.save(company_admin)
            
            messages.success(request,
                __('Recepcionista %s criado(a) com sucesso!' % (form.cleaned_data['first_name'],)))
            context['css_message'] = 'message success'
            form = form_class()
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
    company_admin = CompanyAdmin.objects.get(user=request.user)
    hostess = Hostess.objects.filter(company_admin=company_admin)
    context['hostesses'] = hostess
    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))

@login_required
@transaction.commit_on_success
def add_clinic(request, form_class=AddClinicForm, template='add_clinic.html'):
    context = {'title': 'Clínica'}
    if request.method == 'POST':
        form = form_class(request.POST)

        if form.is_valid():
            user = request.user
            clinic = form.save()
            
            messages.success(request,
                __(u'Clínica %s criada com sucesso!' % (form.cleaned_data['name'],)))
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
    
#@login_required
#def list_hostess(request, template='clinic_list.html'):
#    context = {'title': 'Clínica', 'active_clinic_sidemenu': 'current'}
#    clinics = Clinic.objects.all()
#    context['clinics'] = clinics
#    return render_to_response(template,
#                              context,
#                              context_instance=RequestContext(request))

@login_required
@transaction.commit_on_success
def add_employee(request, form_class=AddEmployeeForm, template='add_employee.html'):
    context = {'title': 'Funcionário'}
    if request.method == 'POST':
        form = form_class(request.user, request.POST)

        if form.is_valid():
            user = request.user
            employee = form.save()
            
            messages.success(request,
                __(u'Funcionário %s criado com sucesso!' % (form.cleaned_data['first_name'],)))
            context['css_message'] = 'message success'
            form = form_class(request.user)
        else:
            messages.error(request,
                __(u'Ocorreu um erro ao tentar salvar o perfil. Verifique os campos!'))
            context['css_message'] = 'message error'
    else:
        form = form_class(request.user)
    context['form'] = form
    return render_to_response(template,
                                context,
                                context_instance=RequestContext(request))
    
@login_required
def list_employee(request, template='employee_list.html'):
    context = {'title': 'Funcionários', 'active_employee_sidemenu': 'current'}
    employees = []
    for clinic in CompanyAdmin.objects.get(user=request.user).clinics.all():
        for employee in clinic.employee_set.all():
            employees.append(employee)
    context['employees'] = employees
    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))
# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import gettext as __
from django.contrib import messages
from django.forms.models import model_to_dict

from django.contrib.auth.decorators import login_required

from forms import *

@login_required
def add_client(request, form_class=AddClientForm, template="add_client.html"):
    context = {'title': 'Paciente'}
    if request.method == 'POST':
        form = form_class(request.POST)

        if form.is_valid():
            form.save()
            form = form_class()
            messages.success(request,
                __('Paciente criado com sucesso!'))
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
    
@login_required
def edit_client(request, client_id, form_class=AddClientForm, template="add_client.html"):
    client = get_object_or_404(Client, pk=client_id)
    # dictionary = model_to_dict(client, fields=[], exclude=[])
    dictionary = model_to_dict(client, fields=[field.name for field in client._meta.fields])
    context = {'title': 'Editar Paciente'}
    
    if request.method == 'GET':
        form = form_class(dictionary)
        form.fill_address(client.address)
        form.fill_phone(Phone.objects.filter(client=client))
    else:
        form = form_class()
        
    context['form'] = form
    return render_to_response(template,
                                context,
                                context_instance=RequestContext(request))
    
@login_required
def list_client(request, template='list_client.html'):
    context = {'title': 'Paciente'}
    clients = Client.objects.all()
    result = []
    for client in clients:
        result.append([client, Phone.objects.filter(client=client)])
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
            address = Address()
            address.street = form.cleaned_data['street']
            address.complement = form.cleaned_data['complement']
            address.neighborhood = form.cleaned_data['neighborhood']
            address.zip = form.cleaned_data['zip']
            address.save()
            
            if form.cleaned_data['agency']:
                billing_account = BillingAccount()
                billing_account.agency = form.cleaned_data['agency']
                billing_account.account_number = form.cleaned_data['account_number']
                billing_account.bank = form.cleaned_data['bank']
                billing_account.account_type = form.cleaned_data['account_type']
                billing_account.save()
            
            phone = Phone()
            if form.cleaned_data['phone_home']:
                phone.phone_number = form.cleaned_data['phone_home']
                phone.phone_type = Phone.PHONE_TYPE[0][0]
                phone.save()
            
            if form.cleaned_data['phone_businness']:
                phone.phone_number = form.cleaned_data['phone_businness']
                phone.phone_type = Phone.PHONE_TYPE[1][0]
                phone.save()
            
            if form.cleaned_data['phone_mobile']:
                phone.phone_number = form.cleaned_data['phone_mobile']
                phone.phone_type = Phone.PHONE_TYPE[2][0]
                phone.save()
            
            doctor = Doctor()
            doctor.name = form.cleaned_data['name']
            doctor.cnpf = form.cleaned_data['cnpf']
            doctor.email = form.cleaned_data['email']
            doctor.birthday = form.cleaned_data['birthday']
            doctor.address = address
            doctor.billing_account = billing_account
            doctor.phone = phone
            doctor.save()
            
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
    context = {'title': 'Médico'}
    doctors = Doctor.objects.all()
    context['doctors'] = doctors
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
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
def add_service(request, form_class=AddServiceForm, template="add_service.html"):
    context = {'title': 'Paciente', 'active_service_sidemenu': 'current'}
    if request.method == 'POST':
        form = form_class(request.POST)

        if form.is_valid():
            try:
                service = form.save()
                messages.success(request,
                    __(u'Serviço \'%s\' criado com sucesso!') % (form.cleaned_data['description'],))
                form = form_class()
                context['css_message'] = 'message success'
            except:
                messages.success(request,__('Erro ao tentar salvar serviço!'))
                form = form_class()
                context['css_message'] = 'message error'
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
def list_service(request, template="list_service.html"):
    context = {'title': 'Serviço', 'active_service_sidemenu': 'current'}
    services = Service.objects.all()
    context['services'] = services
    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))
    
@login_required
def add_table(request, form_class=AddTableForm, template="add_table.html"):
    context = {'title': 'Tabela', 'active_table_sidemenu': 'current'}
    if request.method == 'POST':
        form = form_class(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request,
                __('Tabela \'%s\' criada com sucesso!') % (form.cleaned_data['description'],))
            form = form_class()
            context['css_message'] = 'message success'
        else:
            messages.error(request,
                __(u'Ocorreu um erro. Verifique os campos!'))
            context['css_message'] = 'message error'
    else:
        form = form_class()
    context['form'] = form
    return render_to_response(template,
                                context,
                                context_instance=RequestContext(request))
    
@login_required
def list_table(request, template="list_table.html"):
    context = {'title': 'Tabela', 'active_table_sidemenu': 'current'}
    tables = Table.objects.all()
    context['tables'] = tables
    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))
    

# Table Service
@login_required
def add_table_service(request, form_class=AddTableServiceForm, template="add_table_service.html"):
    context = {'title': 'Tabela/Serviço', 'active_table_service_sidemenu': 'current'}
    if request.method == 'POST':
        form = form_class(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request,
                __('Tabela e Serviço associados com sucesso!') )
            form = form_class()
            context['css_message'] = 'message success'
        else:
            messages.error(request,
                __(u'Ocorreu um erro. Verifique os campos!'))
            context['css_message'] = 'message error'
    else:
        form = form_class()
    context['form'] = form
    return render_to_response(template,
                                context,
                                context_instance=RequestContext(request))
    
@login_required
def list_table_service(request, template="list_table_service.html"):
    context = {'title': 'Tabela/Serviço', 'active_table_service_sidemenu': 'current'}
    results = TableService.objects.all()
    context['results'] = results
    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))
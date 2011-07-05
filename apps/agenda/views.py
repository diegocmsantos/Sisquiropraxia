# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import gettext as __
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from apps.appointments.models import MedicalAppointment, Section

from utils import html_email

import simplejson as json

# Views

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
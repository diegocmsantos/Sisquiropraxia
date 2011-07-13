# -*- coding: utf-8 -*-

from django import forms

from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.translation import gettext_lazy as _, gettext as __

import datetime
from utils import generate_password

from apps.appointments.models import *
from apps.service.models import TableService

class DoctorMakeAppointmentForm(forms.Form):
    diagnostic = forms.CharField(label=_('Diagnóstico'), widget=forms.Textarea())
    bed_times = forms.IntegerField(label=_('Seções de Cama Termo'), required=False)
    quiro_times = forms.IntegerField(label=_('Seções de Quiropraxia'), required=False)
    
    def save(self, client):
        data = self.cleaned_data
        _save_appointment(data['bed_times'], client, \
            MedicalAppointment.APPOINTMENT_TYPE[1][0], data['diagnostic'])
        _save_appointment(data['quiro_times'], client, \
            MedicalAppointment.APPOINTMENT_TYPE[1][0], data['diagnostic'])
    
class HostessMakeAppointmentForm(forms.Form):
    def __init__(self, table_services, *args, **kwargs):
        super(HostessMakeAppointmentForm, self).__init__(*args, **kwargs)
        self.fields['service'].queryset = table_services
    SECTIONS_FREQUENCY = (
        ('1', _('diariamente')),
        ('2', _('2 em 2 dias')),
        ('3', _('3 em 3 dias')),
        ('7', _('semanalmente')),
        ('30', _('mensalmente')),
    )
    service = forms.ModelChoiceField(label=_('Serviço'), \
        queryset=None)
    quantity = forms.IntegerField(label=_('Quantidade'), initial='1')
    
    payment_type = forms.ChoiceField(label=_('Tipo de pagamento'), choices=PaymentWay.PAYMENT_TYPE)
    card_payment_type = forms.ChoiceField(label=_('Tipo de cartão de crédito'), \
        choices=PaymentWay.CARD_PAYMENT_TYPE, required=False)
    check_number = forms.IntegerField(label=_('Número do cheque'), required=False)
    check_date = forms.DateField(label=_('Data do cheque'), required=False)
    quant_parcels = forms.IntegerField(label=_('Quantidade de parcelas'), required=False)
    total_payment = forms.DecimalField(label=_('Valor'), max_digits=10, \
        decimal_places=2, required=False, widget = forms.TextInput(attrs={'readonly':'readonly'}))
    first_section = forms.DateTimeField(label=_('Primeira seção'))
    sections_frequency = forms.ChoiceField(label=_('Frequência'), choices=SECTIONS_FREQUENCY)
    
    def clean_first_section(self):
        data = self.cleaned_data['first_section']
        #if Section.objects.filter(section_date=data).count() > 1:
        #    raise forms.ValidationError(_("Conflito de horário. Por favor, tente outra data."))

        # Always return the cleaned data, whether you have changed it or
        # not.
        return data
    
    def save(self, client):
        data = self.cleaned_data
        
        # Verificando tipo de pagamento
        payment_way = PaymentWay()
        if data['payment_type'] == '0':
            # Money
            payment_way.payment_type = data['payment_type']
            payment_way.total_payment = data['total_payment']
        elif data['payment_type'] == '1':
            # Check
            check_quant = data['total_payment'].count
            count = 0
            while count <= check_quant:
                payment_way.payment_type = data['payment_type']
                payment_way.total_payment = data['total_payment'][count]
                payment_way.quant_parcels = check_quant
                payment_way.check_number = data['check_number'][count]
                payment_way.check_date = data['check_date'][count]
        elif data['payment_type'] == '2':
            payment_way.payment_type = data['payment_type']
            payment_way.card_payment_type = data['card_payment_type']
            payment_way.total_payment = data['total_payment']
            if payment_way.card_payment_type == '0':
                payment_way.quant_parcels = 1
            elif payment_way.card_payment_type == '1':
                payment_way.quant_parcels = data['quant_parcels']
        payment_way.save()
        
        # Saving bed and quiro appointment
        _save_appointment(data['first_section'], data['sections_frequency'], \
            data['quantity'], client, data['service'], payment_way=payment_way)
        
def _schedule(start_date, quantity, frequency, appointment, client):
    for i in range(0, quantity):
        appointment.id = None
        if i == 0:
            appointment.appointment_date = (start_date)
        else:
            appointment.appointment_date = (start_date + \
                datetime.timedelta(days=int(frequency)))
        start_date = appointment.appointment_date
        appointment.save()
        
        # Saving medical appointment in client
        client.medical_appointment.add(appointment)
        client.save()
        
def _save_appointment(start_date, frequency, quantity, client, \
        service, diagnostic=None, payment_way=None):
    # Getting Today
    today = datetime.datetime.today()
    
    # Saving appointment
    appointment = MedicalAppointment()
    appointment.diagnostic = diagnostic
    appointment.quantity = quantity
    if payment_way and service:
        appointment.table_service = service
        appointment.payment_way = payment_way
    _schedule(start_date, quantity, frequency, appointment, client)
    
    
# -*- coding: utf-8 -*-

from django.db import models

from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _, gettext as __
from django.core.urlresolvers import reverse
from django.conf import settings
import datetime

from apps.payments.models import PaymentWay
from apps.service.models import TableService

# Models

class MedicalAppointment(models.Model):
    appointment_date = models.DateField(
        _('Data Consulta')
    )
    diagnostic = models.CharField(
        _('Diagnóstico'),
        max_length=255,
        blank=True,
        null=True
    )
    quantity = models.IntegerField(_('Quantidade'), blank=True, null=True)
    service = models.ForeignKey(TableService)
    payment_way = models.ManyToManyField(PaymentWay, related_name='Forma de pagamento', \
        blank=True, null=True)
    
    class Meta:
        verbose_name = __('Consulta')
        verbose_name_plural = __('Consultas')
    
    def __unicode__(self):
        return self.appointment_type
    
    def get_absolute_url(self):
        return reverse('crm.views.medical_appointment',
                kwargs={'id': self.id})
        
class Section(models.Model):
    medicalAppointment = models.ForeignKey('MedicalAppointment')
    section_date = models.DateTimeField(_('Data Seção'))
    section_done = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = __('Seção')
        verbose_name_plural = __('Seções')
        ordering = ('-section_date',)
    
    def __unicode__(self):
        return self.medicalAppointment.appointment_type
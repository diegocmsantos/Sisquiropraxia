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
    quantity = models.IntegerField(_('Quantidade'))
    table_service = models.ForeignKey(TableService)
    payment_way = models.ForeignKey(PaymentWay, related_name='Forma de pagamento',)
    appointment_date = models.DateTimeField(_('Data Seção'))
    appointment_done = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = __('Consulta')
        verbose_name_plural = __('Consultas')
    
    def __unicode__(self):
        return self.table_service.service.description
    
    def get_absolute_url(self):
        return reverse('crm.views.medical_appointment',
                kwargs={'id': self.id})
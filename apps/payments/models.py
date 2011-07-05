# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext_lazy as _, gettext as __
from django.core.urlresolvers import reverse
from django.conf import settings
import datetime

# Models

class PaymentWay(models.Model):
    PAYMENT_TYPE = (
        ('', _('----------')),
        ('0', _('Dinheiro')),
        ('1', _('Cheque')),
        ('2', _('Cartão')),
    )
    CARD_PAYMENT_TYPE = (
        ('', _('----------')),
        ('0', _('Débito')),
        ('1', _('Crédito')),
    )
    total_payment = models.DecimalField(_('Valor'), max_digits=10, decimal_places=2)
    quant_parcels = models.IntegerField(_('Quantidade de parcelas'), blank=True, \
        null=True)
    check_number = models.IntegerField(_('Número'), blank=True, null=True)
    check_date = models.DateField(_('Data'), blank=True, null=True)
    payment_type = models.CharField(_('Tipo de pagamento'), max_length=1, \
        choices=PAYMENT_TYPE)
    card_payment_type = models.CharField(_('Tipo de cartão de crédito'), \
        max_length=1, choices=CARD_PAYMENT_TYPE, blank=True, null=True)
    paid = models.BooleanField(default=False)
    
    def __unicode__(self):
        return '%s no valor de %s' % (self.payment_type, self.total_payment,)
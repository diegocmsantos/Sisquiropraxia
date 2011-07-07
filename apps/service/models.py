# -*- coding: utf-8 -*-

from django.db import models

from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _, gettext as __
from django.core.urlresolvers import reverse
from django.conf import settings
import datetime

# Models

class Service(models.Model):
    code = models.CharField(
        _('Código'),
        max_length=15
    )
    description = models.CharField(
        _('Descrição'),
        max_length=255
    )
    
    def __unicode__(self):
        return self.description
    
class Table(models.Model):
    description = models.CharField(
        _('Descrição'),
        max_length=255
    )
    def __unicode__(self):
        return self.description
    
class TableService(models.Model):
    table = models.ForeignKey(
        Table
    )
    service = models.ForeignKey(
        Service
    )
    price = models.DecimalField(
        _('Preço'),
        max_digits=8,
        decimal_places=2
    )
    
    def __unicode__(self):
        return u'tabela %s --> serviço %s --> preço %s ' \
        % (self.table.description, self.service.description, self.price)
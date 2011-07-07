# -*- coding: utf-8 -*-

from django.db import models

from django.contrib.localflavor.br.br_states import STATE_CHOICES
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _, gettext as __
from django.core.urlresolvers import reverse
from django.conf import settings
import datetime

from apps.appointments.models import MedicalAppointment, Section
from apps.service.models import Table, TableService

# Models

class Clinic(models.Model):
    name = models.CharField(_('Nome'), max_length=100)
    cnpj = models.CharField(_('CNPJ'), max_length=14)
    address = models.ForeignKey('Address')
    
    class Meta:
        verbose_name = __('Clínica')
        verbose_name_plural = __('Clínicas')
    
    def __unicode__(self):
        return self.name

class Person(models.Model):
    user = models.ForeignKey(User)
    cnpf = models.CharField(_('CPF/CNPJ'), max_length=18)
    birthday = models.DateField(_('Nascimento'), blank=True, null=True)
    address = models.ForeignKey('Address', blank=True, null=True)
    billing_account = models.ForeignKey('BillingAccount', \
                                        blank=True, null=True)
        
    def idade(self):
        return (datetime.date.today() - self.birthday).days / 365
        
    class Meta:
        abstract = True
        
class CompanyAdmin(Person):
    clinics = models.ManyToManyField(Clinic)
    
    class Meta:
        verbose_name = __('Administrador')
        verbose_name_plural = __('Administradores')
    
    def __unicode__(self):
        return self.user.username

class Employees(Person):
    clinic = models.ForeignKey(Clinic)
    
    class Meta:
        verbose_name = __('Funcionário')
        verbose_name_plural = __('Funcionários')
    
    def __unicode__(self):
        return self.clinic.name
        
class DoctorClientsManager(models.Manager):
    def get_query_set(self):
        return super(DoctorClientsManager, self).get_query_set().filter(pk=self.pk)

class Doctor(Person):
    crm = models.CharField(max_length=50)
    clients = models.ManyToManyField('Client')
    table = models.ForeignKey(Table)
    objects = models.Manager() # The default manager.
    doctor_clients = DoctorClientsManager() # Clients of doctor Manager
    
    def table_services(self):
        return TableService.objects.filter(table=self.table)
    
    class Meta:
        verbose_name = __('Médico')
        verbose_name_plural = __('Médicos')
    
    def __unicode__(self):
        return self.crm
    
    def get_absolute_url(self):
        return reverse('crm.views.doctor',
                kwargs={'id': self.id})
        
class Client(Person):
    medical_appointment = models.ManyToManyField(MedicalAppointment)
    clients = models.ManyToManyField('self')
    
    def last_appointment(self):
        result = None
        try:
            result = self.medical_appointment.latest('appointment_date')
        except:
            pass
        return result
    
    def has_evaluation(self):
        return self.medical_appointment.filter(appointment_type=0)
    
    def can_evaluation(self):
        last_appointment = Section.objects.filter(
            medicalAppointment=self.last_appointment()
        )
        if last_appointment:
            return last_appointment.filter(section_done=False)
        return True
        
    def appointment_cost(self, services_dict=None):
        total = 0
        if services_dict:
            doctor = Doctor.objects.get(clients=self)
            table_services = doctor.table_services()
            for service in services_dict:
                if service['service_id']:
                    price = table_services.get(service__id=service['service_id']).price
                    if service['quant']:
                        try:
                            quant = int(service['quant'])
                        except ValueError:
                            quant = 1
                        total += (price * quant)
        return total
    
    class Meta:
        verbose_name = __('Paciente')
        verbose_name_plural = __('Pacientes')
    
    def __unicode__(self):
        return 'paciente'
    
    def get_absolute_url(self):
        return reverse('crm.views.client',
                kwargs={'id': self.id})
        
class Hostess(models.Model):
    user = models.ForeignKey(User)
    
class Address(models.Model):
    street = models.CharField(_('Rua'), max_length=200)
    complement = models.CharField(_('Complemento'), max_length=100, blank=True)
    neighborhood = models.CharField(_('Bairro'), max_length=100)
    zip = models.CharField(_('CEP'), max_length=10)
    state = models.CharField(_('Estado'), max_length=2, choices=STATE_CHOICES)
    city = models.CharField(_('Cidade'), max_length=200)
    
    class Meta:
        verbose_name = __('Endereço')
        verbose_name_plural = __('Endereços')
        ordering = ('street', )
    
    def __unicode__(self):
        return self.street
    
    def get_absolute_url(self):
        return reverse('crm.views.address',
                kwargs={'id': self.id})
        
class BillingAccount(models.Model):
    ACCOUNT_TYPE_CHOICES = (
        ('0', _('Conta Corrente')),
        ('1', _('Poupança')),
    )
    agency = models.CharField(_('Agência'), max_length=10, null=True, blank=True)
    account_number = models.CharField(_('Conta Corrente'), max_length=20, null=True, blank=True)
    bank = models.ForeignKey('Bank', related_name=_('Banco'), null=True, blank=True)
    account_type = models.CharField(max_length=1, choices=ACCOUNT_TYPE_CHOICES, null=True, blank=True)
    
    class Meta:
        verbose_name = __('Conta Bancária')
        verbose_name_plural = __('Contas Bancária')
    
    def __unicode__(self):
        return self.account_number
    
    def get_absolute_url(self):
        return reverse('crm.views.billing_account',
                kwargs={'id': self.id})
    
class Bank(models.Model):
    bank_code = models.IntegerField(_('Código do Banco'))
    name = models.CharField(_('Banco'), max_length=100)
    
    class Meta:
        verbose_name = __('Banco')
        verbose_name_plural = __('Bancos')
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('crm.views.bank',
                kwargs={'id': self.id})
    
class Phone(models.Model):
    PHONE_TYPE = (
        ('', _('----------')),
        ('0', _('Residencial')),
        ('1', _('Comercial')),
        ('2', _('Celular')),
    )
    user = models.ForeignKey(User)
    phone_type = models.CharField(max_length=1, choices=PHONE_TYPE)
    phone_number = models.CharField(_('Telefone'), max_length=14)
    
    class Meta:
        verbose_name = __('Telefone')
        verbose_name_plural = __('Telefones')
    
    def __unicode__(self):
        return self.phone_number
    
    def get_absolute_url(self):
        return reverse('crm.views.phone',
                kwargs={'id': self.id})
        
class UserProfile(models.Model):
    USER_TYPE = (
        ('', _('------------')),
        ('0', _('Administrador Master')),
        ('1', _('Parceiro Indicador')),
        ('2', _('Cliente')),
        ('3', _('Recepcionista')),
        ('4', _('Administrador')),
        ('5', _('Funcionário')),
    )
    user = models.ForeignKey(User)
    user_type = models.CharField(max_length=1, choices=USER_TYPE)
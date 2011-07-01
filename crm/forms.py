# -*- coding: utf-8 -*-

from django import forms

from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.translation import gettext_lazy as _, gettext as __

import datetime
from utils import generate_password

from crm.models import *

class AddClientForm(forms.Form):
    name = forms.CharField(label=_('Nome'))
    cnpf = forms.CharField(label=_('CPF/CNPJ'))
    email = forms.EmailField()
    birthday = forms.DateField(label=_('Nascimento'), required=False)
    
    street = forms.CharField(label=_('Rua'), required=False)
    complement = forms.CharField(label=_('Complemento'), required=False)
    neighborhood = forms.CharField(label=_('Bairro'), required=False)
    zip = forms.CharField(label=_('CEP'), required=False)
    
    agency = forms.CharField(label=_('Agência'), required=False)
    account_number = forms.CharField(label=_('Conta Corrente'), required=False)
    bank = forms.ModelChoiceField(label=_('Banco'), queryset=Bank.objects.all(), required=False)
    account_type = forms.ChoiceField(label=_('Tipo de conta'), choices=BillingAccount.ACCOUNT_TYPE_CHOICES, required=False)
    
    phone_home = forms.CharField(label=_('Telefone Residencial'), required=False)
    phone_businness = forms.CharField(label=_('Telefone Comercial'), required=False)
    phone_mobile = forms.CharField(label=_('Telefone Celular'))
    
    def save(self):
        if self.cleaned_data:
            address = Address()
            address.street = self.cleaned_data['street']
            address.complement = self.cleaned_data['complement']
            address.neighborhood = self.cleaned_data['neighborhood']
            address.zip = self.cleaned_data['zip']
            address.save()
            
            if self.cleaned_data['agency']:
                billing_account = BillingAccount()
                billing_account.agency = self.cleaned_data['agency']
                billing_account.account_number = self.cleaned_data['account_number']
                billing_account.bank = self.cleaned_data['bank']
                billing_account.account_type = self.cleaned_data['account_type']
                billing_account.save()
            
            # Creating User
            first_name = self.cleaned_data['name']
            email = self.cleaned_data['email']
            password = generate_password()
            user = User.objects.create_user(first_name, email, password)
            
            person = Client()
            person.user = user
            person.cnpf = self.cleaned_data['cnpf']
            person.birthday = self.cleaned_data['birthday']
            person.address = address
            if self.cleaned_data['agency']:
                person.billing_account = billing_account
            person.save()
            
            if self.cleaned_data['phone_mobile']:
                phone = Phone()
                phone.user = user
                phone.phone_number = self.cleaned_data['phone_mobile']
                phone.phone_type = Phone.PHONE_TYPE[2][0]
                phone.save()
            
            if self.cleaned_data['phone_home']:
                phone = Phone()
                phone.user = user
                phone.phone_number = self.cleaned_data['phone_home']
                phone.phone_type = Phone.PHONE_TYPE[3][0]
                phone.save()
                
            if self.cleaned_data['phone_businness']:
                phone = Phone()
                phone.user = user
                phone.phone_number = self.cleaned_data['phone_businness']
                phone.phone_type = Phone.PHONE_TYPE[1][0]
                phone.save()
                
            return person
        
    def fill_client(self, client):
        if client:
            self.data['name'] = client.user.username
            self.data['email'] = client.user.email

    def fill_address(self, address):
        if address:
            self.data['street'] = address.street
            self.data['complement'] = address.complement
            self.data['neighborhood'] = address.neighborhood
            self.data['zip'] = address.zip
        
    def fill_phone(self, phones):
        for phone in phones:
            if phone.phone_type == '0':
                self.data['phone_home'] = phone.phone_number
            elif phone.phone_type == '1':
                self.data['phone_businness'] = phone.phone_number
            elif phone.phone_type == '2':
                self.data['phone_mobile'] = phone.phone_number
                
class AddClientDoctorForm(forms.Form):
    name = forms.CharField(label=_('Nome'))
    cnpf = forms.CharField(label=_('CPF/CNPJ'))
    email = forms.EmailField(required=False)
    
    def save(self):
        if self.cleaned_data:
            # Creating User
            first_name = self.cleaned_data['name']
            email = self.cleaned_data.get('email', None)
            password = generate_password()
            user = User.objects.create_user(first_name, email, password)
            
            person = Client()
            person.user = user
            person.cnpf = self.cleaned_data['cnpf']
            person.save()
            
            return person
        
class AddDoctorForm(forms.Form):
    name = forms.CharField(label=_('Nome'))
    cnpf = forms.CharField(label=_('CPF/CNPJ'))
    crm = forms.CharField(label=_('CRM'))
    email = forms.EmailField()
    birthday = forms.DateField(label=_('Nascimento'))
    
    street = forms.CharField(label=_('Rua'))
    complement = forms.CharField(label=_('Complemento'), required=False)
    neighborhood = forms.CharField(label=_('Bairro'))
    zip = forms.CharField(label=_('CEP'))
    
    agency = forms.CharField(label=_('Agência'), required=False)
    account_number = forms.CharField(label=_('Conta Corrente'), required=False)
    bank = forms.ModelChoiceField(label=_('Banco'), queryset=Bank.objects.all(), required=False)
    account_type = forms.ChoiceField(label=_('Tipo de conta'), choices=BillingAccount.ACCOUNT_TYPE_CHOICES, required=False)
    
    phone_home = forms.CharField(label=_('Telefone Residencial'), required=False)
    phone_businness = forms.CharField(label=_('Telefone Comercial'), required=False)
    phone_mobile = forms.CharField(label=_('Telefone Celular'))

    def save(self):
        if self.cleaned_data:
            address = Address()
            address.street = self.cleaned_data['street']
            address.complement = self.cleaned_data['complement']
            address.neighborhood = self.cleaned_data['neighborhood']
            address.zip = self.cleaned_data['zip']
            address.save()
            
            if self.cleaned_data['agency']:
                billing_account = BillingAccount()
                billing_account.agency = self.cleaned_data['agency']
                billing_account.account_number = self.cleaned_data['account_number']
                billing_account.bank = self.cleaned_data['bank']
                billing_account.account_type = self.cleaned_data['account_type']
                billing_account.save()
            
            # Creating User
            first_name = self.cleaned_data['name']
            username = ''.join(first_name.lower().split())
            email = self.cleaned_data['email']
            password = generate_password()
            user = User.objects.create_user(username, email, password)
            
            # UserProfile
            user_profile = UserProfile()
            user_profile.user = user
            user_profile.user_type = 1
            user_profile.save()
            
            # Doctor
            person = Doctor()
            person.user = user
            person.cnpf = self.cleaned_data['cnpf']
            person.crm = self.cleaned_data['crm']
            person.birthday = self.cleaned_data['birthday']
            person.address = address
            if self.cleaned_data['agency']:
                person.billing_account = billing_account
            person.save()
            
            if self.cleaned_data['phone_mobile']:
                phone = Phone()
                phone.user = user
                phone.phone_number = self.cleaned_data['phone_mobile']
                phone.phone_type = Phone.PHONE_TYPE[2][0]
                phone.save()
            
            if self.cleaned_data['phone_home']:
                phone = Phone()
                phone.user = user
                phone.phone_number = self.cleaned_data['phone_home']
                phone.phone_type = Phone.PHONE_TYPE[3][0]
                phone.save()
                
            if self.cleaned_data['phone_businness']:
                phone = Phone()
                phone.user = user
                phone.phone_number = self.cleaned_data['phone_businness']
                phone.phone_type = Phone.PHONE_TYPE[1][0]
                phone.save()
            
            return user, password

    def fill_address(self, address):
        self.data['street'] = address.street
        self.data['complement'] = address.complement
        self.data['neighborhood'] = address.neighborhood
        self.data['zip'] = address.zip
        
    def fill_phone(self, phones):
        for phone in phones:
            if phone.phone_type == '0':
                self.data['phone_home'] = phone.phone_number
            elif phone.phone_type == '1':
                self.data['phone_businness'] = phone.phone_number
            elif phone.phone_type == '2':
                self.data['phone_mobile'] = phone.phone_number
                
class AddHostessForm(forms.Form):
    first_name = forms.CharField(label=_('Nome'), help_text='30 caracteres ou menos. Somente letras, dígitos e @/./+/-/_.')
    last_name = forms.CharField(label=_('Sobrenome'))
    email = forms.EmailField(help_text="ex.: usuario@gmail.com")
    username = forms.CharField(label=_('Usuário'))
    password = forms.CharField(label=_('Senha'), widget=forms.PasswordInput)
    confirm_password = forms.CharField(label=_('Confirmar senha'), widget=forms.PasswordInput, help_text="repita a mesma senha")
    
    def save(self):
        if self.cleaned_data:
            username = self.cleaned_data['username']
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            
            try:
                # User
                user = User.objects.create_user(username, email, password)
                user.first_name = self.cleaned_data['first_name']
                user.last_name = self.cleaned_data['last_name']
                user.save()
                
                # UserProfile
                user_profile = UserProfile()
                user_profile.user = user
                user_profile.user_type = 3
                user_profile.save()
            except:
                pass
            
            return user
    
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
    SECTIONS_FREQUENCY = (
        ('1', _('diariamente')),
        ('2', _('2 em 2 dias')),
        ('3', _('3 em 3 dias')),
        ('7', _('semanalmente')),
        ('30', _('mensalmente')),
    )
    bed_times = forms.IntegerField(label=_('Seções de Cama Termo'))
    quiro_times = forms.IntegerField(label=_('Seções de Quiropraxia'))
    
    payment_type = forms.ChoiceField(label=_('Tipo de pagamento'), choices=PaymentWay.PAYMENT_TYPE)
    card_payment_type = forms.ChoiceField(label=_('Tipo de cartão de crédito'), \
        choices=PaymentWay.CARD_PAYMENT_TYPE, required=False)
    check_number = forms.IntegerField(label=_('Número do cheque'), required=False)
    check_date = forms.DateField(label=_('Data do cheque'), required=False)
    quant_parcels = forms.IntegerField(label=_('Quantidade de parcelas'), required=False)
    total_payment = forms.DecimalField(label=_('Valor'), max_digits=10, \
        decimal_places=2, required=False)
    first_section = forms.DateTimeField(label=_('Primeira seção'))
    sections_frequency = forms.ChoiceField(label=_('Frequência'), choices=SECTIONS_FREQUENCY)
    
    def clean_first_section(self):
        data = self.cleaned_data['first_section']
        print data
        print 'quant sections %s' % (Section.objects.filter(section_date=data).count(),)
        if Section.objects.filter(section_date=data).count() > 1:
            raise forms.ValidationError(_("Conflito de horário. Por favor, tente outra data."))

        # Always return the cleaned data, whether you have changed it or
        # not.
        return data
    
    def save_sections(self, bed_appointment, quiro_appointment):
        data = self.cleaned_data
        _schedule(data['first_section'], data['bed_times'], data['sections_frequency'], bed_appointment)
        _schedule(data['first_section'], data['quiro_times'], data['sections_frequency'], quiro_appointment)
    
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
        bed_appointment = _save_appointment(data['bed_times'], client, \
            MedicalAppointment.APPOINTMENT_TYPE[2][0], payment_way=payment_way)
        quiro_appointment = _save_appointment(data['quiro_times'], client, \
            MedicalAppointment.APPOINTMENT_TYPE[3][0], payment_way=payment_way)
        
        # Saving bed and quiro sections
        self.save_sections(bed_appointment, quiro_appointment)
        
def _schedule(start_date, no_section, frequency, appointment):
    for i in range(0, no_section):
            section = Section()
            section.medicalAppointment = appointment
            if i == 0:
                section.section_date = (start_date)
            else:
                section.section_date = (start_date + \
                    datetime.timedelta(days=int(frequency)))
            start_date = section.section_date
            section.save()
        
def _save_appointment(section_times, client, appointment_type, diagnostic=None, \
        payment_way=None):
    today = datetime.datetime.today()
    # Saving appointment
    appointment = MedicalAppointment()
    appointment.appointment_date = today
    appointment.diagnostic = diagnostic
    appointment.section_times = section_times
    appointment.appointment_type = appointment_type
    appointment.save()
    if payment_way:
        appointment.payment_way.add(payment_way)
    appointment.save()
    # Saving medical appointment in client
    client.medical_appointment.add(appointment)
    client.save()
    return appointment
        
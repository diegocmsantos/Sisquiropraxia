# -*- coding: utf-8 -*-

from django import forms

from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.translation import gettext_lazy as _, gettext as __

import datetime
from utils import generate_password

from apps.profiles.models import *

class AddClientForm(forms.ModelForm):
    name = forms.CharField(label=_('Nome'))
    cnpf = forms.CharField(label=_('CPF'))
    email = forms.EmailField()
    birthday = forms.DateField(label=_('Nascimento'), input_formats=['%d/%m/%Y'], required=False)
    
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

    class Meta:
        model = Client
        exclude = ('user', 'address', 'billing_account', 'medical_appointment', \
            'clients',)
        
    def __init__(self, *args, **kwargs):
        super(AddClientForm, self).__init__(*args, **kwargs)

        self.fields['name'].initial = self.instance.user.username
        self.fields['email'].initial = self.instance.user.email

        if self.instance.address:
            self.fields['street'].initial = self.instance.address.street
            self.fields['complement'].initial = self.instance.address.complement
            self.fields['neighborhood'].initial = self.instance.address.neighborhood
            self.fields['zip'].initial = self.instance.address.zip
            
        if self.instance.billing_account:
            self.fields['agency'].initial = self.instance.billing_account.agency
            self.fields['account_number'].initial = self.instance.billing_account.account_number
            self.fields['bank'].initial = self.instance.billing_account.bank
            self.fields['account_type'].initial = self.instance.billing_account.account_type

    def save(self, *args, **kwargs):
        print self.instance.user.first_name
        if self.cleaned_data['name']:
            self.instance.user.first_name = self.cleaned_data['name']
            
        if self.cleaned_data['email']:
            self.instance.user.email = self.cleaned_data['email']
        
        self.instance.user.save()
        
        if self.cleaned_data:
            address = Address()
            if self.instance.address:
                address.id = self.instance.address.id
            address.street = self.cleaned_data.get('street','')
            address.complement = self.cleaned_data.get('complement', '')
            address.neighborhood = self.cleaned_data.get('neighborhood', '')
            address.zip = self.cleaned_data.get('zip', '')
            address.save()
            self.instance.address = address
            self.instance.save()
        
        if self.cleaned_data:
            billing_account = BillingAccount()
            if self.instance.billing_account:
                billing_account.id = self.instance.billing_account.id
            billing_account.agency = self.cleaned_data['agency']
            billing_account.account_number = self.cleaned_data['account_number']
            billing_account.bank = self.cleaned_data['bank']
            billing_account.account_type = self.cleaned_data['account_type']
            billing_account.save()
            self.instance.billing_account = billing_account
            self.instance.save()
            
        return super(AddClientForm, self).save(*args, **kwargs)
    
    def save_old(self):
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
            password = User.objects.make_random_password(length=8, \
                allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
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
    
    table = forms.ModelChoiceField(label=_('Tabela de preço'), queryset=Table.objects.all())

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
            password = User.objects.make_random_password(length=8, \
                allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
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
            person.table = self.cleaned_data['table']
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
    first_name = forms.CharField(label=_('Nome'), help_text=_('30 caracteres ou menos. Somente letras, dígitos e @/./+/-/_.'))
    last_name = forms.CharField(label=_('Sobrenome'))
    email = forms.EmailField(help_text=_("ex.: usuario@gmail.com"))
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
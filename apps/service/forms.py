# -*- coding: utf-8 -*-

from django import forms

from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.translation import gettext_lazy as _, gettext as __

import datetime
from utils import generate_password

from apps.service.models import *

# Service
class AddServiceForm(forms.ModelForm):
    
    class Meta:
        model = Service


# Table
class AddTableForm(forms.ModelForm):
    
    class Meta:
        model = Table

# Table Service 
class AddTableServiceForm(forms.ModelForm):
    
    class Meta:
        model = TableService
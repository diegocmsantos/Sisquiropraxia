# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.translation import gettext as __

from django.contrib import messages

from django.contrib.auth.decorators import login_required

@login_required
def index(request, template="site_base.html"):
    return render_to_response(template,
                                {},
                                context_instance=RequestContext(request))



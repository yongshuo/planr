from django.shortcuts import render

from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy
from users.models import EntityLogin
import json
from django.http import HttpResponse
from datetime import datetime, timedelta
from config import settings

def gantter(request):
    context = {}
    
    if request.session.has_key('EMAIL') == False:
        return redirect('/login/')
    
    context['TAB'] = 'GANTTER'
    context['EMAIL'] = request.session['EMAIL']
    
    return render_to_response(
        'gantter/gantter.html',
        context,
        context_instance = RequestContext(request)
    )


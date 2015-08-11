from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy
from django.utils import translation
from users.models import EntityLogin
from django.http import HttpResponse
import json

def index(request):
    context = {}
    
    return render_to_response(
        'users/home.html',
        context,
        context_instance = RequestContext(request)
    )

def dashboard(request):
    context = {}
    
    if request.session.has_key('EMAIL') == False:
        return redirect('/login/')
    
    context['TAB'] = 'DASHBOARD'
    context['EMAIL'] = request.session['EMAIL'] if request.session.has_key('EMAIL') else None
    
    return render_to_response(
        'dashboard/dashboard.html',
        context,
        context_instance = RequestContext(request)
    )

def change_language_ajax(request):
    
    lang = request.POST.get('lang','en')
    
    translation.activate(lang)
    request.session[translation.LANGUAGE_SESSION_KEY] = lang
    
    request.LANGUAGE_CODE = translation.get_language()
    
    data = {}
    
    return HttpResponse(json.dumps(data), content_type="application/json")

def register(request):
    context = {}
    
    context['Error'] = request.session['REGISTER_ERROR'] if request.session.has_key('REGISTER_ERROR') else None
    
    if request.session.has_key('REGISTER_ERROR'):
        del request.session['REGISTER_ERROR']
    
    return render_to_response(
        'users/register.html',
        context,
        context_instance = RequestContext(request)
    )

def register_action(request):
    
    context = {}
    
    email = request.POST.get('email', None)
    password = request.POST.get('password', None)
    rpassword = request.POST.get('rpassword', None)
    
    if not email:
        request.session['REGISTER_ERROR'] = ugettext_lazy('Please provide email !').encode('utf-8')
        return redirect('/register/')
    
    if not password or not rpassword:
        context['Error'] = ugettext_lazy('Please provide password !')
        return render_to_response('users/register.html',context, context_instance = RequestContext(request))

    if password != rpassword:
        request.session['REGISTER_ERROR'] = ugettext_lazy('Password does not match !').encode('utf-8')
        return redirect('/register/')
    
    try:
        entity_login = EntityLogin.objects.get(email = email)
    except Exception as e:
        try:
            entity_login = EntityLogin(email = email, search_text = email, password = password)
            entity_login.save()
        except Exception as e:
            equest.session['REGISTER_ERROR'] = e.args[0]
            return redirect('/register/')
        
        request.session['REGISTER_SUCCESS'] = ugettext_lazy('Register successfully! you can login now .').encode('utf-8')
        return redirect('/login/')
    else:
        if entity_login:
            request.session['REGISTER_ERROR'] = ugettext_lazy('Email already in use, please choose another one !').encode('utf-8')
            return redirect('/register/')
        
def login(request):
    context = {}
    
    context['Error'] = request.session['LOGIN_ERROR'] if request.session.has_key('LOGIN_ERROR') else None
    context['SuccessMsg'] = request.session['REGISTER_SUCCESS'] if request.session.has_key('REGISTER_SUCCESS') else None
    
    if request.session.has_key('LOGIN_ERROR'):
        del request.session['LOGIN_ERROR'] 
    if request.session.has_key('REGISTER_SUCCESS'):
        del request.session['REGISTER_SUCCESS']
    
    return render_to_response(
        'users/login.html',
        context,
        context_instance = RequestContext(request)
    )

def login_action(request):
    context = {}
    
    email = request.POST.get('email', None)
    password = request.POST.get('password', None)
    
    if not email:
        request.session['LOGIN_ERROR'] = ugettext_lazy('Please provide email !').encode('utf-8')
        return redirect('/login/')
    
    if not password:
        request.session['LOGIN_ERROR'] = ugettext_lazy('Please provide password !').encode('utf-8')
        return redirect('/login/')
    
    try:
        entity_login = EntityLogin.objects.get(email = email)
    except Exception as e:
        request.session['LOGIN_ERROR'] = ugettext_lazy('Login failed, invalid email or password!').encode('utf-8')
        return redirect('/login/')
    
    else:
        if entity_login.verify_password(password) == False:
            request.session['LOGIN_ERROR'] = ugettext_lazy('Login failed, invalid email or password!').encode('utf-8')
            return redirect('/login/')
        else:
            request.session['EMAIL'] = email
            return redirect('/dashboard/')

def logout(request):
    if request.session.has_key('EMAIL'):
        del request.session['EMAIL']
    
    return redirect('/login/')

def account(request):
    context = {}
    
    if request.session.has_key('EMAIL') == False:
        return redirect('/login/')
    
    context['EMAIL'] = request.session['EMAIL'] if request.session.has_key('EMAIL') else None
    
    context['Error'] = request.session['UPDATEACCOUNT_ERROR'] if request.session.has_key('UPDATEACCOUNT_ERROR') else None
    context['SuccessMsg'] = request.session['UPDATEACCOUNT_SUCCESS'] if request.session.has_key('UPDATEACCOUNT_SUCCESS') else None
    
    if request.session.has_key('UPDATEACCOUNT_ERROR'):
        del request.session['UPDATEACCOUNT_ERROR']
    
    if request.session.has_key('UPDATEACCOUNT_SUCCESS'):
        del request.session['UPDATEACCOUNT_SUCCESS']
    
    try:
        entity_login = EntityLogin.objects.get(email = context['EMAIL'])
    except Exception as e:
        context['Error'] = e.args[0]
    else:
        context['full_name'] = entity_login.full_name
        context['email'] = entity_login.email
    
    context['TAB'] = 'ACCOUNT'
    
    return render_to_response(
        'users/account.html',
        context,
        context_instance = RequestContext(request)
    )

def update_account(request):
    email = request.POST.get('email', None)
    full_name = request.POST.get('fname', None)
    password = request.POST.get('password', None)
    
    pre_email = request.session['EMAIL'] if request.session.has_key('EMAIL') else None
    
    if not pre_email:
        return redirect('/login/')
    
    try:
        entity_login = EntityLogin.objects.get(email = pre_email)
    except Exception as e:
        request.session['UPDATEACCOUNT_ERROR'] = e.args[0]
        return redirect('/account/')
    else:
        entity_login.email = email
        entity_login.full_name = full_name
        if password:
            entity_login.password = password
        
        entity_login.save()
        
        request.session['EMAIL'] = email
        
        request.session['UPDATEACCOUNT_SUCCESS'] = ugettext_lazy('Account details updated successfully!').encode('utf-8')
        return redirect('/account/')
        
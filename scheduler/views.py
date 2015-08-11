from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy
from scheduler.models import Category, Event
from users.models import EntityLogin
import json
from django.http import HttpResponse
from datetime import datetime, timedelta
from config import settings

def scheduler(request):
    context = {}
    
    if request.session.has_key('EMAIL') == False:
        return redirect('/login/')
    
    context['TAB'] = 'SCHEDULE'
    context['EMAIL'] = request.session['EMAIL']
    
    return render_to_response(
        'scheduler/scheduler.html',
        context,
        context_instance = RequestContext(request)
    )

def load_category_ajax(request):
    
    return_data, details = {}, []
    
    if request.session.has_key('EMAIL') == False:
        return redirect('/login/')
    try:
        entity_login = EntityLogin.objects.get(email = request.session['EMAIL'])
    except Exception as e:
        raise Exception(e.args[0])
    else:
        category = Category.objects.filter(owner = entity_login).order_by('-id')
    
        for c in category:
            details.append({
                'owner' : entity_login.email,
                'categoryId' : str(c.id),
                'name' : c.name,
                'color' : c.color,
                'value':str(c.id),
                'text':c.name,
            })
    
        return_data['details'] = details
        
    return HttpResponse(json.dumps(return_data), content_type = 'application/json')

def update_category_ajax(request):
    
    if request.session.has_key('EMAIL') == False:
        return redirect('/login/')
    
    models = request.POST.get('models', None)
    
    import ast
    data =  ast.literal_eval(models)
    data_dict = data[0]
    
    return_data = {}
    
    try:
        category = Category.objects.get(id = int(data_dict['categoryId']))
    except Exception as e:
        raise Exception(e.args[0])
    else:
        category.name = data_dict['name']
        category.color = data_dict['color']
        category.save()
    
    return HttpResponse(json.dumps(return_data), content_type = 'application/json')

def create_category_ajax(request):
    if request.session.has_key('EMAIL') == False:
        return redirect('/login/')
    
    models = request.POST.get('models', None)
    
    import ast
    data =  ast.literal_eval(models)
    data_dict = data[0]
    
    return_data = {}
    
    try:
        entity_login = EntityLogin.objects.get(email = request.session['EMAIL'])
    except Exception as e:
        raise Exception(e.args[0])
    else:
        try:
            category = Category(owner = entity_login, name = data_dict['name'], color = data_dict['color'])
            category.save()
        except Exception as e:
            raise Exception(e.args[0])
    
    return HttpResponse(json.dumps(return_data), content_type = 'application/json')

def delete_category_ajax(request):
    if request.session.has_key('EMAIL') == False:
        return redirect('/login/')
    
    models = request.POST.get('models', None)
    
    import ast
    data =  ast.literal_eval(models)
    data_dict = data[0]
    
    return_data = {}
    
    try:
        category = Category.objects.get(id = int(data_dict['categoryId']))
    except Exception as e:
        raise Exception(e.args[0])
    else:
        category.delete()
        
    return HttpResponse(json.dumps(return_data), content_type = 'application/json')

def load_events_ajax(request):
    if request.session.has_key('EMAIL') == False:
        return redirect('/login/')
    
    details, return_data = [], {}
    
    models = request.POST.get('models', None)
    
    
    import ast
    data_dict =  ast.literal_eval(models)
    
    try:
        entity_login = EntityLogin.objects.get(email = request.session['EMAIL'])
    except Exception as e:
        raise Exception(e.args[0])
    else:
        category = Category.objects.filter(owner = entity_login)
        
        for c in category:
            events = Event.objects.filter(category = c)
            for e in events:
                details.append({
                    'eventId' : str(e.id),
                    'title' : e.title,
                    'start' : datetime.strftime(e.start_date,'%Y-%m-%d') if e.isAllDay else datetime.strftime(e.start_date_time.replace(tzinfo = settings.TZ_INFO) - timedelta(minutes = int(data_dict['tz'])), '%Y-%m-%d %I:%M %p'),
                    'end' : datetime.strftime(e.to_date,'%Y-%m-%d') if e.isAllDay else datetime.strftime(e.to_date_time.replace(tzinfo = settings.TZ_INFO) - timedelta(minutes = int(data_dict['tz'])), '%Y-%m-%d %I:%M %p'),
                    #'start_timezone' : e.start_time_zone,
                    #'end_timezone' : e.end_time_zone,
                    'description' : e.description,
                    'recurrenceID' : e.recurrenceID,
                    'recurrenceRule' : e.recurrenceRule,
                    'recurrenceException' : e.recurrenceException,
                    'categoryId' : str(e.category.id),
                    'isAllDay' : e.isAllDay,
                })
        return_data['details'] = details
        
    return HttpResponse(json.dumps(return_data), content_type = 'application/json')

def create_events_ajax(request):
    if request.session.has_key('EMAIL') == False:
        return redirect('/login/')
    
    details, return_data = [], {}
    models = request.POST.get('models', None)
    tz = request.POST.get('tz', None)
    
    models = models.replace('false','False').replace('true','True')
    
    import ast
    data =  ast.literal_eval(models)
    data_dict = data[-1]
    
    
    try:
        category = Category.objects.get(id = int(data_dict['categoryId']))
    except Exception as e:
        raise Exception(e.args[0])
    else:
        if data_dict['isAllDay'] == True: 
            start_date = datetime.strptime(data_dict['start'].split('T')[0],'%Y-%m-%d') - timedelta(minutes = int(tz))
            end_date = datetime.strptime(data_dict['end'].split('T')[0], '%Y-%m-%d') - timedelta(minutes = int(tz))
            start_date_time, end_date_time = None, None
        else:
            start_date_time = datetime.strptime(data_dict['start'], '%Y-%m-%dT%H:%M:00.000Z') - timedelta(minutes = int(tz))
            end_date_time = datetime.strptime(data_dict['end'], '%Y-%m-%dT%H:%M:00.000Z') - timedelta(minutes = int(tz))
            start_date, end_date = None, None
        
        
        event = Event(category = category, title = data_dict['title'], start_date = start_date,
                      start_date_time = start_date_time, to_date = end_date, to_date_time = end_date_time,
                      recurrenceID = data_dict['recurrenceID'], recurrenceRule = data_dict['recurrenceRule'],
                      recurrenceException = data_dict['recurrenceException'], isAllDay = data_dict['isAllDay'],
                      description = data_dict['description'])
        
        event.save()
        
    return HttpResponse(json.dumps(return_data), content_type = 'application/json')

def update_events_ajax(request):
    
    if request.session.has_key('EMAIL') == False:
        return redirect('/login/')
    
    details, return_data = [], {}
    models = request.POST.get('models', None)
    tz = request.POST.get('tz', None)
    
    models = models.replace('false','False').replace('true','True')
    
    import ast
    data =  ast.literal_eval(models)
    data_dict = data[-1]

    try:
        category = Category.objects.get(id = int(data_dict['categoryId']))
    except Exception as e:
        raise Exception(e.args[0])
    else:
        try:
            event = Event.objects.get(id = int(data_dict['eventId']))
        except Exception as e:
            raise Exception(e.args[0])
        else:
            event.category = category
            event.title = data_dict['title']
            if data_dict['isAllDay'] == True: 
                event.start_date = datetime.strptime(data_dict['start'].split('T')[0],'%Y-%m-%d') - timedelta(minutes = int(tz))
                event.to_date = datetime.strptime(data_dict['end'].split('T')[0], '%Y-%m-%d') - timedelta(minutes = int(tz))
                event.start_date_time = None
                event.to_date_time = None
            else:
                event.start_date_time = datetime.strptime(data_dict['start'], '%Y-%m-%dT%H:%M:00.000Z') - timedelta(minutes = int(tz))
                event.to_date_time = datetime.strptime(data_dict['end'], '%Y-%m-%dT%H:%M:00.000Z') - timedelta(minutes = int(tz))
                start_date, end_date = None, None
                event.to_date = None
            
            event.description = data_dict['description']
            event.isAllDay = data_dict['isAllDay']
            event.recurrenceID = data_dict['recurrenceID']
            event.recurrenceRule = data_dict['recurrenceRule']
            event.recurrenceException = data_dict['recurrenceException']
            
            event.save()
    
    return_data = {}
    
    return HttpResponse(json.dumps(return_data), content_type = 'application/json')

def delete_event_ajax(request):
    if request.session.has_key('EMAIL') == False:
        return redirect('/login/')
    
    models = request.POST.get('models', None)
    
    models = models.replace('false','False').replace('true','True')
    
    import ast
    data =  ast.literal_eval(models)
    data_dict = data[-1]
    
    try:
        event = Event.objects.get(id = int(data_dict['eventId']))
    except Exception as e:
        raise Exeption(e.args[0])
    else:
        event.delete()
        
    return_data = {}
    
    return HttpResponse(json.dumps(return_data), content_type = 'application/json')
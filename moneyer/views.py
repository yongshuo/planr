from django.shortcuts import render

from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy
from users.models import EntityLogin
from moneyer.models import Moneyer
import json
from django.http import HttpResponse
from datetime import datetime, timedelta
from config import settings
from decimal import Decimal

def moneyer(request):
    context = {}
    
    if request.session.has_key('EMAIL') == False:
        return redirect('/login/')
    
    context['TAB'] = 'MONEYER'
    context['EMAIL'] = request.session['EMAIL']
    
    if request.LANGUAGE_CODE == 'zh-hans':
        context['to_date'] = datetime.strftime(datetime.today(), '%Y/%m/%d')
        context['from_date'] = datetime.strftime(datetime.today() - timedelta(days = 30), '%Y/%m/%d')
    else:
        context['to_date'] = datetime.strftime(datetime.today(), '%m/%d/%Y')
        context['from_date'] = datetime.strftime(datetime.today() - timedelta(days = 30), '%m/%d/%Y')
        
    return render_to_response(
        'moneyer/moneyer.html',
        context,
        context_instance = RequestContext(request)
    )

def load_moneyer(request):
    if request.session.has_key('EMAIL') == False:
        return redirect('/login/')
    
    from_date = request.POST.get('from_date', None)
    to_date = request.POST.get('to_date', None)
    
    if from_date:
        if request.LANGUAGE_CODE == 'zh-hans':
            from_date = datetime.strptime(from_date, '%Y/%m/%d')
        else:
            from_date = datetime.strptime(from_date, '%m/%d/%Y')
    else:
        from_date = datetime.today() - timedelta(days = 30)
    
    if to_date:
        if request.LANGUAGE_CODE == 'zh-hans':
            to_date = datetime.strptime(to_date, '%Y/%m/%d')
        else:
            to_date = datetime.strptime(to_date, '%m/%d/%Y')
    else:
        to_date = datetime.today()
    
    try:
        entity_login = EntityLogin.objects.get(email = request.session['EMAIL'])
    except Exception as e:
        raise Exception(e.args[0])
    else:
        details = []
        
        moneyers = Moneyer.objects.filter(create_date__lte = to_date, create_date__gte = from_date, owner = entity_login)
        for m in moneyers:
            categories = {}
            categories['categoryID'] = m.money_category
            categories['categoryName'] = map(lambda s: s[1], filter(lambda s: s[0] == m.money_category, Moneyer.MONEY_CATEGORY))[0].encode('utf-8')
            details.append({
                'transactionID' : str(m.id),
                'category' : categories,
                'credit' : str(m.credit),
                'debit' : str(m.debit),
                'date' : datetime.strftime(m.create_date, '%Y/%m/%d') if request.LANGUAGE_CODE == 'zh-hans' else datetime.strftime(m.create_date, '%m/%d/%Y'),
                'sort_date' : datetime.strftime(m.create_date, '%Y/%m/%d'),
                'remarks' : m.remarks,
            })
    
    details = sorted(details, key = lambda s: datetime.strptime(s['sort_date'], '%Y/%m/%d'), reverse = True)
    
    return_data = {'details' : details }
    
    return HttpResponse(json.dumps(return_data), content_type = 'application/json')


def load_moneyer_category(request):
    if request.session.has_key('EMAIL') == False:
        return redirect('/login/')
    
    details = []
    for d in Moneyer.MONEY_CATEGORY:
        details.append({
            'categoryID' : str(d[0]),
            'categoryName' : d[1].encode('UTF-8'),
        })
    
    details = sorted(details, key = lambda s: s['categoryName'])
    
    return_data = {'category' : details }
    
    return HttpResponse(json.dumps(return_data), content_type = 'application/json')

def create_moneyer(request):
    if request.session.has_key('EMAIL') == False:
        return redirect('/login/')
    
    models = request.POST.get('models', None)
    
    models = models.replace('false','False').replace('true','True')
    
    import ast
    data =  ast.literal_eval(models)
    data_dict = data[-1]
    
    date = datetime.strptime(data_dict['date'].split('T')[0], '%Y-%m-%d')
    
    try:
        entity_login = EntityLogin.objects.get(email = request.session['EMAIL'])
    except Exception as e:
        raise Exception(e.args[0])
    else:
        try:
            moneyer = Moneyer(owner = entity_login,
                                money_category = int(data_dict['category']['categoryID']),
                                credit = data_dict['credit'],
                                debit = data_dict['debit'],
                                create_date = date, remarks = data_dict['remarks'])
            moneyer.save()
        except Exception as e:
            raise Exception(e.args[0])
        
    return_data = {}
    
    return HttpResponse(json.dumps(return_data), content_type = 'application/json')

def update_moneyer(request):
    if request.session.has_key('EMAIL') == False:
        return redirect('/login/')
    
    models = request.POST.get('models', None)
    
    models = models.replace('false','False').replace('true','True')
    
    import ast
    data =  ast.literal_eval(models)
    data_dict = data[-1]
    
    date = datetime.strptime(data_dict['date'].split('T')[0], '%Y-%m-%d') + timedelta(days = 1)
    
    try:
        moneyer = Moneyer.objects.get(id = int(data_dict['transactionID']))
    except Exception as e:
        raise Exception(e.args[0])
    else:
        moneyer.money_category = data_dict['category']['categoryID']
        moneyer.credit = data_dict['credit']
        moneyer.debit = data_dict['debit']
        moneyer.remarks = data_dict['remarks']
        moneyer.create_date = date
        
        moneyer.save()
    return_data = {}
    
    return HttpResponse(json.dumps(return_data), content_type = 'application/json')

def delete_moneyer(request):
    if request.session.has_key('EMAIL') == False:
        return redirect('/login/')
    
    models = request.POST.get('models', None)
    
    models = models.replace('false','False').replace('true','True')
    
    import ast
    data =  ast.literal_eval(models)
    data_dict = data[-1]
    
    try:
        moneyer = Moneyer.objects.get(id = int(data_dict['transactionID']))
    except Exception as e:
        raise Exception(e.args[0])
    else:
        moneyer.delete()
    
    return_data = {}
    
    return HttpResponse(json.dumps(return_data), content_type = 'application/json')
    
    
def load_dashboard_pie(request):
    if request.session.has_key('EMAIL') == False:
        return redirect('/login/')
    
    import random
    r = lambda: random.randint(0,255)

    total_amount, details = Decimal(0.0), []
    
    try:
        entity_login = EntityLogin.objects.get(email = request.session['EMAIL'])
    except Exception as e:
        raise Exception(e.args[0])
    else:    
        for c in Moneyer.MONEY_CATEGORY:
            amount = Decimal(0.0)
            for m in Moneyer.objects.filter(owner = entity_login, money_category = c[0]):
                amount += m.credit
                amount += m.debit
                total_amount += m.credit
                total_amount += m.debit
            
            details.append({
                'value' : str(amount),
                'category' : c[1].encode('UTF-8'),
                'color' : '#%02X%02X%02X' % (r(),r(),r())
            })
    
    return_data = {'details' : details}
    
    return HttpResponse(json.dumps(return_data), content_type = 'application/json')
    
def load_dashboard_line(request):
    
    if request.session.has_key('EMAIL') == False:
        return redirect('/login/')

    try:
        entity_login = EntityLogin.objects.get(email = request.session['EMAIL'])
    except Exception as e:
        raise Exception(e.args[0])
    else:
        list_value = []
        list_date = []
        
        i = 13
        while i >= 0:
            money  = Decimal(0.0)
            date = datetime.today() - timedelta(days = i)
            for m  in Moneyer.objects.filter(owner = entity_login, create_date__lte = date):
                money += m.credit
                money -= m.debit
            
            list_value.append(str(money))
            list_date.append(datetime.strftime(date, '%Y-%m-%d'))
            
            i -= 1
        
        return_data = {'value_list' : list_value, 'date_list' : list_date}
    
    return HttpResponse(json.dumps(return_data), content_type = 'application/json')

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from cms.models import Minutes
from cms.forms import MinutesForm

from etherpad_lite import EtherpadLiteClient
import os
from datetime import datetime

f = open('./etherpad-lite/APIKEY.txt')
EP_API_KEY = f.readline()
f.close()
EP_CLIENT = EtherpadLiteClient(base_params={'api_key': EP_API_KEY})
EP_CLIENT.api_version = '1.2.13'

# Create your views here.
def minutes_list(request):
    """show minutes list"""
    minutes_list = Minutes.objects.all().order_by('id')
    return render(request,
                    'cms/minutes_list.html',
                    {'minutes_list': minutes_list})

def minutes_edit(request, minutes_id=None):
    """edit minutes"""
    if minutes_id:
        minutes = get_object_or_404(Minutes, pk=minutes_id)
        padID = minutes.minutes_url.split('/')[-1]
    else:
        minutes = Minutes()
        dt = datetime.now()
        padID = dt.strftime('%Y%m%d%H%M%S')
        pad_url = '%s/p/%s'%(EP_CLIENT.base_url.replace('/api', ''), padID)
        minutes.minutes_url = pad_url

    if request.method == 'POST':
        form = MinutesForm(request.POST, instance=minutes)
        if form.is_valid():
            minutes = form.save(commit=False)
            minutes.save()
            try:
                ret = EP_CLIENT.createPad(padID=padID)
                # if ret == ...
                EP_CLIENT.setHTML(padID=padID, html='<html></html>')
            except Exception as e:
                print(str(e))

            return redirect('cms:minutes_list')
    else:
        form = MinutesForm(instance=minutes)
    return render(request, 'cms/minutes_edit.html', dict(form=form, minutes_id=minutes_id))

def minutes_del(request, minutes_id):
    """delete minutes"""
    minutes = get_object_or_404(Minutes, pk=minutes_id)
    minutes.delete()
    try:
        padID = minutes.minutes_url.split('/')[-1]
        EP_CLIENT.deletePad(padID=padID)
    except Exception as e:
        print(str(e))
    return redirect('cms:minutes_list')

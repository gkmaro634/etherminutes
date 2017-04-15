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

SHOW_SEARCH_RESULT_CONTENT_LENGTH = 255

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

def minutes_search(request):
    if request.method == 'GET':
        return redirect('cms:minutes_list')
    elif request.method == 'POST':
        search_word = request.POST.get('search_word')
        minutes_list = Minutes.objects.all().order_by('id')
        search_results = {}
        cnt = 0
        for minutes in minutes_list:
            padID = minutes.minutes_url.split('/')[-1]
            pad_content = EP_CLIENT.getText(padID=padID)['text']
            print(search_word in pad_content)
            if len(pad_content) > SHOW_SEARCH_RESULT_CONTENT_LENGTH:
                find_idx = pad_content.find(search_word)
                if len(pad_content[find_idx:]) > SHOW_SEARCH_RESULT_CONTENT_LENGTH:
                    start_idx = find_idx
                    end_idx = start_idx + SHOW_SEARCH_RESULT_CONTENT_LENGTH
                    if start_idx == 0:
                        pad_content = pad_content[start_idx: end_idx] + '... '
                    else:
                        pad_content = '... ' + pad_content[start_idx: end_idx] + '... '

                else:
                    start_idx = len(pad_content) - SHOW_SEARCH_RESULT_CONTENT_LENGTH
                    end_idx = start_idx + SHOW_SEARCH_RESULT_CONTENT_LENGTH
                    pad_content = '... ' + pad_content[start_idx: end_idx]
                print(start_idx, end_idx)
            else:
                pass
            if search_word in pad_content:
                tmp_l = pad_content.split(search_word)
                bolded_search_word = '<span style="background-color: #ffff00;">'+search_word+'</span>'
                out_pad_content = bolded_search_word.join(tmp_l)
                search_results[cnt] = {}
                search_results[cnt]['padID'] = padID
                search_results[cnt]['name'] = minutes.name
                search_results[cnt]['minutes_url'] = minutes.minutes_url
                search_results[cnt]['pad_content'] = out_pad_content
                cnt += 1

        return render(request, 'cms/search_result.html', dict(search_word=search_word, search_results=search_results, hitnum=cnt))
    return redirect('cms:minutes_list')

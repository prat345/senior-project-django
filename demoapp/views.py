from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from .mongo import get_collection_names, get_data, get_incident, get_stations, get_video, get_all_video, delete_incident, update_label, get_information, get_testdrive_info
from .graph import make_plot, waypoint_chart, make_chart1, make_chart2, incident_num_chart
import numpy as np
import pandas as pd
import pickle
from django.core.paginator import Paginator
from demoapp.models import TestLog

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def summary(request):
    info_df = get_information()
    chart1 = make_chart1(info_df)
    chart2, chart3 = make_chart2(info_df,'month')
    chart4, chart5 = make_chart2(info_df,'vehicle')
    context = {}
    for i in range(1,6):
        context[f'chart{i}'] = vars()['chart'+str(i)].to_html()
    context['incident_num_chart']=incident_num_chart().to_html()
    return render(request, 'summary.html',context)
    
def testdrive(request):
    collections = get_collection_names()
    incident_d = get_incident()
    station_wp = get_stations()
    testdrive = collections[0]
    if request.method == "POST":
        if 'testdrive' in request.POST:
            testdrive = request.POST["testdrive"] # get data
        elif 'download-csv' in request.POST:
            df = get_data(testdrive)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename={testdrive}.csv'
            df.to_csv(path_or_buf=response,sep=',')
            return response
        print('>>>>',testdrive) 
    incident_d = incident_d[testdrive]
    df = get_data(testdrive)
    topics = ['twist.linear.x','linear_acceleration.x_filtered', 'msg.brake', 'msg.mode']
    yaxis = ['Velocity(m/s)', 'Long Acc(m/s\u00b2)', 'Brake Input(%)', 'Mode']
    context = {'charts':{}, 'collections':collections , 'selected_test':testdrive}
    for index, topic in enumerate(topics):
        fig = make_plot(df,topic, yaxis[index], incident_d)
        chart = fig.to_html()
        context['charts'][f'chart{index+1}'] = chart

    fig = waypoint_chart(df, incident_d, testdrive, station_wp)
    context['waypoint'] = fig.to_html()
    dic = get_testdrive_info(testdrive)
    context['stats'] = dic
    return render(request, 'testdrive.html', context)

def testdrive2(request,selected):
    collections = get_collection_names()
    incident_d = get_incident()
    station_wp = get_stations()
    # testdrive = collections[0]
    testdrive = selected
    if request.method == "POST":
        if 'testdrive' in request.POST:
            testdrive = request.POST["testdrive"] # get data
        elif 'download-csv' in request.POST:
            df = get_data(testdrive)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename={testdrive}.csv'
            df.to_csv(path_or_buf=response,sep=',')
            return response
        # print(testdrive) 
    incident_d = incident_d[testdrive]
    df = get_data(testdrive)
    topics = ['twist.linear.x','linear_acceleration.x_filtered', 'msg.brake', 'msg.mode']
    yaxis = ['Velocity(m/s)', 'Long Acc(m/s\u00b2)', 'Brake Input(%)', 'Mode']
    context = {'charts':{}, 'collections':collections , 'selected_test':testdrive}
    for index, topic in enumerate(topics):
        fig = make_plot(df,topic, yaxis[index], incident_d)
        chart = fig.to_html()
        context['charts'][f'chart{index+1}'] = chart

    fig = waypoint_chart(df, incident_d, testdrive, station_wp)
    context['waypoint'] = fig.to_html()
    dic = get_testdrive_info(testdrive)
    context['stats'] = dic
    return render(request, 'testdrive.html', context)

def incident(request):
    factors = ['External','Internal']
    # EXTERNAL
    actors = ['Vehicle','Truck','Tuk-Tuk','Bus','Motorcycle','Pedestrian','Animal','Cyclist','Scooter','Non-Motor Vehicle','Other Vehicle']
    environments = ['Obstacle','Straight Road','Slope','Corner','Crosswalk','Junction','Roundabout','Speed Bump']
    scenarios = ['Cut In','Parking','Emergency Brake','Red Light Running','Wrong-Way Driving','Turning Across Lane','Other Scenario']
    # INTERNAL
    occupants = ['Driver','Passenger','Emergency']
    systems = ['Battery','Sensing','Localization','Planning','Computing Node']
    context = {'labels':{'Actor':actors, 'Environment':environments,
                'Scenario':scenarios, 'Occupant':occupants, 'System':systems}}
    # all_labels = factors+actors+environments+scenarios+occupants+systems + list(context['labels'].keys())

    labels = []
    if request.method == "POST":
        labels = request.POST.getlist('label')
        context['selected'] = labels
        operation = request.POST['operation']
        context['operation'] = operation
        query = get_video(labels,operation)
        # context['query_p'] = query
    else:
        # query = get_all_video()
        q1 = request.GET.get('q1','AND')
        q2 = request.GET.get('q2','DEFAULT')
        q2 = q2.split('_')
        print('>>>>> query1',q1,'query2',q2)
        operation = q1
        labels = q2
        context['selected'] = labels
        context['operation'] = operation
        query = get_video(labels,operation)
        # pagination
    p = Paginator(query, 5)
    page = request.GET.get('page')
    query_p = p.get_page(page)
    context['query_p'] = query_p
    context['query'] = query
    request.session['query'] = pickle.dumps(query).hex()
    return render(request, 'incident.html', context)

# def incident2(request, select_operation, selected):
#     selected = selected.split('_')
#     factors = ['External','Internal']
#     # EXTERNAL
#     actors = ['Vehicle','Truck','Tuk-Tuk','Bus','Motorcycle','Pedestrian','Animal','Cyclist','Scooter','Non-Motor Vehicle','Other Vehicle']
#     environments = ['Obstacle','Straight Road','Slope','Corner','Crosswalk','Junction','Roundabout','Speed Bump']
#     scenarios = ['Cut In','Parking','Emergency Brake','Red Light Running','Wrong-Way Driving','Turning Across Lane','Other Scenario']
#     # INTERNAL
#     occupants = ['Driver','Passenger','Emergency']
#     systems = ['Battery','Sensing','Localization','Planning','Computing Node']
#     context = {'labels':{'Actor':actors, 'Environment':environments,
#                 'Scenario':scenarios, 'Occupant':occupants, 'System':systems}}
#     labels = []
#     if request.method == "POST":
#         # get data
#         labels = request.POST.getlist('label')
#         operation = request.POST['operation']    
#     else:
#         labels = selected
#         operation = select_operation
#     context['selected'] = labels
#     context['operation'] = operation
#     query = get_video(labels,operation)
#     # pagination
#     p = Paginator(query, 5)
#     page = request.GET.get('page')
#     query_p = p.get_page(page)
#     context['query_p'] = query_p
#     context['query'] = query
#     request.session['query'] = pickle.dumps(query).hex()
#     return render(request, 'incident.html', context)

def edit(request,to_edit):
    print('TO EDIT: ',to_edit)
    query = request.session.get('query')
    query = pickle.loads(bytes.fromhex(query))
    # print(query)
    for dic in query:
        if dic['stamp'] == to_edit:
            edit_info = dic
    if request.method == 'POST':
        newLabel = request.POST['label']
        newLabel = newLabel.split(', ')
        print(newLabel)
        update_label(to_edit, newLabel)
        messages.success(request,'Update Succesfully')
        return redirect("/incident")
    else:
        return render(request, 'edit.html', {'to_edit': edit_info})

def delete(request, to_delete):
    print('TO DELETE: ', to_delete)
    delete_incident(to_delete)
    messages.success(request,f'Delete {to_delete} Succesfully')
    return redirect("/incident") 

def driver_input(request):
    if request.method == "POST":
        # get data
        dic = {}
        for i in 'driver,date,time,vehicle,location,label,note'.split(','):
            if i in request.POST:
                dic[i] = request.POST[i]
            else:
                dic[i] = ''
        # record data to db
        newlog = TestLog.objects.create( 
            driver = dic['driver'],
            date = dic['date'],
            time = dic['time'],
            vehicle = dic['vehicle'],
            location = dic['location'],
            label = dic['label'],
            note = dic['note'],
        )
        newlog.save()
        messages.success(request,'Record Successfully')
        return redirect('/show-log')
    else:
        return render(request, 'new-log.html')

def show_log(request):
    all_log = TestLog.objects.all().order_by('-id') # sort newest first
    # pagination
    p = Paginator(all_log, 10)
    page = request.GET.get('page')
    log_p = p.get_page(page)
    context = {'all_log':all_log}
    context['log_p'] = log_p
    return render(request, 'show-log.html', context)

def edit_log(request, log_id):
    log = TestLog.objects.get(id=log_id)
    if request.method == 'POST':
        log.driver = request.POST['driver']
        log.vehicle = request.POST["vehicle"]
        log.location = request.POST["location"]
        log.note = request.POST["note"]
        if request.POST["date"] != '':
            log.date = request.POST["date"]
        if request.POST["time"] != '':
            log.time = request.POST["time"]
        if "label" in request.POST:
            log.label = request.POST["label"]
        log.save()
        messages.success(request,'Update Succesfully')
        return redirect("/show-log")
    else:
        return render(request, 'edit-log.html', {'log':log})

def delete_log(request, log_id):
    log = TestLog.objects.get(id=log_id)
    log.delete()
    messages.success(request,'Remove Succesfully')
    return redirect("/show-log")

def test(request):
    # testdrive  = 'T2-B_SL_NBTC_20230125202407'
    # if request.method == 'POST':
    #     df = get_data(testdrive)
    #     response = HttpResponse(content_type='text/csv')
    #     response['Content-Disposition'] = f'attachment; filename={testdrive}.csv'
    #     df.to_csv(path_or_buf=response,sep=',')
    #     return response
    # else:
    #     return render(request, 'test.html', context={'test':testdrive})
    
    if request.method == 'POST':
        results = request.POST.getlist('interest')
        print(results)

    return render(request, 'test.html')
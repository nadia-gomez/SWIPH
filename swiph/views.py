from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from .forms import processForm,inputBasicForm, inputAdvancedForm
from .models import simulation, BasicMachineLearningDB, MachineLearningDB, ScriptTracker, ErrorCode
from datetime import datetime,timedelta
import numpy as np

from .bokeh_graphs import production_b, storage_b

from .samSimulator import samSim

import sys
import os
import re

import pandas as pd
from iapws import IAPWS97

#from .tasks import basic_start_dbcreation
from django.db.models import Count
from joblib import load
clf = load(os.path.dirname(__file__)+'/basic_classificator.joblib')

# Create your views here.

def asyc_projectshape_nModBoil(request):

    P_turb_des, T_cold_ref, location = (float(request.GET['P_turb_des']), float(request.GET['T_cold_ref']), request.GET['location'])

    if location=='Daggett':
        lat, lon, asm = (34.865371,-116.783023, 215)
    elif location=='Fargo':
        lat, lon, asm = (46.9, -96.8, 276)
    elif location=='Tucson':
        lat, lon, asm = (32.116521, -110.933042, 728)
    elif location=='Blythe':
        lat, lon, asm = (33.617773, -114.588261, 83)
    elif location=='Phoenix':
        lat, lon, asm = (33.450495, -111.983688, 331)
    elif location=='Imperial':
        lat, lon, asm = (32.835205, -115.572398, 18)

    succes_subspace = pd.DataFrame(list(BasicMachineLearningDB.objects.filter(label=1,lat__lt=lat+0.001, lat__gt=lat-0.001, lon__gt=lon-0.001, lon__lt=lon+0.001, asm__lt=asm+0.01, asm__gt=asm-0.01).values('P_turb_des', 'T_cold_ref', 'nModBoil')))
    succes_subspace = succes_subspace.values
    sim_point = np.array([P_turb_des, T_cold_ref, 0])
    #now it is matter to find the nearest point, the success and location is guaranteed.
    distance_vectors = sim_point-succes_subspace
    
    #Agregar, distancia maxima y pesos dependiendo del tipo de error
    w = np.array([1,1,1])
    #Recomendar la variable que más cerca está del punto de prueba
    distances = np.sqrt(w[0]*distance_vectors[:,0]**2+w[1]*distance_vectors[:,1]**2+w[2]*distance_vectors[:,2]**2)
    suggestion = succes_subspace[np.where(distances == np.amin(distances))[0][0]]
    
    form=inputBasicForm()
    return HttpResponse(int(suggestion[2]))
    #return render(request, 'swiph/plant_shape.html', {'form':form, 'default_nModBoil':int(suggestion[2])})

def asyc_project_shape(request):
    
    pk, nModBoil, demand, demandUnit = [int(request.GET['pk']), int(request.GET['nModBoil']), float(request.GET['demand']), request.GET['demandUnit'],]
    
    if demandUnit=='MWh':
        demand=demand*1000
    elif demandUnit=='KJ':
        demand=demand*0.000278
    elif demandUnit=='BTU':
        demand=demand*0.000293
    elif demandUnit=='kcal':
        demand=demand*0.001162

    hourINI,hourEND,Mond,Tues,Wend,Thur,Fri,Sat,Sun,Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec = [int(request.GET['hourINI']),int(request.GET['hourEND']),request.GET['Mond'],request.GET['Tues'],request.GET['Wend'],request.GET['Thur'],request.GET['Fri'],request.GET['Sat'],request.GET['Sun'],request.GET['Jan'],request.GET['Feb'],request.GET['Mar'],request.GET['Apr'],request.GET['May'],request.GET['Jun'],request.GET['Jul'],request.GET['Aug'],request.GET['Sep'],request.GET['Oct'],request.GET['Nov'],request.GET['Dec']]

    prof_w = [Mond,Tues,Wend,Thur,Fri,Sat,Sun]
    n_w=0
    for i, val in enumerate(prof_w):
        if val == 'true':
            prof_w[i] = 'on'
            n_w+=1
    [Mond,Tues,Wend,Thur,Fri,Sat,Sun] = prof_w

    prof_y = [Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec]
    n_y=0
    for i, val in enumerate(prof_y):
        if val == 'true':
            prof_y[i] = 'on'
            n_y+=1
    [Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec] = prof_y

    if n_w==0:
        [Mond,Tues,Wend,Thur,Fri,Sat,Sun] = ['on','on','on','on','on','on','on']
    if n_y==0:
        [Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec] = ['on','on','on','on','on','on','on','on','on','on','on','on']

    sim = simulation.objects.get(id=pk)

    annualHourly=createDemandArrays(demand,hourINI,hourEND,Mond,Tues,Wend,Thur,Fri,Sat,Sun,Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec)
    sim.nLoops=int((np.ceil(max(annualHourly))*1000)/(sim.I_bn_des*sim.A_aperture*sim.GeomEffects*nModBoil))
    
    sim.nLoops = sim.nLoops + (sim.nLoops==0)

    form=inputBasicForm()

    return JsonResponse({'designPower':int(max(annualHourly)), 'default_nLoops':sim.nLoops, 'default_nModBoil':nModBoil})
    #return render(request, 'swiph/plant_shape.html', {'form':form,'designPower':int(max(annualHourly)), 'default_nLoops':sim.nLoops, 'default_nModBoil':nModBoil})

def check_PT(request):
    [T,P] = [float(request.GET['T']),float(request.GET['P'])]
    try:
        x = IAPWS97(P=P*0.1, T=T+273).x
        if x==0:
            resultado=True
        else:
            resultado=False
    except:
        resultado = False
    return HttpResponse(resultado)

def async_basic_classificator(request):
    
    #['P_turb_des', 'T_cold_ref', 'asm', 'lat', 'lon', 'nModBoil']
    P_turb_des, T_cold_ref, nModBoil, location = (float(request.GET['P_turb_des']), float(request.GET['T_cold_ref']), float(request.GET['nModBoil']), request.GET['location'])
    if location=='Daggett':
        lat, lon, asm = (34.865371,-116.783023, 215)
    elif location=='Fargo':
        lat, lon, asm = (46.9, -96.8, 276)
    elif location=='Tucson':
        lat, lon, asm = (32.116521, -110.933042, 728)
    elif location=='Blythe':
        lat, lon, asm = (33.617773, -114.588261, 83)
    elif location=='Phoenix':
        lat, lon, asm = (33.450495, -111.983688, 331)
    elif location=='Imperial':
        lat, lon, asm = (32.835205, -115.572398, 18)

    sim_test = [[P_turb_des, T_cold_ref, asm, lat, lon, nModBoil]]

    error_code = clf.predict(sim_test)

    if error_code[0]!=1:
        error_message = ErrorCode.objects.get(pk = error_code[0])
        succes_subspace = pd.DataFrame(list(BasicMachineLearningDB.objects.filter(label=1,lat__lt=lat+0.001, lat__gt=lat-0.001, lon__gt=lon-0.001, lon__lt=lon+0.001, asm__lt=asm+0.01, asm__gt=asm-0.01).values('P_turb_des', 'T_cold_ref', 'nModBoil')))
        succes_subspace = succes_subspace.values
        sim_point = np.array([P_turb_des, T_cold_ref, nModBoil])
        #now it is matter to find the nearest point, the success and location is guaranteed.
        distance_vectors = sim_point-succes_subspace
        
        w = np.array([100,100,1])
        #Recomendar la variable que más cerca está del punto de prueba
        distances = np.sqrt(w[0]*distance_vectors[:,0]**2+w[1]*distance_vectors[:,1]**2+w[2]*distance_vectors[:,2]**2)
        suggestion = succes_subspace[np.where(distances == np.amin(distances))[0][0]]
        
        form=inputBasicForm()
        if all([P_turb_des, T_cold_ref, nModBoil]==suggestion[:3]):
            contexto = {'error_code':1}
        else:
            contexto = {'error_code':error_code, 'error':error_message,'P_turb_des':suggestion[0], 'T_cold_ref':suggestion[1], 'nModBoil':suggestion[2],'location':location, 'f':form}

        
        return render(request, 'swiph/basic_classificator_alert.html', contexto)
    
    

    return render(request, 'swiph/basic_classificator_alert.html',{'error_code':error_code})

        #Guardar simulaciones para entrenar de nuevo el forest
"""
def async_mldb_status(request):
    total = len(BasicMachineLearningDB.objects.all())
    grouped_results = BasicMachineLearningDB.objects.all().values('label').annotate(total=Count('label'))
    results = []
    for result_type in grouped_results:
        error = ErrorCode.objects.get(pk=result_type['label']).error
        results += [(error, result_type['total'])]
    total_success = len(BasicMachineLearningDB.objects.filter(label=5))
    latest_sims = BasicMachineLearningDB.objects.all().order_by('-pk')[:10]
    return  render(request, 'ml_db/async_db_status.html',{'total':total,'results':results, 'latest_sims':latest_sims})


@login_required
@permission_required('swiph.view_machinelearningdb')
def mldb_status(request):
    #TaskResult.objects.latest('date_created')
    if request.method=="POST":
        if request.POST.get("action")=="start":
            annualHourly = createDemandArrays(123321, 1,24, 'on','on','on','on','on','on','on',    'on','on','on','on','on','on','on','on','on','on','on','on')
            ScriptTracker.objects.create(name="create_basic_mldb", keep_running=True)
            basic_start_dbcreation.delay(annualHourly.tolist())
            return HttpResponseRedirect(reverse_lazy('mldb_status'))
        elif request.POST.get("action")=="stop":
            track = ScriptTracker.objects.filter(name="create_basic_mldb").latest('starting_date')
            track.keep_running = False
            track.save()
            return HttpResponseRedirect(reverse_lazy('mldb_status'))

    llamadas = ScriptTracker.objects.filter(name="create_basic_mldb")
    if len(llamadas)>0:
        if llamadas.latest('starting_date').keep_running:
            action="stop"
        else:
            action = "start"
    else: #if it is the first time you start the process
        ErrorCode.objects.get_or_create(error="success")
        action = "start"

    total = len(MachineLearningDB.objects.all())
    total_success = len(MachineLearningDB.objects.filter(label="success"))

    return  render(request, 'ml_db/db_status.html',{'total':total,'total_success':total_success,'action':action})
"""

def mobile(request):
    """Return True if the request comes from a mobile device."""
    MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)

    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return True
    else:
        return False

def readSOLAR(location):
    if location=='Daggett':
        meteoFile='daggett_ca_34.865371_-116.783023_psmv3_60_tmy.csv'
    elif location=='Fargo':
        meteoFile='fargo_nd_46.9_-96.8_mts1_60_tmy.csv'
    elif location=='Tucson':
        meteoFile='tucson_az_32.116521_-110.933042_psmv3_60_tmy.csv'
    elif location=='Blythe':
        meteoFile='blythe_ca_33.617773_-114.588261_psmv3_60_tmy.csv'
    elif location=='Phoenix':
        meteoFile='phoenix_az_33.450495_-111.983688_psmv3_60_tmy.csv'
    elif location=='Imperial':
        meteoFile='imperial_ca_32.835205_-115.572398_psmv3_60_tmy.csv'
    
  
    solar = pd.read_csv(os.path.dirname(os.path.dirname(__file__))+"/solar_resource/"+meteoFile, skiprows=2)
    annualDNI=sum(solar['DNI'])/1000 #kWh/m2

    return(meteoFile,annualDNI)

def createDemandArrays(demand,hourINI,hourEND,Mond,Tues,Wend,Thur,Fri,Sat,Sun,Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec):
    dayArray=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    activeHours=int(hourEND)-int(hourINI)
    porctDay=1/activeHours
    for j in range(int(hourINI)-1,int(hourEND)):
        dayArray[j]=porctDay

    weekArray=[0,0,0,0,0,0,0]
    week=[Mond,Tues,Wend,Thur,Fri,Sat,Sun]
    week=[1 if x == 'on' else 0 for x in week]
    porctWeek=1/sum(week)
    for j in range(len(weekArray)):
        if week[j]==1:
            weekArray[j]=porctWeek

    monthArray=[0,0,0,0,0,0,0,0,0,0,0,0]
    year=[Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec]
    year=[1 if x == 'on' else 0 for x in year]
    porctYear=1/sum(year)
    for j in range(len(monthArray)):
        if year[j]==1:
            monthArray[j]=porctYear

    days_in_the_month=[31,28,31,30,31,30,31,31,30,31,30,31] #days_in_the_month[month_number]=how many days are in the month number "month_number"
    
    start_week_day=0 #Asume the first day starts in monday. I could make it variable with the datetime python module but I dont know the conequences in a server
    
    weight_of_hours_in_month=[] #Create the auxiliar list where I'll store the porcentage(weight) of use of every hour for the current month in the loop
    weight_of_hours_in_year=[] #Create the auxiliar list where I'll store the porcentage(weight) of use of every hour of one year
    
    for month_number in range(12): #For each month (12) in the year
        for day_of_the_month in range(days_in_the_month[month_number]): #Calculates the porcentage of use every hour for the whole month
            day=(start_week_day+day_of_the_month)%7 #Calculate wich day it is (Mon=0,Tues=1, ...) using the module 7, so day is which day in the week correspond to each day number in the month
            weight_of_hours_in_month += np.multiply(weekArray[day],dayArray).tolist() #Builts the array of use of every hour in the month, multiplying the porcentage of use of that specific day to the porcentage of use of each hour and then appends it to the end of the list (".tolist() method used to append as a list and do not sum as an array) as the next day.
        start_week_day=(day+1)%7 #pulls out which was the last day in the previus month to use it in the next day in the beginning of the next month
        weight_of_hours_in_year += np.multiply(monthArray[month_number],weight_of_hours_in_month).tolist() #Multiplies the hours of use of the month to the porcentage of use of the month in the year, then appends the list to the end of the weight_of_hours_in_year list
        weight_of_hours_in_month=[] #Restarts the weight_of_hours_in_month list to be used again for the next month data
       
    renormalization_factor=sum(weight_of_hours_in_year) #calculates the renormalization factor of the list in order to get "1" when summing all the 8760 elements.
    totalConsumption_normailized=demand/renormalization_factor #Renormalices the totalConsumption
    
    annualHourly=np.multiply(totalConsumption_normailized,weight_of_hours_in_year) #Obtains the energy required for every hour in the year.
        
    return (annualHourly)


def SW_index(request):
     
    if request.method=="POST":
        form=processForm(request.POST)
        if form.is_valid():
            process=form.cleaned_data['process']
            size=form.cleaned_data['size']
            
            if process[0]=='L':
                industry='laundry'
            elif process[0]=='D':
                industry='dairy'
            elif process[0]=='T':
                industry='textile'
            elif process[0]=='F':
                industry='meat'
            elif process[0]=='C':
                industry='cork manufacturing'
            elif process[0]=='M':
                industry='mining'
            else:
                industry='unknown'

            simulation.objects.create(
                created=datetime.now().strftime('%Y-%m-%d %H:%M'),
                process=process[2:],
                size=size[2:],
                industry=industry,
                ).save()
            
            sim = simulation.objects.latest('id')
            return HttpResponseRedirect('basicInput/'+str(sim.id))
        else:
            form=processForm()  
    else:
       form=processForm()    
    return  render(request, 'swiph/SW_index.html',{'form':form})

def basicInput(request,pk):
    sim = simulation.objects.get(id=pk)
    
    if request.method=="POST":
        form=inputBasicForm(request.POST)
        if form.is_valid():
            location=form.cleaned_data['location']
            pressure=form.cleaned_data['pressure']
            tempIN=form.cleaned_data['tempIN']
            demand=form.cleaned_data['demand']
            demandUnit=form.cleaned_data['demandUnit']
            hourINI=form.cleaned_data['hourINI']
            hourEND=form.cleaned_data['hourEND']
            
            Mond=form.cleaned_data['Mond']
            Tues=form.cleaned_data['Tues']
            Wend=form.cleaned_data['Wend']
            Thur=form.cleaned_data['Thur']
            Fri=form.cleaned_data['Fri']
            Sat=form.cleaned_data['Sat']
            Sun=form.cleaned_data['Sun']
            if all(v=='' for v in [Mond,Tues,Wend,Thur,Fri,Sat,Sun,]):
                [Mond,Tues,Wend,Thur,Fri,Sat,Sun,] = ['on']*7

            Jan=form.cleaned_data['Jan']
            Feb=form.cleaned_data['Feb']
            Mar=form.cleaned_data['Mar']
            Apr=form.cleaned_data['Apr']
            May=form.cleaned_data['May']
            Jun=form.cleaned_data['Jun']
            Jul=form.cleaned_data['Jul']
            Aug=form.cleaned_data['Aug']
            Sep=form.cleaned_data['Sep']
            Oct=form.cleaned_data['Oct']
            Nov=form.cleaned_data['Nov']
            Dec=form.cleaned_data['Dec']
            if all(v=='' for v in [Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec,]):
                [Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec,] = ['on']*12
            
            if demandUnit=='MWh':
                demand=demand*1000
            if demandUnit=='KJ':
                demand=demand*0.000278
            if demandUnit=='BTU':
                demand=demand*0.000293
            if demandUnit=='kcal':
                demand=demand*0.001162
            
            sim.location=location
            sim.pressure=pressure
            sim.tempIN=tempIN
            sim.demand=demand
            sim.demandUnit=demandUnit
            sim.hourINI=hourINI
            sim.hourEND=hourEND
            sim.Mond=Mond
            sim.Tues=Tues
            sim.Wend=Wend
            sim.Thur=Thur
            sim.Fri=Fri
            sim.Sat=Sat
            sim.Sun=Sun
            sim.Jan=Jan
            sim.Feb=Feb
            sim.Mar=Mar
            sim.Apr=Apr
            sim.May=May
            sim.Jun=Jun
            sim.Jul=Jul
            sim.Aug=Aug
            sim.Sep=Sep
            sim.Oct=Oct
            sim.Nov=Nov
            sim.Dec=Dec
            sim.nLoops = form.cleaned_data['nLoops']
            sim.nModBoil = form.cleaned_data['nModBoil']
            sim.save()

            return HttpResponseRedirect('../advancedInput/'+str(sim.id))
    else:

        #Prepares default variables
        all_default_variables = pd.read_csv(os.path.dirname(__file__)+'/default_var.csv')
        specific_default_variables = all_default_variables[all_default_variables.Industry.eq(sim.industry) & all_default_variables.Process.eq(sim.process) & all_default_variables.Size.eq(sim.size)]
        del specific_default_variables['Process']
        del specific_default_variables['Size']
        del specific_default_variables['Industry']
        specific_default_variables = specific_default_variables.rename(columns={'demand [MWh]':'demand'})
        specific_default_variables = specific_default_variables.to_dict('records')[0]
        specific_default_variables.update({'demandUnit':'MWh', 'hourINI': str(specific_default_variables['hourINI']), 'hourEND': str(specific_default_variables['hourEND'])})

        form=inputBasicForm(initial=specific_default_variables)

    return  render(request, 'swiph/basicInput.html',{'form':form,'industry':sim.industry,'id':sim.id})

def advancedInput(request,pk):
    sim = simulation.objects.get(id=pk)
    

    annualHourly=createDemandArrays(sim.demand,sim.hourINI,sim.hourEND,sim.Mond,sim.Tues,sim.Wend,sim.Thur,sim.Fri,sim.Sat,sim.Sun,sim.Jan,sim.Feb,sim.Mar,sim.Apr,sim.May,sim.Jun,sim.Jul,sim.Aug,sim.Sep,sim.Oct,sim.Nov,sim.Dec)
    
    #sim.nLoops=(np.ceil(max(annualHourly))*1000)/(sim.I_bn_des*sim.A_aperture*sim.GeomEffects*sim.nModBoil)  
    #sim.save()

    if request.method=="POST":
        form=inputAdvancedForm(request.POST)
        if form.is_valid():

            nLoops=form.cleaned_data['nLoops']
            nModBoil=form.cleaned_data['nModBoil']
            I_bn_des=form.cleaned_data['I_bn_des']
            x_b_des=form.cleaned_data['x_b_des']
            heat_sink_dP_frac=form.cleaned_data['heat_sink_dP_frac']
            theta_dep=form.cleaned_data['theta_dep']
            theta_stow=form.cleaned_data['theta_stow']
            V_wind_max=form.cleaned_data['V_wind_max']
            ColAz=form.cleaned_data['ColAz']
            T_amb_des_sf=form.cleaned_data['T_amb_des_sf']
            SCA_drives_elec=form.cleaned_data['SCA_drives_elec']
            Pipe_hl_coef=form.cleaned_data['Pipe_hl_coef']
            csp_lf_sf_water_per_wash=form.cleaned_data['csp_lf_sf_water_per_wash']
            csp_lf_sf_washes_per_year=form.cleaned_data['csp_lf_sf_washes_per_year']
            fP_hdr_c=form.cleaned_data['fP_hdr_c']
            fP_sf_boil=form.cleaned_data['fP_sf_boil']
            fP_hdr_h=form.cleaned_data['fP_hdr_h']
            T_fp=form.cleaned_data['T_fp']
            eta_pump=form.cleaned_data['eta_pump']
            e_startup=form.cleaned_data['e_startup']
            A_aperture=form.cleaned_data['A_aperture']
            L_col=form.cleaned_data['L_col']
            TrackingError=form.cleaned_data['TrackingError']
            GeomEffects=form.cleaned_data['GeomEffects']
            rho_mirror_clean=form.cleaned_data['rho_mirror_clean']
            dirt_mirror=form.cleaned_data['dirt_mirror']
            error=form.cleaned_data['error']
            IAM_T0=form.cleaned_data['IAM_T0']
            IAM_T1=form.cleaned_data['IAM_T1']
            IAM_T2=form.cleaned_data['IAM_T2']
            IAM_T3=form.cleaned_data['IAM_T3']
            IAM_T4=form.cleaned_data['IAM_T4']
            IAM_L0=form.cleaned_data['IAM_L0']
            IAM_L1=form.cleaned_data['IAM_L1']
            IAM_L2=form.cleaned_data['IAM_L2']
            IAM_L3=form.cleaned_data['IAM_L3']
            IAM_L4=form.cleaned_data['IAM_L4']
            HL_dT_0=form.cleaned_data['HL_dT_0']
            HL_dT_1=form.cleaned_data['HL_dT_1']
            HL_dT_2=form.cleaned_data['HL_dT_2']
            HL_dT_3=form.cleaned_data['HL_dT_3']
            HL_dT_4=form.cleaned_data['HL_dT_4']
            HL_W_0=form.cleaned_data['HL_W_0']
            HL_W_1=form.cleaned_data['HL_W_1']
            HL_W_2=form.cleaned_data['HL_W_2']
            HL_W_3=form.cleaned_data['HL_W_3']
            HL_W_4=form.cleaned_data['HL_W_4']

            sim.nModBoil=nModBoil
            sim.nLoops=nLoops
            sim.I_bn_des=I_bn_des
            sim.x_b_des=x_b_des
            sim.heat_sink_dP_frac=heat_sink_dP_frac
            sim.theta_dep=theta_dep
            sim.theta_stow=theta_stow
            sim.V_wind_max=V_wind_max
            sim.ColAz=ColAz
            sim.T_amb_des_sf=T_amb_des_sf
            sim.SCA_drives_elec=SCA_drives_elec
            sim.Pipe_hl_coef=Pipe_hl_coef
            sim.csp_lf_sf_water_per_wash=csp_lf_sf_water_per_wash
            sim.csp_lf_sf_washes_per_year=csp_lf_sf_washes_per_year
            sim.fP_hdr_c=fP_hdr_c
            sim.fP_sf_boil=fP_sf_boil
            sim.fP_hdr_h=fP_hdr_h
            sim.T_fp=T_fp
            sim.eta_pump=eta_pump
            sim.e_startup=e_startup
            sim.A_aperture=A_aperture
            sim.L_col=L_col
            sim.TrackingError=TrackingError
            sim.GeomEffects=GeomEffects
            sim.rho_mirror_clean=rho_mirror_clean
            sim.dirt_mirror=dirt_mirror
            sim.error=error
            sim.IAM_T0=IAM_T0
            sim.IAM_T1=IAM_T1
            sim.IAM_T2=IAM_T2
            sim.IAM_T3=IAM_T3
            sim.IAM_T4=IAM_T4
            sim.IAM_L0=IAM_L0
            sim.IAM_L1=IAM_L1
            sim.IAM_L2=IAM_L2
            sim.IAM_L3=IAM_L3
            sim.IAM_L4=IAM_L4
            sim.HL_dT_0=HL_dT_0
            sim.HL_dT_1=HL_dT_1
            sim.HL_dT_2=HL_dT_2
            sim.HL_dT_3=HL_dT_3
            sim.HL_dT_4=HL_dT_4
            sim.HL_W_0=HL_W_0
            sim.HL_W_1=HL_W_1
            sim.HL_W_2=HL_W_2
            sim.HL_W_3=HL_W_3
            sim.HL_W_4=HL_W_4
            sim.save()

            return HttpResponseRedirect('../samResults/'+str(sim.id)+'/3')

    else:
       form=inputAdvancedForm()

    return  render(request, 'swiph/advancedInput.html',{'form':form,'industry':sim.industry,'id':sim.id,
    'nLoops':int(sim.nLoops),'nModBoil':sim.nModBoil,'designPower':int(max(annualHourly))})

def samResults(request,pk,plt):
    sim = simulation.objects.get(id=pk)
    annualHourly=createDemandArrays(sim.demand,sim.hourINI,sim.hourEND,sim.Mond,sim.Tues,sim.Wend,sim.Thur,sim.Fri,sim.Sat,sim.Sun,sim.Jan,sim.Feb,sim.Mar,sim.Apr,sim.May,sim.Jun,sim.Jul,sim.Aug,sim.Sep,sim.Oct,sim.Nov,sim.Dec)
    
    [meteoFile,annualDNI]=readSOLAR(sim.location)
    meteoPath=os.path.dirname(os.path.dirname(__file__))+"/solar_resource/"+meteoFile
    T_cold_ref=sim.tempIN
    P_turb_des=sim.pressure
    q_pb_des=1 #not used in the simulation
   
    A_aperture =[[ sim.A_aperture], [ 0 ]]
    L_col=[[ sim.L_col ], [ 0 ]]
    TrackingError=[[ sim.TrackingError ], [ 0 ]] # User-defined tracking error derate [none]
    GeomEffects=[[ sim.GeomEffects ], [ 0 ]] # User-defined geometry effects derate [none] (boiler, SH)
    rho_mirror_clean=[[ sim.rho_mirror_clean], [ 0 ]] # User-defined clean mirror reflectivity [none]
    dirt_mirror=[[ sim.dirt_mirror ], [ 0 ]] # User-defined dirt on mirror derate [none]
    error=[[ sim.error ], [ 0 ]] # User-defined general optical error derate [none]
    IAM_T=[[ sim.IAM_T0,   sim.IAM_T1,   sim.IAM_T2,   sim.IAM_T3,   sim.IAM_T4 ], [ 0,   0,   0,   0,   0 ]] # Transverse Incident angle modifiers (0,1,2,3,4 order terms) [none]
    IAM_L=[[ sim.IAM_L0,   sim.IAM_L1,   sim.IAM_L2,   sim.IAM_L3,   sim.IAM_L4  ], [ 0,   0,   0,   0,   0 ]] # Longitudinal Incident angle modifiers (0,1,2,3,4 order terms) [none]
    HL_dT=[[ sim.HL_dT_0,   sim.HL_dT_1,   sim.HL_dT_2,   sim.HL_dT_3,   sim.HL_dT_4 ], [ 0,   0,   0,   0,   0 ]] # Heat loss coefficient - HTF temperature (0,1,2,3,4 order terms) [W/m-K^order]
    HL_W=[[ sim.HL_W_0,   sim.HL_W_1,   sim.HL_W_2,   sim.HL_W_3,   sim.HL_W_4 ], [ 0,   0,   0,   0,   0 ]] # Heat loss coef adj wind velocity (0,1,2,3,4 order terms) [1/(m/s)^order]

    location = sim.location
    if location=='Daggett':
        lat, lon, asm = (34.865371,-116.783023, 215)
    elif location=='Fargo':
        lat, lon, asm = (46.9, -96.8, 276)
    elif location=='Tucson':
        lat, lon, asm = (32.116521, -110.933042, 728)
    elif location=='Blythe':
        lat, lon, asm = (33.617773, -114.588261, 83)
    elif location=='Phoenix':
        lat, lon, asm = (33.450495, -111.983688, 331)
    elif location=='Imperial':
        lat, lon, asm = (32.835205, -115.572398, 18)

    try:
        [dataTemp,results]=samSim(annualHourly,meteoPath,sim.I_bn_des,T_cold_ref,sim.x_b_des,sim.nLoops,q_pb_des,P_turb_des,sim.heat_sink_dP_frac,
            sim.nModBoil,sim.theta_dep,sim.theta_stow,sim.V_wind_max,sim.ColAz,sim.T_amb_des_sf,sim.SCA_drives_elec,
            sim.Pipe_hl_coef,sim.csp_lf_sf_water_per_wash,sim.csp_lf_sf_washes_per_year,sim.fP_hdr_c,
            sim.fP_sf_boil,sim.fP_hdr_h,sim.T_fp,sim.eta_pump,sim.e_startup,A_aperture,L_col,
            TrackingError,GeomEffects,rho_mirror_clean,dirt_mirror,error,
            IAM_T,IAM_L,HL_dT,HL_W)

        succes = ErrorCode.objects.get_or_create(error='success')[0]
        basic_learningdata = {'lon':lon,'lat':lat, 'asm':asm, 'P_turb_des':P_turb_des, 'T_cold_ref':T_cold_ref, 'nModBoil':sim.nModBoil, 'label':succes}
        BasicMachineLearningDB.objects.get_or_create(**basic_learningdata)

    except Exception as e:
        # Just print(e) is cleaner and more likely what you want,
        # but if you insist on printing message specifically whenever possible...
        #errorList.append([T_cold_ref,sim.nModBoil,sim.T_fp,str(e.args[0])])
        
        #gets what kind of error it was. Or creates a new one if it is a new error
        sim_error = ErrorCode.objects.get_or_create(error=str(e.args[0]))
        #builds the data to be stored in the db
        basic_learningdata = {'lon':lon,'lat':lat, 'asm':asm, 'P_turb_des':P_turb_des, 'T_cold_ref':T_cold_ref, 'nModBoil':sim.nModBoil, 'label':sim_error[0]}
        #If there was exatly the same case it will get it otherwise it will reate a new instances and save it
        BasicMachineLearningDB.objects.get_or_create(**basic_learningdata)

        #redirect to the error page
        return render(request, 'swiph/simulation_error.html', {'sim_id':sim.id, 'error':sim_error[0]})

    Q_prod=dataTemp['q_dot_to_heat_sink']*1000
    Q_prod_lim=dataTemp['Q_prod_lim_SAM']*1000
    DNI=dataTemp['beam']
    Demand=annualHourly
    Q_inc_tot=int(sum(dataTemp['q_inc_sf_tot']))
    Q_inc_rec=int(sum(dataTemp['q_dot_rec_inc']))
    Q_abs_rec=int(sum(dataTemp['q_dot_rec_abs']))
    Q_thermal=int(sum(dataTemp['q_dot_rec_thermal_loss']))         
    OptEff=round(100*Q_inc_rec/Q_inc_tot,2)              
   
    if plt == 1:
        init_x=0
        end_x=180
    if plt == 2:
        init_x=2800
        end_x=2960
    if plt == 3:
        init_x=4360
        end_x=4540
    if plt == 4:
        init_x=6543
        end_x=6728

    
    [script_prod,div_prod]=production_b(450,300,Q_prod,Q_prod_lim,DNI,Demand)
    [script_prod2,div_prod2]=storage_b(800,250,init_x,end_x,np.array(dataTemp['q_dot_to_heat_sink']*1000),np.zeros(8760),np.array(Q_prod_lim),np.zeros(8760),Demand,np.array(dataTemp['Q_defocus_SAM']*1000),np.zeros(8760),np.array(np.zeros(8760)))


    
    return  render(request, 'swiph/samResults.html',{'entry':sim,'script_prod':script_prod,'div_prod':div_prod,
    'dataTemp':dataTemp,'result':results,'Q_inc_tot':Q_inc_tot,'Q_inc_rec':Q_inc_rec,'Q_abs_rec':Q_abs_rec,'Q_thermal':Q_thermal,
    'OptEff':OptEff,'script_prod2':script_prod2,'div_prod2':div_prod2,'id':sim.id,'plotModf':[]})




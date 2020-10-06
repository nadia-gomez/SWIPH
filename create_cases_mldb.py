#Set up to connect to django
import sys
import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'miguel.settings'
django.setup()

#Connect and manage the datbase
from swiph.models import BasicMachineLearningDB, ErrorCode, MachineLearningDB
from swiph.samSimulator import samSim
from swiph.views import createDemandArrays
import numpy as np

def basic_dbcreation(n_cases):
    """
    Param: annualHourly [list]. It doesn't need to have anything special
    Return: None. It only feeds the database.

    Creates a databse of artificial basic inputs for the swiph wraper and checks for the errors.
    This will be used for machine learning trainning of a basic clasificator.
    """
    #Just to be sure that pk=1 is hte success case

    #prepare fixed values
    annualHourly = createDemandArrays(123321, 1,24, 'on','on','on','on','on','on','on',    'on','on','on','on','on','on','on','on','on','on','on','on')
    #annualHourly=createDemandArrays(demand [kWh],sim.hourINI,sim.hourEND,sim.Mond,sim.Tues,sim.Wend,sim.Thur,sim.Fri,sim.Sat,sim.Sun,sim.Jan,sim.Feb,sim.Mar,sim.Apr,sim.May,sim.Jun,sim.Jul,sim.Aug,sim.Sep,sim.Oct,sim.Nov,sim.Dec)
    inputs_sam = {
        'annualHourly' : annualHourly,
        #'meteoFile' : os.path.dirname(os.path.dirname(__file__))+"/solar_resource/fargo_nd_46.9_-96.8_mts1_60_tmy.csv",
        'q_pb_des' : .5,
        'IAM_T' : [[ 1.0099999904632568,   -0.29499998688697815,   0.96299999952316284,   -1.2300000190734863,   0.30799999833106995 ], [ 0,   0,   0,   0,   0 ]],
        'IAM_L' : [[ 1,   -0.13400000333786011,   -0.17499999701976776,   -0.39399999380111694,   0.19099999964237213 ], [ 0,   0,   0,   0,   0 ]],
        'HL_dT' : [[ 0,   0.67199999094009399,   0.0025559999048709869,   0,   0 ], [ 0,   0,   0,   0,   0 ]],
        'HL_W' : [[1,0,0,0,0], [ 0,   0,   0,   0,   0 ]],

        # <><><><><><><><><><><><>  Design Point - Solar Field Parameters  <><><><><><><><><><><><>
        'I_bn_des':950, # Solarfield  Design point irradiation value [W/m2]  #From form validation [0,1400)
        'x_b_des':0.40000000596046448, # Solarfield Design point boiler outlet steam quality [none] #From form validation [0,1)
        'nLoops':6, # Solarfield Number of loops [none] # [1,100] 
        
        # <><><><><><><><><><><><>  Design Point - Heat Sink Parameters  <><><><><><><><><><><><>
        'heat_sink_dP_frac':0, # HeatSink Fractional pressure drop through heat sink # From form validation [0,0.2)
        
        # @@@@@@@@@@@@@@@@@@@@@@@@ SOLAR FIELD @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        
        # <><><><><><><><><><><><>  Solar Field Parameters  <><><><><><><><><><><><>
        'theta_dep':10, # Solarfield  Solar elevation for collector morning deploy [deg] # From form validation [0,90)
        'theta_stow':10, # Solarfield  Solar elevation for collector nightime stow [deg]  # From form validation [0,90)
        'V_wind_max':120, # Solarfield Maximum allowable wind velocity before safety stow [m/s]  # From the fastest wind recorded [0,11)
        'ColAz':0, # Solarfield  Collector azimuth angle [deg] IMP -> Disabled when OptCharType:1 since the values are taken from the table  # From form validation [0,360)
        'T_amb_des_sf':42, # Solarfield  Design-point ambient temperature [C] #The hottest ambient temperature ever recorder [0,56)
        'SCA_drives_elec':0, # Solarfield Tracking power.. in Watts per m2 [W/m2] [0,50)
        'Pipe_hl_coef':0, # Solarfield  Loss coefficient from the header.. runner pipe.. and non-HCE pipin [W/m2-K]
        
        # <><><><><><><><><><><><>  Mirror Washing  <><><><><><><><><><><><>
        #####Revisar qué tan relevante es termodinámica
        'csp_lf_sf_water_per_wash':0.019999999552965164, # Heliostat Water usage per wash [L/m2_aper]
        'csp_lf_sf_washes_per_year':12, # Heliostat Mirror washing annual frequency [-/year]
        
        # <><><><><><><><><><><><>  Steam Design Conditions  <><><><><><><><><><><><>
        'fP_hdr_c':0, # Solarfield Average design-point cold header pressure drop fraction [none] # [0,1)
        'fP_sf_boil':0, # Solarfield  Design-point pressure drop across the solar field boiler fraction [none] # [0,1)
        'fP_hdr_h':0, # Solarfield Average design-point hot header pressure drop fraction [none] # [0,1)
        'T_fp':5, # Solarfield  Freeze protection temperature (heat trace activation temperature) [C] #From the cold temperature  [0,T_cold_ref)
        'eta_pump':1, # Solarfield Feedwater pump efficiency [none] #From form validation [0,1)
        
        # <><><><><><><><><><><><>  Plant Heat Capacity  <><><><><><><><><><><><>
        'e_startup':1, # Solarfield  Thermal inertia contribution per sq meter of solar field [kJ/K-m2]
        
        # @@@@@@@@@@@@@@@@@@@@@@@@ COLLECTOR AND RECEIVER @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        # <><><><><><><><><><><><>  Geometry and Optical Performance  <><><><><><><><><><><><>
        'A_aperture':[[ 26.399999618530273 ], [ 0 ]], # Reflective aperture area of the collector module [m^2] (boiler, SH)
        'L_col':[[ 6 ], [ 0 ]], # Active length of the boiler/superheater section collector module [m] (boiler, SH) 
        'TrackingError':[[ 1 ], [ 0 ]], # User-defined tracking error derate [none]
        'GeomEffects':[[ 0.8399999737739563 ], [ 0 ]], # User-defined geometry effects derate [none] (boiler, SH)
        'rho_mirror_clean':[[ 0.93500000238418579 ], [ 0 ]], # User-defined clean mirror reflectivity [none]
        'dirt_mirror':[[ 1 ], [ 0 ]], # User-defined dirt on mirror derate [none]
        'error':[[ 1 ], [ 0 ]], # User-defined general optical error derate [none]
    }

    locations = [
        #(file_name, latitude, longitude, hsl)
        ('daggett_ca_34.865371_-116.783023_psmv3_60_tmy.csv', 34.865371,-116.783023, 215),
        ('fargo_nd_46.9_-96.8_mts1_60_tmy.csv', 46.9, -96.8, 276),
        ('tucson_az_32.116521_-110.933042_psmv3_60_tmy.csv', 32.116521, -110.933042, 728),
        ('blythe_ca_33.617773_-114.588261_psmv3_60_tmy.csv', 33.617773, -114.588261, 83),
        ('phoenix_az_33.450495_-111.983688_psmv3_60_tmy.csv', 33.450495, -111.983688, 331),
        ('imperial_ca_32.835205_-115.572398_psmv3_60_tmy.csv', 32.835205, -115.572398, 18),
    ]
    n = 0
    while n<n_cases:
        #Prepare random values
        
        location = locations[np.random.randint(len(locations))]

        inputs={
            'T_cold_ref':round(np.random.uniform(low=inputs_sam['T_fp'],high=150),2), #[0,150)
            'P_turb_des':round(np.random.rand()*20,2), # Solarfield Heat sink inlet pressure [bar] #[0,20)
            'nModBoil':np.random.randint(low=1, high=51), # Solarfield  Number of modules in the boiler section [none] # [1,50] 
        }

        inputs_sam.update(inputs)
        inputs_sam.update({'meteoFile' : "solar_resource/"+location[0],})

        inputs.update({'lat':location[1],'lon':location[2],'asm':location[3],})
        try:
            dataTemp,results = samSim(**inputs_sam)
            success = ErrorCode.objects.get_or_create(error="success")[0]
            BasicMachineLearningDB.objects.create(label=success, **inputs)
        except Exception as e:
            error = ErrorCode.objects.get_or_create(error=str(e.args[0]))[0]
            BasicMachineLearningDB.objects.create(label=error, **inputs)

        n+=1

def full_dbcreation(n_cases):
    """
    Param: annualHourly list. It doesn't need to have anything special
    Return: None. It only feeds the database.

    Creates a databse with artificial inputs for SAM and their errors.
    This will be used for machine learning trainning.
    """

    #prepare fixed values
    
    annualHourly = np.array(annualHourly)
    #annualHourly=createDemandArrays(demand [kWh],sim.hourINI,sim.hourEND,sim.Mond,sim.Tues,sim.Wend,sim.Thur,sim.Fri,sim.Sat,sim.Sun,sim.Jan,sim.Feb,sim.Mar,sim.Apr,sim.May,sim.Jun,sim.Jul,sim.Aug,sim.Sep,sim.Oct,sim.Nov,sim.Dec)
    inputs_sam = {
        'annualHourly' : annualHourly,
        'meteoFile' : os.path.dirname(os.path.dirname(__file__))+"/solar_resource/fargo_nd_46.9_-96.8_mts1_60_tmy.csv",
        'q_pb_des' : 1,
        'IAM_T' : [[1.01,-0.295,0.963,-1.23,0.308], [ 0,   0,   0,   0,   0 ]],
        'IAM_L' : [[1,-0.134,-0.175,-0.394,0.19], [ 0,   0,   0,   0,   0 ]],
        'HL_dT' : [[0,0.672,0.00255,0,0], [ 0,   0,   0,   0,   0 ]],
        'HL_W' : [[1,0,0,0,0], [ 0,   0,   0,   0,   0 ]],
    }

    n=0
    while n<n_cases:
    #for i in range(500):

        if not ScriptTracker.objects.filter(name="create_mldb").latest('starting_date').keep_running:
            break

        rv = np.random.rand(28) #rv=random_values Just to create all the random number at once.
        #Prepare random values
        T_cold_ref=round(rv[1]*150,2) #[0,150)
        A_aperture=round((rv[20]*50)+1,2) #[1,50)
        inputs={
            # <><><><><><><><><><><><>  Design Point - Solar Field Parameters  <><><><><><><><><><><><>
            'I_bn_des':round(rv[0]*1400,2), # Solarfield  Design point irradiation value [W/m2]  #From form validation [0,1400)
            'T_cold_ref':T_cold_ref, # Powerblock Reference HTF outlet temperature at design [C] #393 was the T_hot temperature [0,393)
            'x_b_des':round(rv[2],2), # Solarfield Design point boiler outlet steam quality [none] #From form validation [0,1)

            'nLoops':np.random.randint(low=1, high=101), # Solarfield Number of loops [none] # [1,100] 
            
            # <><><><><><><><><><><><>  Design Point - Heat Sink Parameters  <><><><><><><><><><><><>
            'P_turb_des':round(rv[4]*16,2), # Solarfield Heat sink inlet pressure [bar] #[0,16)
            
            'heat_sink_dP_frac':round(rv[4]*0.2,2), # HeatSink Fractional pressure drop through heat sink # From form validation [0,0.2)
            
            
            # @@@@@@@@@@@@@@@@@@@@@@@@ SOLAR FIELD @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            
            # <><><><><><><><><><><><>  Solar Field Parameters  <><><><><><><><><><><><>
            'nModBoil':np.random.randint(low=1, high=51), # Solarfield  Number of modules in the boiler section [none] # [1,100] 
            'theta_dep':round(rv[5]*20,2), # Solarfield  Solar elevation for collector morning deploy [deg] # From form validation [0,90)
            'theta_stow':round(rv[6]*20,2), # Solarfield  Solar elevation for collector nightime stow [deg]  # From form validation [0,90)
            'V_wind_max':round(rv[7]*200,2), # Solarfield Maximum allowable wind velocity before safety stow [m/s]  # From the fastest wind recorded [0,11)
            'ColAz':round(rv[8]*360,2), # Solarfield  Collector azimuth angle [deg] IMP -> Disabled when OptCharType:1 since the values are taken from the table  # From form validation [0,360)
            'T_amb_des_sf':round(rv[9]*50,2), # Solarfield  Design-point ambient temperature [C] #The hottest ambient temperature ever recorder [0,56)

            'SCA_drives_elec':round(rv[10]*50,2), # Solarfield Tracking power.. in Watts per m2 [W/m2] [0,50)
            'Pipe_hl_coef':round(rv[11]*50,2), # Solarfield  Loss coefficient from the header.. runner pipe.. and non-HCE pipin [W/m2-K]
            
            # <><><><><><><><><><><><>  Mirror Washing  <><><><><><><><><><><><>
            #####Revisar qué tan relevante es termodinámica
            'csp_lf_sf_water_per_wash':round(rv[12]*0.1,2), # Heliostat Water usage per wash [L/m2_aper]
            'csp_lf_sf_washes_per_year':round(rv[13]*24,2), # Heliostat Mirror washing annual frequency [-/year]
            
            # <><><><><><><><><><><><>  Steam Design Conditions  <><><><><><><><><><><><>
            'fP_hdr_c':round(rv[14],2), # Solarfield Average design-point cold header pressure drop fraction [none] # [0,1)
            'fP_sf_boil':round(rv[15],2), # Solarfield  Design-point pressure drop across the solar field boiler fraction [none] # [0,1)
            'fP_hdr_h':round(rv[16],2), # Solarfield Average design-point hot header pressure drop fraction [none] # [0,1)
            'T_fp':round(rv[17]*T_cold_ref,2), # Solarfield  Freeze protection temperature (heat trace activation temperature) [C] #From the cold temperature  [0,T_cold_ref)
            'eta_pump':round(rv[18],2), # Solarfield Feedwater pump efficiency [none] #From form validation [0,1)
            
            # <><><><><><><><><><><><>  Plant Heat Capacity  <><><><><><><><><><><><>
            'e_startup':round(rv[19]*20,2), # Solarfield  Thermal inertia contribution per sq meter of solar field [kJ/K-m2]
            
            # @@@@@@@@@@@@@@@@@@@@@@@@ COLLECTOR AND RECEIVER @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

            # <><><><><><><><><><><><>  Geometry and Optical Performance  <><><><><><><><><><><><>
            'A_aperture':A_aperture, # Solarfield  Reflective aperture area of the collector module [m^2] (boiler, SH) #Double of the default input [0,50)
            'L_col':round(rv[21]*A_aperture,2), # Solarfield  Active length of the boiler/superheater section collector module [m] (boiler, SH) 
            'TrackingError':round(rv[22],2)+0.01, # Solarfield  User-defined tracking error derate [none] #[0.01,1]
            'GeomEffects':round(rv[23],2)+0.01, # Solarfield  User-defined geometry effects derate [none] (boiler, SH) #[0.01,1]
            'rho_mirror_clean':round(rv[24],2)+0.01, # Solarfield  User-defined clean mirror reflectivity [none] #[0.01,1]
            'dirt_mirror':round(rv[25],2)+0.01, # Solarfield User-defined dirt on mirror derate [none] #[0.01,1]
            'error':round(rv[26],2)+0.01, # Solarfield User-defined general optical error derate [none] #[0.01,1]i
        }
        inputs_sam.update(inputs)
        inputs_sam.update({
                'A_aperture':[[ inputs['A_aperture']], [ 0 ]],
                'L_col':[[ inputs['L_col'] ], [ 0 ]],
                'TrackingError':[[ inputs['TrackingError'] ], [ 0 ]], # User-defined tracking error derate [none]
                'GeomEffects':[[ inputs['GeomEffects'] ], [ 0 ]], # User-defined geometry effects derate [none] (boiler, SH)
                'rho_mirror_clean':[[ inputs['rho_mirror_clean']], [ 0 ]], # User-defined clean mirror reflectivity [none]
                'dirt_mirror':[[ inputs['dirt_mirror'] ], [ 0 ]], # User-defined dirt on mirror derate [none]
                'error':[[ inputs['error'] ], [ 0 ]], # User-defined general optical error derate [none]
        })
        try:
            dataTemp,results = samSim(**inputs_sam)
            success = ErrorCode.objects.get_or_create(error="success")
            MachineLearningDB.objects.create(**inputs, label=success)
        except Exception as e:
            error = ErrorCode.objects.get_or_create(error=str(e.args[0]))
            MachineLearningDB.objects.create(**inputs, label=error)
        n+=1

if sys.argv[1]== "check_success_code":
    ErrorCode.objects.update_or_create(pk=1, error='success')
elif sys.argv[1]=="basic":
    basic_start_dbcreation(int(sys.argv[2]))
elif sys.argv[1]=="full":
    full_dbcreation(int(sys.argv[2]))
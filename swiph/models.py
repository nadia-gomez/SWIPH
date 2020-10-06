from django.db import models
from django.contrib.auth.models import User
from datetime import date
# Create your models here.
class ScriptTracker(models.Model):
    name = models.CharField(max_length=60, default="create_mldb")
    starting_date = models.DateTimeField(auto_now_add=True)
    ending_date = models.DateTimeField(blank=True, null=True, auto_now=True)
    keep_running = models.BooleanField(default=True)

    def __str__(self):
        return str(self.keep_running)
    

class ErrorCode(models.Model):
    #The pk is the errror code.
    error = models.TextField()
    def __str__(self):
        return self.error[:15]
    

class BasicMachineLearningDB(models.Model):
    """
    Database to store the only the lat, lon, asm, P_turb_des, T_cold_ref, nModBoil and the possible error code
    for the basic classificator training.
    """
    #Label
    label = models.ForeignKey('ErrorCode', on_delete=models.CASCADE)

    #Features
    lat = models.FloatField() 
    lon = models.FloatField()
    asm = models.FloatField() # meters
    P_turb_des = models.FloatField() #[0,20]
    T_cold_ref = models.FloatField() #[0,150]
    nModBoil = models.FloatField() #[1,50]

    def __str__(self):
        return str(self.label)
    

class MachineLearningDB(models.Model):
    """
    DB table to store the possible relevant features and labels that we will use for machine learning
    """

    ######################################  LABEL  ############################################
    #label = models.ForeignKey('ErrorCode', on_delete=models.CASCADE)
    label = models.TextField()

    ####################################  FEATURES  ###########################################
    # <><><><><><><><><><><><>  Design Point - Solar Field Parameters  <><><><><><><><><><><><>
    I_bn_des=models.FloatField() # Solarfield  Design point irradiation value [W/m2]
    T_cold_ref=models.FloatField() # Powerblock Reference HTF outlet temperature at design [C]
    x_b_des=models.FloatField() # Solarfield Design point boiler outlet steam quality [none]
    
    nLoops=models.IntegerField() # Solarfield Number of loops [none]
    
    # <><><><><><><><><><><><>  Design Point - Heat Sink Parameters  <><><><><><><><><><><><>
    P_turb_des=models.FloatField() # Solarfield Heat sink inlet pressure [bar]
    heat_sink_dP_frac=models.FloatField() # HeatSink Fractional pressure drop through heat sink
    
    
    # @@@@@@@@@@@@@@@@@@@@@@@@ SOLAR FIELD @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    
    # <><><><><><><><><><><><>  Solar Field Parameters  <><><><><><><><><><><><>
    
    nModBoil=models.IntegerField() # Solarfield  Number of modules in the boiler section [none]
    theta_dep=models.FloatField() # Solarfield  Solar elevation for collector morning deploy [deg]
    theta_stow=models.FloatField() # Solarfield  Solar elevation for collector nightime stow [deg]
    V_wind_max=models.FloatField() # Solarfield Maximum allowable wind velocity before safety stow [m/s]
    ColAz=models.FloatField() # Solarfield  Collector azimuth angle [deg] IMP -> Disabled when OptCharType=1 since the values are taken from the table
    T_amb_des_sf=models.FloatField() # Solarfield  Design-point ambient temperature [C]
    SCA_drives_elec=models.FloatField() # Solarfield Tracking power.. in Watts per m2 [W/m2]
    Pipe_hl_coef=models.FloatField() # Solarfield  Loss coefficient from the header.. runner pipe.. and non-HCE pipin [W/m2-K]
    
    # <><><><><><><><><><><><>  Mirror Washing  <><><><><><><><><><><><>
    
    csp_lf_sf_water_per_wash=models.FloatField() # Heliostat Water usage per wash [L/m2_aper]
    csp_lf_sf_washes_per_year=models.FloatField() # Heliostat Mirror washing annual frequency [-/year]
    
    # <><><><><><><><><><><><>  Steam Design Conditions  <><><><><><><><><><><><>
    
    fP_hdr_c=models.FloatField() # Solarfield Average design-point cold header pressure drop fraction [none]
    fP_sf_boil=models.FloatField() # Solarfield  Design-point pressure drop across the solar field boiler fraction [none]
    fP_hdr_h=models.FloatField() # Solarfield Average design-point hot header pressure drop fraction [none]
    T_fp=models.FloatField() # Solarfield  Freeze protection temperature (heat trace activation temperature) [C]
    eta_pump=models.FloatField() # Solarfield Feedwater pump efficiency [none]
    
    # <><><><><><><><><><><><>  Plant Heat Capacity  <><><><><><><><><><><><>
    
    e_startup=models.FloatField() # Solarfield  Thermal inertia contribution per sq meter of solar field [kJ/K-m2]
    
    # @@@@@@@@@@@@@@@@@@@@@@@@ COLLECTOR AND RECEIVER @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    
    # <><><><><><><><><><><><>  Geometry and Optical Performance  <><><><><><><><><><><><>
    
    A_aperture =models.FloatField() # Solarfield  Reflective aperture area of the collector module [m^2] (boiler, SH)
    L_col=models.FloatField() # Solarfield  Active length of the boiler/superheater section collector module [m] (boiler, SH) 
    TrackingError=models.FloatField() # Solarfield  User-defined tracking error derate [none]
    GeomEffects=models.FloatField() # Solarfield  User-defined geometry effects derate [none] (boiler, SH)
    rho_mirror_clean=models.FloatField() # Solarfield  User-defined clean mirror reflectivity [none]
    dirt_mirror=models.FloatField() # Solarfield User-defined dirt on mirror derate [none]
    error=models.FloatField() # Solarfield User-defined general optical error derate [none]

class simulation(models.Model):
    created=models.DateField(auto_now_add=True)
    industry = models.CharField(max_length=60, default="unknown")
    process = models.CharField(max_length=80, default="unknown")
    size = models.CharField(max_length=20, default="unknown")

    #Location
    location=models.CharField(max_length=200, blank=True,null=True)

    #Process
    pressure=models.FloatField(blank=True, null=True)
    tempIN=models.FloatField(blank=True, null=True)
    
    #Demand
    demand=models.FloatField(blank=True, null=True)
    demandUnit=models.CharField(blank=True,max_length=50, null=True)
    hourINI=models.IntegerField(blank=True, null=True)
    hourEND=models.IntegerField(blank=True, null=True)

    Mond=models.CharField(blank=True,max_length=4, null=True)
    Tues=models.CharField(blank=True,max_length=4, null=True)
    Wend=models.CharField(blank=True,max_length=4, null=True)
    Thur=models.CharField(blank=True,max_length=4, null=True)
    Fri=models.CharField(blank=True,max_length=4, null=True)
    Sat=models.CharField(blank=True,max_length=4, null=True)
    Sun=models.CharField(blank=True,max_length=4, null=True)


    Jan=models.CharField(blank=True,max_length=4, null=True)
    Feb=models.CharField(blank=True,max_length=4, null=True)
    Mar=models.CharField(blank=True,max_length=4, null=True)
    Apr=models.CharField(blank=True,max_length=4, null=True)
    May=models.CharField(blank=True,max_length=4, null=True)
    Jun=models.CharField(blank=True,max_length=4, null=True)
    Jul=models.CharField(blank=True,max_length=4, null=True)
    Aug=models.CharField(blank=True,max_length=4, null=True)
    Sep=models.CharField(blank=True,max_length=4, null=True)
    Oct=models.CharField(blank=True,max_length=4, null=True)
    Nov=models.CharField(blank=True,max_length=4, null=True)
    Dec=models.CharField(blank=True,max_length=4, null=True)

    nModBoil=models.IntegerField(default=4)
    nLoops=models.IntegerField(default=1)
    I_bn_des = models.FloatField(default=950)
    x_b_des=models.FloatField(blank=True, null=True)
    heat_sink_dP_frac=models.FloatField(blank=True, null=True)
    theta_dep=models.FloatField(blank=True, null=True)
    theta_stow=models.FloatField(blank=True, null=True)
    V_wind_max=models.FloatField(blank=True, null=True)
    ColAz=models.FloatField(blank=True, null=True)
    T_amb_des_sf=models.FloatField(blank=True, null=True)
    SCA_drives_elec=models.FloatField(blank=True, null=True)
    Pipe_hl_coef=models.FloatField(blank=True, null=True)
    csp_lf_sf_water_per_wash=models.FloatField(blank=True, null=True)
    csp_lf_sf_washes_per_year=models.IntegerField(blank=True, null=True)
    fP_hdr_c=models.FloatField(blank=True, null=True)
    fP_sf_boil=models.FloatField(blank=True, null=True)
    fP_hdr_h=models.FloatField(blank=True, null=True)
    T_fp=models.FloatField(blank=True, null=True)
    eta_pump=models.FloatField(blank=True, null=True)
    e_startup=models.FloatField(blank=True, null=True)
    A_aperture=models.FloatField(default=26.4)
    L_col=models.FloatField(blank=True, null=True)
    TrackingError=models.FloatField(blank=True, null=True)
    GeomEffects=models.FloatField(default=0.632)
    rho_mirror_clean=models.FloatField(blank=True, null=True)
    dirt_mirror=models.FloatField(blank=True, null=True)
    error=models.FloatField(blank=True, null=True)
    IAM_T0=models.FloatField(blank=True, null=True)
    IAM_T1=models.FloatField(blank=True, null=True)
    IAM_T2=models.FloatField(blank=True, null=True)
    IAM_T3=models.FloatField(blank=True, null=True)
    IAM_T4=models.FloatField(blank=True, null=True)
    IAM_L0=models.FloatField(blank=True, null=True)
    IAM_L1=models.FloatField(blank=True, null=True)
    IAM_L2=models.FloatField(blank=True, null=True)
    IAM_L3=models.FloatField(blank=True, null=True)
    IAM_L4=models.FloatField(blank=True, null=True)
    HL_dT_0=models.FloatField(blank=True, null=True)
    HL_dT_1=models.FloatField(blank=True, null=True)
    HL_dT_2=models.FloatField(blank=True, null=True)
    HL_dT_3=models.FloatField(blank=True, null=True)
    HL_dT_4=models.FloatField(blank=True, null=True)
    HL_W_0=models.FloatField(blank=True, null=True)
    HL_W_1=models.FloatField(blank=True, null=True)
    HL_W_2=models.FloatField(blank=True, null=True)
    HL_W_3=models.FloatField(blank=True, null=True)
    HL_W_4=models.FloatField(blank=True, null=True)


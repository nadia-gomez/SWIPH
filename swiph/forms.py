from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
import numpy as np

demandUnitDict=['kWh','MWh','KJ','BTU','kcal']
hourDayDict=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]

class processForm(forms.Form):
    process = forms.CharField(max_length=80)
    size = forms.CharField(max_length=20)

class inputBasicForm(forms.Form):
    location = forms.CharField(max_length=200)
    pressure=forms.FloatField(validators=[MinValueValidator(0)])
    tempIN=forms.FloatField(validators=[MinValueValidator(0)])
    
    demand=forms.FloatField(validators=[MinValueValidator(0)])
    demandUnit=forms.ChoiceField(choices=list(zip(demandUnitDict,demandUnitDict)))
    hourINI=forms.ChoiceField(choices=list(zip(hourDayDict,hourDayDict)))
    hourEND=forms.ChoiceField(choices=list(zip(hourDayDict,hourDayDict)))
    
    Mond=forms.CharField(required=False,max_length=10)
    Tues=forms.CharField(required=False,max_length=10)
    Wend=forms.CharField(required=False,max_length=10)
    Thur=forms.CharField(required=False,max_length=10)
    Fri=forms.CharField(required=False,max_length=10)
    Sat=forms.CharField(required=False,max_length=10)
    Sun=forms.CharField(required=False,max_length=10)

    Jan=forms.CharField(required=False,max_length=10)
    Feb=forms.CharField(required=False,max_length=10)
    Mar=forms.CharField(required=False,max_length=10)
    Apr=forms.CharField(required=False,max_length=10)
    May=forms.CharField(required=False,max_length=10)
    Jun=forms.CharField(required=False,max_length=10)
    Jul=forms.CharField(required=False,max_length=10)
    Aug=forms.CharField(required=False,max_length=10)
    Sep=forms.CharField(required=False,max_length=10)
    Oct=forms.CharField(required=False,max_length=10)
    Nov=forms.CharField(required=False,max_length=10)
    Dec=forms.CharField(required=False,max_length=10)

    Mond_value=forms.FloatField(required=False,validators=[MinValueValidator(0),MaxValueValidator(1)])
    Tues_value=forms.FloatField(required=False,validators=[MinValueValidator(0),MaxValueValidator(1)])
    Wend_value=forms.FloatField(required=False,validators=[MinValueValidator(0),MaxValueValidator(1)])
    Thur_value=forms.FloatField(required=False,validators=[MinValueValidator(0),MaxValueValidator(1)])
    Fri_value=forms.FloatField(required=False,validators=[MinValueValidator(0),MaxValueValidator(1)])
    Sat_value=forms.FloatField(required=False,validators=[MinValueValidator(0),MaxValueValidator(1)])
    Sun_value=forms.FloatField(required=False,validators=[MinValueValidator(0),MaxValueValidator(1)])

    Jan_value=forms.FloatField(required=False,validators=[MinValueValidator(0),MaxValueValidator(1)])
    Feb_value=forms.FloatField(required=False,validators=[MinValueValidator(0),MaxValueValidator(1)])
    Mar_value=forms.FloatField(required=False,validators=[MinValueValidator(0),MaxValueValidator(1)])
    Apr_value=forms.FloatField(required=False,validators=[MinValueValidator(0),MaxValueValidator(1)])
    May_value=forms.FloatField(required=False,validators=[MinValueValidator(0),MaxValueValidator(1)])
    Jun_value=forms.FloatField(required=False,validators=[MinValueValidator(0),MaxValueValidator(1)])
    Jul_value=forms.FloatField(required=False,validators=[MinValueValidator(0),MaxValueValidator(1)])
    Aug_value=forms.FloatField(required=False,validators=[MinValueValidator(0),MaxValueValidator(1)])
    Sep_value=forms.FloatField(required=False,validators=[MinValueValidator(0),MaxValueValidator(1)])
    Oct_value=forms.FloatField(required=False,validators=[MinValueValidator(0),MaxValueValidator(1)])
    Nov_value=forms.FloatField(required=False,validators=[MinValueValidator(0),MaxValueValidator(1)])
    Dec_value=forms.FloatField(required=False,validators=[MinValueValidator(0),MaxValueValidator(1)])


    nLoops=forms.IntegerField(validators=[MinValueValidator(0)])
    nModBoil=forms.IntegerField(validators=[MinValueValidator(0)])

class inputAdvancedForm(forms.Form):

    nLoops=forms.IntegerField(validators=[MinValueValidator(0)])
    nModBoil=forms.IntegerField(validators=[MinValueValidator(0)])
    I_bn_des = forms.FloatField(validators=[MinValueValidator(0),MaxValueValidator(1400)])
    x_b_des=forms.FloatField(validators=[MinValueValidator(0),MaxValueValidator(1)])
    heat_sink_dP_frac=forms.FloatField(validators=[MinValueValidator(0),MaxValueValidator(1)])
    theta_dep=forms.FloatField(validators=[MinValueValidator(0),MaxValueValidator(90)])
    theta_stow=forms.FloatField(validators=[MinValueValidator(0),MaxValueValidator(90)])
    V_wind_max=forms.FloatField(validators=[MinValueValidator(0)])
    ColAz=forms.FloatField(validators=[MinValueValidator(0),MaxValueValidator(360)])
    T_amb_des_sf=forms.FloatField()
    SCA_drives_elec=forms.FloatField(validators=[MinValueValidator(0)])
    Pipe_hl_coef=forms.FloatField(validators=[MinValueValidator(0)])
    csp_lf_sf_water_per_wash=forms.FloatField(validators=[MinValueValidator(0)])
    csp_lf_sf_washes_per_year=forms.IntegerField(validators=[MinValueValidator(0)])
    fP_hdr_c=forms.FloatField(validators=[MinValueValidator(0)])
    fP_sf_boil=forms.FloatField(validators=[MinValueValidator(0)])
    fP_hdr_h=forms.FloatField(validators=[MinValueValidator(0)])
    T_fp=forms.FloatField()
    eta_pump=forms.FloatField(validators=[MinValueValidator(0),MaxValueValidator(1)])
    e_startup=forms.FloatField(validators=[MinValueValidator(0)])
    A_aperture=forms.FloatField(validators=[MinValueValidator(0)])
    L_col=forms.FloatField(validators=[MinValueValidator(0)])
    TrackingError=forms.FloatField(validators=[MinValueValidator(0),MaxValueValidator(1)])
    GeomEffects=forms.FloatField(validators=[MinValueValidator(0),MaxValueValidator(1)])
    rho_mirror_clean=forms.FloatField(validators=[MinValueValidator(0),MaxValueValidator(1)])
    dirt_mirror=forms.FloatField(validators=[MinValueValidator(0),MaxValueValidator(1)])
    error=forms.FloatField(validators=[MinValueValidator(0),MaxValueValidator(1)])
    IAM_T0=forms.FloatField()
    IAM_T1=forms.FloatField()
    IAM_T2=forms.FloatField()
    IAM_T3=forms.FloatField()
    IAM_T4=forms.FloatField()
    IAM_L0=forms.FloatField()
    IAM_L1=forms.FloatField()
    IAM_L2=forms.FloatField()
    IAM_L3=forms.FloatField()
    IAM_L4=forms.FloatField()
    HL_dT_0=forms.FloatField()
    HL_dT_1=forms.FloatField()
    HL_dT_2=forms.FloatField()
    HL_dT_3=forms.FloatField()
    HL_dT_4=forms.FloatField()
    HL_W_0=forms.FloatField()
    HL_W_1=forms.FloatField()
    HL_W_2=forms.FloatField()
    HL_W_3=forms.FloatField()
    HL_W_4=forms.FloatField()

    def clean(self):
        cleaned_data = super().clean()
        HL_dT = [cleaned_data.get("HL_dT_4",0), cleaned_data.get("HL_dT_3",0), cleaned_data.get("HL_dT_2",0), cleaned_data.get("HL_dT_1",0), cleaned_data.get("HL_dT_0",0)]
        HL_W = [cleaned_data.get("HL_W_4",0), cleaned_data.get("HL_W_3",0), cleaned_data.get("HL_W_2",0), cleaned_data.get("HL_W_1",0), cleaned_data.get("HL_W_0",0)]

        HL_dT_roots = np.roots(HL_dT)
        #zeros at real 600>dt>0
        HL_dT_critic_zeros = [root.real for root in HL_dT_roots if root.imag==0 and root.real>0 and root.real<600]
        r_items=[]
        for dT in HL_dT_critic_zeros:
            upper_limit = np.polyval(HL_dT,dT+0.1)
            lower_limit = np.polyval(HL_dT,dT-0.1)
            if np.sign(upper_limit)==np.sign(lower_limit):
                r_items.append(dT)
        for dT in r_items:
            HL_dT_critic_zeros.remove(dT)
        if len(HL_dT_critic_zeros) > 0:
            raise forms.ValidationError("The heat loss polynomial results in a heat gainance at " +HL_dT_critic_zeros+ " temperature differences")

        HL_W_roots = np.roots(HL_W[1:])
        HL_W_critic_zeros = [root.real for root in HL_W_roots if root.imag==0 and root.real>0 and root.real<112]
        for w_velocity in HL_W_critic_zeros:
            loss_factor = np.polyval(HL_W, w_velocity)
            if loss_factor>1:
                raise forms.ValidationError("The factor due the wind velocity becomes greater than"+ loss_factor +"at" +w_velocity+". As if it were earning energy due the wind.")
            elif loss_factor<1:
                raise forms.ValidationError("The factor due the wind velocity becomes negative ("+loss_factor+") at "+w_velocity+" which doesn't have any sense.")

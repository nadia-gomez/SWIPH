#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 1 10:00:56 2019

@author: miguel Frasquet
"""

import PySAM.LinearFresnelDsgIph as LF

import pandas as pd
import numpy as np

def samSim(annualHourly,meteoFile,I_bn_des,T_cold_ref,x_b_des,nLoops,q_pb_des,P_turb_des,heat_sink_dP_frac,
           nModBoil,theta_dep,theta_stow,V_wind_max,ColAz,T_amb_des_sf,SCA_drives_elec,
           Pipe_hl_coef,csp_lf_sf_water_per_wash,csp_lf_sf_washes_per_year,fP_hdr_c,
           fP_sf_boil,fP_hdr_h,T_fp,eta_pump,e_startup,A_aperture,L_col,
           TrackingError,GeomEffects,rho_mirror_clean,dirt_mirror,error,
           IAM_T,IAM_L,HL_dT,HL_W):



    model =LF.new()
    
    # Group Weather
    model.Weather.file_name = meteoFile # Meteo file
    
    
    
    model.Powerblock.T_hot=393 # Hot HTF inlet temperature, from storage tank [C] XXXXXXX
    
    model.Solarfield.sh_OpticalTable=[[ 0,   0 ], [ 0,   0 ]] #Values of the optical efficiency table [none]
    
    errorList=[]
    
    
    
    # @@@@@@@@@@@@@@@@@@@@@@@@ SYSTEM DESIGN @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    
    # <><><><><><><><><><><><>  Design Point - Solar Field Parameters  <><><><><><><><><><><><>
    model.Solarfield.I_bn_des=I_bn_des # Design point irradiation value [W/m2]
    model.Powerblock.T_cold_ref=T_cold_ref # Reference HTF outlet temperature at design [C]
    model.Solarfield.x_b_des=x_b_des #Design point boiler outlet steam quality [none]
    
    model.Solarfield.nLoops=nLoops #Number of loops [none]
    
    # <><><><><><><><><><><><>  Design Point - Heat Sink Parameters  <><><><><><><><><><><><>
    model.Solarfield.q_pb_des=q_pb_des # Design heat input to the power block [MW]
    model.Solarfield.P_turb_des=P_turb_des #Heat sink inlet pressure [bar]
    model.HeatSink.heat_sink_dP_frac=heat_sink_dP_frac #Fractional pressure drop through heat sink
    
    
    # @@@@@@@@@@@@@@@@@@@@@@@@ SOLAR FIELD @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    
    # <><><><><><><><><><><><>  Solar Field Parameters  <><><><><><><><><><><><>
    
    model.Solarfield.nModBoil=nModBoil # Number of modules in the boiler section [none]
    model.Solarfield.theta_dep=theta_dep # Solar elevation for collector morning deploy [deg]
    model.Solarfield.theta_stow=theta_stow # Solar elevation for collector nightime stow [deg]
    model.Solarfield.V_wind_max=V_wind_max #Maximum allowable wind velocity before safety stow [m/s]
    model.Solarfield.ColAz=ColAz # Collector azimuth angle [deg] IMP -> Disabled when OptCharType=1 since the values are taken from the table
    model.Solarfield.T_amb_des_sf=T_amb_des_sf # Design-point ambient temperature [C]
    model.Solarfield.SCA_drives_elec=SCA_drives_elec #Tracking power.. in Watts per m2 [W/m2]
    model.Solarfield.Pipe_hl_coef=Pipe_hl_coef # Loss coefficient from the header.. runner pipe.. and non-HCE pipin [W/m2-K]
    
    # <><><><><><><><><><><><>  Mirror Washing  <><><><><><><><><><><><>
    
    model.Heliostat.csp_lf_sf_water_per_wash=csp_lf_sf_water_per_wash # Water usage per wash [L/m2_aper]
    model.Heliostat.csp_lf_sf_washes_per_year=csp_lf_sf_washes_per_year # Mirror washing annual frequency [-/year]
    
    # <><><><><><><><><><><><>  Steam Design Conditions  <><><><><><><><><><><><>
    
    model.Solarfield.fP_hdr_c=fP_hdr_c #Average design-point cold header pressure drop fraction [none]
    model.Solarfield.fP_sf_boil=fP_sf_boil # Design-point pressure drop across the solar field boiler fraction [none]
    model.Solarfield.fP_hdr_h=fP_hdr_h #Average design-point hot header pressure drop fraction [none]
    model.Solarfield.T_fp=T_fp # Freeze protection temperature (heat trace activation temperature) [C]
    model.Solarfield.eta_pump=eta_pump #Feedwater pump efficiency [none]
    
    # <><><><><><><><><><><><>  Plant Heat Capacity  <><><><><><><><><><><><>
    
    model.Solarfield.e_startup=e_startup # Thermal inertia contribution per sq meter of solar field [kJ/K-m2]
    
    # @@@@@@@@@@@@@@@@@@@@@@@@ COLLECTOR AND RECEIVER @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    
    # <><><><><><><><><><><><>  Geometry and Optical Performance  <><><><><><><><><><><><>
    
    model.Solarfield.A_aperture =A_aperture # Reflective aperture area of the collector module [m^2] (boiler, SH)
    model.Solarfield.L_col=L_col # Active length of the boiler/superheater section collector module [m] (boiler, SH) 
    model.Solarfield.TrackingError=TrackingError # User-defined tracking error derate [none]
    model.Solarfield.GeomEffects=GeomEffects # User-defined geometry effects derate [none] (boiler, SH)
    model.Solarfield.rho_mirror_clean=rho_mirror_clean # User-defined clean mirror reflectivity [none]
    model.Solarfield.dirt_mirror=dirt_mirror # User-defined dirt on mirror derate [none]
    model.Solarfield.error=error # User-defined general optical error derate [none]
    
    # Optical characterization of the collector
    model.Solarfield.OptCharType=[[ 3 ], [ 0 ]]  # The optical characterization method [none] 1-> Solar position Table 2 -> Collector incidence angle table 3-> polynomial IAM
    ## Table
    model.Solarfield.b_OpticalTable=[[ -180,   -160,   -140,   -120,   -100,   -80,   -60,   -40,   -20,   0,   20,   40,   60,   80,   100,   120,   140,   160,   180,   -999.9000244140625 ], [ 0,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 10,   0.98000001907348633,   0.97444498538970947,   0.97197598218917847,   0.97284698486328125,   0.97690999507904053,   0.97690999507904053,   0.97284698486328125,   0.97197598218917847,   0.97444498538970947,   0.98000001907348633,   0.97444498538970947,   0.97197598218917847,   0.97284698486328125,   0.97690999507904053,   0.97690999507904053,   0.97284698486328125,   0.97197598218917847,   0.97444498538970947,   0.98000001907348633 ], [ 20,   0.93000000715255737,   0.92297601699829102,   0.92892998456954956,   0.94600498676300049,   0.95401901006698608,   0.95401901006698608,   0.94600498676300049,   0.92892998456954956,   0.92297601699829102,   0.93000000715255737,   0.92297601699829102,   0.92892998456954956,   0.94600498676300049,   0.95401901006698608,   0.95401901006698608,   0.94600498676300049,   0.92892998456954956,   0.92297601699829102,   0.93000000715255737 ], [ 30,   0.8399999737739563,   0.83861798048019409,   0.87069100141525269,   0.9130210280418396,   0.94091099500656128,   0.94091099500656128,   0.9130210280418396,   0.87069100141525269,   0.83861798048019409,   0.8399999737739563,   0.83861798048019409,   0.87069100141525269,   0.9130210280418396,   0.94091099500656128,   0.94091099500656128,   0.9130210280418396,   0.87069100141525269,   0.83861798048019409,   0.8399999737739563 ], [ 40,   0.72000002861022949,   0.72994697093963623,   0.80368697643280029,   0.86696100234985352,   0.90003901720046997,   0.90003901720046997,   0.86696100234985352,   0.80368697643280029,   0.72994697093963623,   0.72000002861022949,   0.72994697093963623,   0.80368697643280029,   0.86696100234985352,   0.90003901720046997,   0.90003901720046997,   0.86696100234985352,   0.80368697643280029,   0.72994697093963623,   0.72000002861022949 ], [ 50,   0.55000001192092896,   0.59125500917434692,   0.70745402574539185,   0.79350900650024414,   0.83955997228622437,   0.83955997228622437,   0.79350900650024414,   0.70745402574539185,   0.59125500917434692,   0.55000001192092896,   0.59125500917434692,   0.70745402574539185,   0.79350900650024414,   0.83955997228622437,   0.83955997228622437,   0.79350900650024414,   0.70745402574539185,   0.59125500917434692,   0.55000001192092896 ], [ 60,   0.34000000357627869,   0.43217799067497253,   0.59747797250747681,   0.66400599479675293,   0.69351100921630859,   0.69351100921630859,   0.66400599479675293,   0.59747797250747681,   0.43217799067497253,   0.34000000357627869,   0.43217799067497253,   0.59747797250747681,   0.66400599479675293,   0.69351100921630859,   0.69351100921630859,   0.66400599479675293,   0.59747797250747681,   0.43217799067497253,   0.34000000357627869 ], [ 70,   0.12999999523162842,   0.26525399088859558,   0.42558598518371582,   0.46449598670005798,   0.4771060049533844,   0.4771060049533844,   0.46449598670005798,   0.42558598518371582,   0.26525399088859558,   0.12999999523162842,   0.26525399088859558,   0.42558598518371582,   0.46449598670005798,   0.4771060049533844,   0.4771060049533844,   0.46449598670005798,   0.42558598518371582,   0.26525399088859558,   0.12999999523162842 ], [ 80,   0.0099999997764825821,   0.11369399726390839,   0.20891000330448151,   0.23325499892234802,   0.23882800340652466,   0.23882800340652466,   0.23325499892234802,   0.20891000330448151,   0.11369399726390839,   0.0099999997764825821,   0.11369399726390839,   0.20891000330448151,   0.23325499892234802,   0.23882800340652466,   0.23882800340652466,   0.23325499892234802,   0.20891000330448151,   0.11369399726390839,   0.0099999997764825821 ], [ 90,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0 ]]
    ## Polynomial IAMs
    model.Solarfield.IAM_T=IAM_T # Transverse Incident angle modifiers (0,1,2,3,4 order terms) [none]
    model.Solarfield.IAM_L=IAM_L # Longitudinal Incident angle modifiers (0,1,2,3,4 order terms) [none]
    
    
    # <><><><><><><><><><><><>  Receiver Geometry and Heat Loss <><><><><><><><><><><><>
    
    model.Solarfield.HLCharType=[[ 1 ], [ 0 ]]  # Flag indicating the heat loss model type {1=poly.; 2=Forristall} [none]
    
    # Polynomial heat loss model [1] --------------------------------------
    model.Solarfield.HL_dT=HL_dT # Heat loss coefficient - HTF temperature (0,1,2,3,4 order terms) [W/m-K^order]
    model.Solarfield.HL_W=HL_W # Heat loss coef adj wind velocity (0,1,2,3,4 order terms) [1/(m/s)^order]
    
    #Forristall model [2] -----------------------------------
    ## Diameters
    model.Solarfield.D_2=[[ 0.065999999642372131 ], [ 0 ]] # The inner absorber tube diameter [m] (boiler, SH)
    model.Solarfield.D_3=[[ 0.070000000298023224 ], [ 0 ]] # The outer absorber tube diameter [m] (boiler, SH)
    model.Solarfield.D_4=[[ 0.11500000208616257 ], [ 0 ]] # The inner glass envelope diameter [m] (boiler, SH)
    model.Solarfield.D_5=[[ 0.11999999731779099 ], [ 0 ]] # The outer glass envelope diameter [m] (boiler, SH)
    model.Solarfield.D_p=[[ 0 ], [ 0 ]] # The diameter of the absorber flow plug [m]  (boiler, SH)
    ## Internal surface roughness
    model.Solarfield.Rough=[[ 4.5000000682193786e-05 ], [ 0 ]] # Roughness of the internal surface [m]
    ## Absorber flow and material
    model.Solarfield.AbsorberMaterial=[[ 1 ], [ 0 ]] # Absorber material type 1 -> 304L 2 ->216L 3->321H 4->B42 Copper (boiler, SH)
    model.Solarfield.Flow_type=[[ 2 ], [ 0 ]] # The flow type through the absorber 1-> Tube flow 2-> Annular flow [none] (boiler, SH) 
    ## Variations
    model.Solarfield.HCE_FieldFrac=[[ 0.98500001430511475,   0.0099999997764825821,   0.004999999888241291,   0 ], [ 0,   0,   0,   0 ]] # Variant weighting fraction - The fraction of the field occupied by this HCE type (4: # field fracs) [none]
    model.Solarfield.alpha_abs=[[ 0.95999997854232788,   0.95999997854232788,   0.80000001192092896,   0 ], [ 0,   0,   0,   0 ]] # Absorber absorptance (4: # field fracs) [none]
    model.Solarfield.alpha_env=[[ 0.019999999552965164,   0.019999999552965164,   0,   0 ], [ 0,   0,   0,   0 ]] # Envelope absorptance (4: # field fracs) [none]
    model.Solarfield.EPSILON_4= [[ 0.86000001430511475,   0.86000001430511475,   1,   0 ], [ 0,   0,   0,   0 ]] # Inner glass envelope emissivities (Pyrex) (4: # field fracs) [none] (boiler, SH)
    model.Solarfield.Tau_envelope=[[ 0.96299999952316284,   0.96299999952316284,   1,   0 ], [ 0,   0,   0,   0 ]] # Envelope transmittance (4: # field fracs) [none]
    model.Solarfield.GlazingIntactIn=[[ 1,   1,   0,   1 ], [ 0,   0,   0,   0 ]] # The glazing intact flag {true=0; false=1} (4: # field fracs) [none]
    model.Solarfield.AnnulusGas=[[ 1,   1,   1,   1 ], [ 0,   0,   0,   0 ]] # Annulus gas type {1=air; 26=Ar; 27=H2} (4: # field fracs)
    model.Solarfield.P_a=[[ 9.9999997473787516e-05,   750,   750,   0 ], [ 0,   0,   0,   0 ]] # Annulus gas pressure (4: # field fracs) [torr]
    model.Solarfield.Design_loss=[[ 150,   1100,   1500,   0 ], [ 0,   0,   0,   0 ]] # Receiver heat loss at design (4: # field fracs) [W/m]  (boiler, SH)
    model.Solarfield.Shadowing=[[ 0.95999997854232788,   0.95999997854232788,   0.95999997854232788,   0 ], [ 0,   0,   0,   0 ]] # Receiver bellows shadowing loss factor (4: # field fracs) [none]
    model.Solarfield.Dirt_HCE=[[ 0.98000001907348633,   0.98000001907348633,   1,   0 ], [ 0,   0,   0,   0 ]] # Loss due to dirt on the receiver envelope (4: # field fracs) [none] (boiler, SH)
    ### Absorber emittance table
    model.Solarfield.b_eps_HCE1=[[ 0 ], [ 0.13840000331401825 ]] #(temperature) Absorber emittance (eps) [none]
    model.Solarfield.b_eps_HCE2=[[ 0 ], [ 0.64999997615814209 ]] #(temperature) Absorber emittance (eps) [none]
    model.Solarfield.b_eps_HCE3=[[ 0 ], [ 0.64999997615814209 ]] #(temperature) Absorber emittance (eps) [none]
    model.Solarfield.b_eps_HCE4=[[ 0 ], [ 0.13840000331401825 ]] #(temperature) Absorber emittance (eps) [none]
    
    model.Solarfield.sh_eps_HCE1=[[ 0 ], [ 0 ]] #(temperature) Absorber emittance (eps) [none]
    model.Solarfield.sh_eps_HCE2=[[ 0 ], [ 0 ]] #(temperature) Absorber emittance (eps) [none]
    model.Solarfield.sh_eps_HCE3=[[ 0 ], [ 0 ]] #(temperature) Absorber emittance (eps) [none]
    model.Solarfield.sh_eps_HCE4=[[ 0 ], [ 0 ]] #(temperature) Absorber emittance (eps) [none]
    
    
    
    
    # Group AdjustmentFactors
    model.AdjustmentFactors.constant=0 # 0-100 0-> No reduction [%]
    # model.AdjustmentFactors.hourly=[90]*8760
    
    model.execute()
    #Print outputs
    results={'Annual_Field_Energy':int(model.Outputs.annual_field_energy),
    'Thermal_energy_consumption':int(model.Outputs.annual_thermal_consumption),
    'Annual_Energy':int(model.Outputs.annual_energy)}

    
    Q_prod_lim_SAM=np.zeros(8760)
    Q_defocus_SAM=np.zeros(8760)
    
    for i in range(len(model.Outputs.q_dot_to_heat_sink)):
        try:
            if model.Outputs.q_dot_to_heat_sink[i]<=annualHourly[i]/1000:
                Q_prod_lim_SAM[i]=model.Outputs.q_dot_to_heat_sink[i]
                Q_defocus_SAM[i]=0
            else:
                Q_prod_lim_SAM[i]= annualHourly[i]/1000
                Q_defocus_SAM[i]=model.Outputs.q_dot_to_heat_sink[i]-(annualHourly[i]/1000)
        except:       
            Q_prod_lim_SAM[i]=0
            Q_defocus_SAM[i]=0
        
    dataTemp=pd.DataFrame({'step':np.arange(8760),
                        'T_field_cold_in':model.Outputs.T_field_cold_in,
                        'T_field_hot_out':model.Outputs.T_field_hot_out,
                        'T_rec_cold_in':model.Outputs.T_rec_cold_in,
                        'T_rec_hot_out':model.Outputs.T_rec_hot_out,
                        'beam':model.Outputs.beam,
                        'm_dot_field':model.Outputs.m_dot_field,
                        'm_dot_loop':model.Outputs.m_dot_loop,
                        'op_mode_1':model.Outputs.op_mode_1,
                        'op_mode_2':model.Outputs.op_mode_2,
                        'op_mode_3':model.Outputs.op_mode_3,
                        'q_dot_freeze_prot':model.Outputs.q_dot_freeze_prot,
                        'q_dot_piping_loss':model.Outputs.q_dot_piping_loss,
                        'q_dot_rec_abs':model.Outputs.q_dot_rec_abs,
                        'q_dot_rec_inc':model.Outputs.q_dot_rec_inc,
                        'q_dot_rec_thermal_loss':model.Outputs.q_dot_rec_thermal_loss,
                        'q_dot_sf_out':model.Outputs.q_dot_sf_out,
                        'q_dot_to_heat_sink':model.Outputs.q_dot_to_heat_sink,
                        'q_inc_sf_tot':model.Outputs.q_inc_sf_tot,
                        'x_field_hot_out':model.Outputs.x_field_hot_out,
                        'x_rec_hot_out':model.Outputs.x_rec_hot_out,
                        'defocus':model.Outputs.defocus,
                        'eta_opt_ave':model.Outputs.eta_opt_ave,
                        'solazi':model.Outputs.solazi,
                        'solzen':model.Outputs.solzen,
                        'theta_Long':model.Outputs.theta_longitudinal,
                        'theta_Transv':model.Outputs.theta_traverse,
                        'hour_day':model.Outputs.hour_day,
                        'Q_defocus_SAM':Q_defocus_SAM,'Q_prod_lim_SAM':Q_prod_lim_SAM,})
    return(dataTemp,results)


from bokeh.plotting import figure, output_file, show 
from bokeh.embed import components, server_document
#from . import bk_config

import bokeh
from bokeh.plotting import figure, output_file, show
from collections import OrderedDict

from bokeh.core.properties import value
from bokeh.models import ColumnDataSource,CustomJS, Slider, Span,LinearAxis, Range1d,HoverTool,Label,LabelSet,CustomJS, Slider

from bokeh.layouts import gridplot,column,row, widgetbox
import numpy as np

def arraysMonth(Q_prod,Q_prod_lim,DNI,Demand):
 #Para resumen mensual      
    Ene_prod=np.zeros(8760)
    Feb_prod=np.zeros(8760)
    Mar_prod=np.zeros(8760)
    Abr_prod=np.zeros(8760)
    May_prod=np.zeros(8760)
    Jun_prod=np.zeros(8760)
    Jul_prod=np.zeros(8760)
    Ago_prod=np.zeros(8760)
    Sep_prod=np.zeros(8760)
    Oct_prod=np.zeros(8760)
    Nov_prod=np.zeros(8760)
    Dic_prod=np.zeros(8760)
    Ene_prod_lim=np.zeros(8760)
    Feb_prod_lim=np.zeros(8760)
    Mar_prod_lim=np.zeros(8760)
    Abr_prod_lim=np.zeros(8760)
    May_prod_lim=np.zeros(8760)
    Jun_prod_lim=np.zeros(8760)
    Jul_prod_lim=np.zeros(8760)
    Ago_prod_lim=np.zeros(8760)
    Sep_prod_lim=np.zeros(8760)
    Oct_prod_lim=np.zeros(8760)
    Nov_prod_lim=np.zeros(8760)
    Dic_prod_lim=np.zeros(8760)
    Ene_DNI=np.zeros(8760)
    Feb_DNI=np.zeros(8760)
    Mar_DNI=np.zeros(8760)
    Abr_DNI=np.zeros(8760)
    May_DNI=np.zeros(8760)
    Jun_DNI=np.zeros(8760)
    Jul_DNI=np.zeros(8760)
    Ago_DNI=np.zeros(8760)
    Sep_DNI=np.zeros(8760)
    Oct_DNI=np.zeros(8760)
    Nov_DNI=np.zeros(8760)
    Dic_DNI=np.zeros(8760)
    Ene_demd=np.zeros(8760)
    Feb_demd=np.zeros(8760)
    Mar_demd=np.zeros(8760)
    Abr_demd=np.zeros(8760)
    May_demd=np.zeros(8760)
    Jun_demd=np.zeros(8760)
    Jul_demd=np.zeros(8760)
    Ago_demd=np.zeros(8760)
    Sep_demd=np.zeros(8760)
    Oct_demd=np.zeros(8760)
    Nov_demd=np.zeros(8760)
    Dic_demd=np.zeros(8760)

    for i in range(0,8759):
        if (i<=744-1):
            Ene_prod[i]=Q_prod[i]
            Ene_prod_lim[i]=Q_prod_lim[i]
            Ene_DNI[i]=DNI[i]
            Ene_demd[i]=Demand[i]
        if (i>744-1) and (i<=1416-1):
            Feb_prod[i]=Q_prod[i]
            Feb_prod_lim[i]=Q_prod_lim[i]
            Feb_DNI[i]=DNI[i]
            Feb_demd[i]=Demand[i]
        if (i>1416-1) and (i<=2160-1):
            Mar_prod[i]=Q_prod[i]
            Mar_prod_lim[i]=Q_prod_lim[i]
            Mar_DNI[i]=DNI[i]
            Mar_demd[i]=Demand[i]
        if (i>2160-1) and (i<=2880-1):
            Abr_prod[i]=Q_prod[i]
            Abr_prod_lim[i]=Q_prod_lim[i]
            Abr_DNI[i]=DNI[i]
            Abr_demd[i]=Demand[i]
        if (i>2880-1) and (i<=3624-1):
            May_prod[i]=Q_prod[i]
            May_prod_lim[i]=Q_prod_lim[i]
            May_DNI[i]=DNI[i] 
            May_demd[i]=Demand[i]
        if (i>3624-1) and (i<=4344-1):
            Jun_prod[i]=Q_prod[i]
            Jun_prod_lim[i]=Q_prod_lim[i]
            Jun_DNI[i]=DNI[i] 
            Jun_demd[i]=Demand[i]
        if (i>4344-1) and (i<=5088-1):
            Jul_prod[i]=Q_prod[i]
            Jul_prod_lim[i]=Q_prod_lim[i]
            Jul_DNI[i]=DNI[i]
            Jul_demd[i]=Demand[i]
        if (i>5088-1) and (i<=5832-1):
            Ago_prod[i]=Q_prod[i]
            Ago_prod_lim[i]=Q_prod_lim[i]
            Ago_DNI[i]=DNI[i] 
            Ago_demd[i]=Demand[i]
        if (i>5832-1) and (i<=6552-1):
            Sep_prod[i]=Q_prod[i]
            Sep_prod_lim[i]=Q_prod_lim[i]
            Sep_DNI[i]=DNI[i]
            Sep_demd[i]=Demand[i]
        if (i>6552-1) and (i<=7296-1):
            Oct_prod[i]=Q_prod[i]
            Oct_prod_lim[i]=Q_prod_lim[i]
            Oct_DNI[i]=DNI[i]
            Oct_demd[i]=Demand[i]
        if (i>7296-1) and (i<=8016-1):
            Nov_prod[i]=Q_prod[i]
            Nov_prod_lim[i]=Q_prod_lim[i]
            Nov_DNI[i]=DNI[i]
            Nov_demd[i]=Demand[i]
        if (i>8016-1):
            Dic_prod[i]=Q_prod[i]
            Dic_prod_lim[i]=Q_prod_lim[i]
            Dic_DNI[i]=DNI[i]
            Dic_demd[i]=Demand[i]
    array_de_meses=[np.sum(Ene_prod),np.sum(Feb_prod),np.sum(Mar_prod),np.sum(Abr_prod),np.sum(May_prod),np.sum(Jun_prod),np.sum(Jul_prod),np.sum(Ago_prod),np.sum(Sep_prod),np.sum(Oct_prod),np.sum(Nov_prod),np.sum(Dic_prod)]
    array_de_meses_lim=[np.sum(Ene_prod_lim),np.sum(Feb_prod_lim),np.sum(Mar_prod_lim),np.sum(Abr_prod_lim),np.sum(May_prod_lim),np.sum(Jun_prod_lim),np.sum(Jul_prod_lim),np.sum(Ago_prod_lim),np.sum(Sep_prod_lim),np.sum(Oct_prod_lim),np.sum(Nov_prod_lim),np.sum(Dic_prod_lim)]   
    array_de_DNI=[np.sum(Ene_DNI),np.sum(Feb_DNI),np.sum(Mar_DNI),np.sum(Abr_DNI),np.sum(May_DNI),np.sum(Jun_DNI),np.sum(Jul_DNI),np.sum(Ago_DNI),np.sum(Sep_DNI),np.sum(Oct_DNI),np.sum(Nov_DNI),np.sum(Dic_DNI)]
    array_de_demd=[np.sum(Ene_demd),np.sum(Feb_demd),np.sum(Mar_demd),np.sum(Abr_demd),np.sum(May_demd),np.sum(Jun_demd),np.sum(Jul_demd),np.sum(Ago_demd),np.sum(Sep_demd),np.sum(Oct_demd),np.sum(Nov_demd),np.sum(Dic_demd)]
    array_de_fraction=np.zeros(12)

    return array_de_meses,array_de_meses_lim,array_de_DNI,array_de_demd,array_de_fraction

def production_b(plot_width,plot_height,Q_prod,Q_prod_lim,DNI,Demand):

    array_de_meses,array_de_meses_lim,array_de_DNI,array_de_demd,array_de_fraction=arraysMonth(Q_prod,Q_prod_lim,DNI,Demand)
    
    array_de_DNI=np.divide(array_de_DNI,1000)
    Radiation=array_de_DNI
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    Net_Production = array_de_meses_lim
    source = ColumnDataSource(data=dict(months=months, Net_Production=Net_Production))

    Gross_Production=array_de_meses
    source2 = ColumnDataSource(data=dict(months=months, Gross_Production=Gross_Production))

    Demand=array_de_demd
    source3 = ColumnDataSource(data=dict(months=months, Demand=Demand))

    p = figure(plot_width=plot_width, plot_height=plot_height,sizing_mode='scale_width',x_range=months, toolbar_location=None)

    p.x_range.bounds = (0.5, 12.5)

   
    p.vbar(x=months, top=Demand, width=0.9, legend='Demand',
        line_color='white', fill_color='black')

    p.vbar(x=months, top=Gross_Production, width=0.9, legend='Defocused',
        line_color='white', fill_color='grey')

    p.vbar(x=months, top=Net_Production, width=0.9, legend='Net Production',
        line_color='white', fill_color='blue')

  
    max_all=max(max(array_de_demd),max(array_de_meses))

    p.y_range = Range1d(0, 1.1*max_all,bounds=(0, 1.1*max_all))
    p.yaxis.axis_label = 'Production'
    p.extra_y_ranges = {"radiation": Range1d(start=0, end=1.1*max(Radiation),bounds=(0, 1.1*max(Radiation)))}
    p.add_layout(LinearAxis(y_range_name="radiation", axis_label='Radiation'), 'right')

    p.line([0.5, 1.5, 2.5, 3.5, 4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5], Radiation, y_range_name='radiation',line_width=2, color='red')

    p.legend.label_text_font_size = '8pt'
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"
    p.legend.background_fill_color = '#e0e0e0'
    new_legend = p.legend[0]
    p.legend[0].plot = None
    p.add_layout(new_legend, 'above')
 

    p.left[0].formatter.use_scientific = False
    p.yaxis[1].major_label_text_color = "red" 
    p.yaxis[1].axis_label_text_color = "red" 
    p.x_range.range_padding = 0.1
 
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    
    p.background_fill_color = None
    p.border_fill_color = None


    #Store components 
    script, div = components(p)
    return [script,div]
        

 
def storage_b(plot_width,plot_height,ini_x,end_x,Q_prod,Q_charg,Q_prod_lim,Q_useful,Demand,Q_defocus,Q_discharg,SOC):

    p = figure(plot_width=plot_width, plot_height=plot_height, x_range=Range1d(ini_x,end_x,bounds=(0, 8760)), tools='pan,box_zoom,reset' ,toolbar_location='right')



    p.vbar(x=list(range(0, len(Demand))), top=Q_prod, width=0.7, color='blue',legend='Net production')
    p.vbar(x=list(range(0, len(Demand))), top=Q_prod_lim+Q_charg+Q_defocus, bottom=Q_prod_lim+Q_charg,width=0.7, color='#A2A9AB',legend='Defocused')


    line3=p.line(list(range(0, len(Demand))), Demand, line_width=2, color='black',legend='Demand')
    #p.add_tools(HoverTool(renderers=[line3], tooltips=[('Q_charg',"$y")]))



    p.y_range = Range1d(0, 1.05*max(Demand),bounds=(0, 1.05*max(Demand)))
    p.yaxis.axis_label = 'Q_prod'
    #p.extra_y_ranges = {"SOC": Range1d(0, 100, bounds=(0, 100))}
    #p.add_layout(LinearAxis(y_range_name="SOC", axis_label="State of charge [%]"), 'right')
    #
    #p.line(list(range(0, len(Demand))), SOC, y_range_name='SOC',line_dash='dotted',line_width=1, color='red',legend="SOC")

    p.xaxis.ticker = list(range(0,8760,7*24))
    p.xaxis.major_label_overrides = { 7*24: 'Week'+' 1 - '+'January', 
                                    2*7*24: 'Week'+' 2 - '+'January',
                                    3*7*24: 'Week'+' 3 - '+'January',
                                    4*7*24: 'Week'+' 4 - '+'January',
                                    5*7*24: 'Week'+' 5 - '+'January',
                                    6*7*24: 'Week'+' 1 - '+'Feb', 
                                    7*7*24: 'Week'+' 2 - '+'Feb',
                                    8*7*24: 'Week'+' 3 - '+'Feb',
                                    9*7*24: 'Week'+' 1 - '+'Mar',
                                    10*7*24: 'Week'+' 2 - '+'Mar',
                                    11*7*24: 'Week'+' 3 - '+'Mar',
                                    12*7*24: 'Week'+' 4 - '+'Mar', 
                                    13*7*24: 'Week'+' 1 - '+'Apr',
                                    14*7*24: 'Week'+' 2 - '+'Apr',
                                    15*7*24: 'Week'+' 3 - '+'Apr',
                                    16*7*24: 'Week'+' 4 - '+'Apr',
                                    17*7*24: 'Week'+' 5 - '+'Apr',
                                    18*7*24: 'Week'+' 1 - '+'May', 
                                    19*7*24: 'Week'+' 2 - '+'May',
                                    20*7*24: 'Week'+' 3 - '+'May',
                                    21*7*24: 'Week'+' 4 - '+'May',
                                    22*7*24: 'Week'+' 1 - '+'Jun',
                                    23*7*24: 'Week'+' 2 - '+'Jun',
                                    24*7*24: 'Week'+' 3 - '+'Jun', 
                                    25*7*24: 'Week'+' 4 - '+'Jun',
                                    26*7*24: 'Week'+' 1 - '+'Juj',
                                    27*7*24: 'Week'+' 2 - '+'Juj',
                                    28*7*24: 'Week'+' 3 - '+'Juj',
                                    29*7*24: 'Week'+' 4 - '+'Juj',
                                    30*7*24: 'Week'+' 1 - '+'Aug', 
                                    31*7*24: 'Week'+' 2 - '+'Aug',
                                    32*7*24: 'Week'+' 3 - '+'Aug',
                                    33*7*24: 'Week'+' 4 - '+'Aug',
                                    34*7*24: 'Week'+' 5 - '+'Aug',
                                    35*7*24: 'Week'+' 1 - '+'Sept',
                                    36*7*24: 'Week'+' 2 - '+'Sept', 
                                    37*7*24: 'Week'+' 3 - '+'Sept',
                                    38*7*24: 'Week'+' 4 - '+'Sept',
                                    39*7*24: 'Week'+' 1 - '+'Oct',
                                    40*7*24: 'Week'+' 2 - '+'Oct',
                                    41*7*24: 'Week'+' 3 - '+'Oct',
                                    42*7*24: 'Week'+' 4 - '+'Oct', 
                                    43*7*24: 'Week'+' 1 - '+'Nov',
                                    44*7*24: 'Week'+' 2 - '+'Nov',
                                    45*7*24: 'Week'+' 3 - '+'Nov',
                                    46*7*24: 'Week'+' 4 - '+'Nov',
                                    47*7*24: 'Week'+' 5 - '+'Nov',
                                    48*7*24: 'Week'+' 1 - '+'Dec', 
                                    49*7*24: 'Week'+' 2 - '+'Dec',
                                    50*7*24: 'Week'+' 3 - '+'Dec',
                                    51*7*24: 'Week'+' 4 - '+'Dec',
                                    52*7*24: 'Week'+' 5 - '+'Dec'}

    #p.yaxis[1].major_label_text_color = "red" 
    #p.yaxis[1].axis_label_text_color = "red" 
    #p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None
    p.legend.label_text_font_size = '10pt'
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"
    p.legend.click_policy="hide"
    new_legend = p.legend[0]
    p.legend[0].plot = None
    p.add_layout(new_legend, 'below')


    p.background_fill_color = None
    p.border_fill_color = None
 

    p.xgrid.grid_line_color = None


 #Store components 
    script, div = components(p)
    return [script,div]

def first_positive(y):       
    for i in range(0,len(y)):
        if y[i] > 0:
            return i+1

def finance_b2(plot_width,plot_height,n_years_sim,Acum_FCF,FCF,m_dot_min_kgs,steps_sim,AmortYear,Selling_price,lang_text):

    x = list(range(0,25))
    investment=Selling_price


    initialInvest=np.zeros(len(x))

    initialInvest[0]=-investment


    plot = figure(y_range=(-investment*2.1, investment*2), x_range=Range1d(-.5, 20.5,bounds=(-.5, 20.5)), plot_width=plot_width, plot_height=plot_height,toolbar_location=None)
    plot.vbar(x=list(range(0,25)), top=FCF, width=0.7, color='blue',legend=lang_text['det_128'])
    #plot.vbar(x=list(range(0,25)), top=inputFile['net_savings'], width=0.7, color='#489C49',legend="Net Savings")
    #plot.vbar(x=list(range(0,25)), top=inputFile['OM'], width=0.7, color='red',legend="O&M")

            
    plot.left[0].formatter.use_scientific = False
            
    #plot.line(list(range(0,25)), inputFile['Savings'],  line_width=3, line_alpha=0.6)



    y=np.zeros(len(x))

    for i in range(0,len(x)):
        if i==0:
            y[i]=-investment
        else:     
            y[i]=y[i-1]+FCF[i]

    amortYear=first_positive(y)-1
            
    source = ColumnDataSource(data=dict(x=x, y=y,savings=FCF,invest=initialInvest))

    source2=ColumnDataSource(data=dict(x=[0], y=[-investment],year=[amortYear]))



    plot.vbar(x='x', top='y',source=source2, width=0.7, color='#E31E4C',legend=lang_text['det_118'])
    plot.line('x', 'y', source=source, line_width=3, color='black',line_alpha=0.6)
    plot.circle('x', 'y', source=source, color='black', fill_color="white", size=4, legend=lang_text['det_129'])
    #plot.circle('x', 'y', source=source2, fill_color="red", size=4)
    hline = Span(location=0, dimension='width', line_color='#7E7F80', line_width=1)



    label = Label(x=11,y=-investment*1.8,text=lang_text['det_127'])
    label2 = LabelSet(x=16.5,y=-investment*1.8,text='year',source=source2)

    plot.add_layout(label)
    plot.add_layout(label2)

    plot.xaxis.axis_label = lang_text['det_117']
    plot.yaxis.axis_label = lang_text['det_126']


    plot.renderers.extend([ hline])


    plot.title.text = lang_text['det_130']
    #plot.xgrid.grid_line_color = None
    plot.axis.minor_tick_line_color = None
    plot.outline_line_color = None
    plot.legend.label_text_font_size = '10pt'
    plot.legend.orientation = "horizontal"
    plot.legend.location = "top_left"
    plot.legend.click_policy="hide"

    new_legend = plot.legend[0]
    plot.legend[0].plot = None
    plot.add_layout(new_legend, 'above')

    plot.background_fill_color = None
    plot.border_fill_color = None






    callback = CustomJS(args=dict(source=source,source2=source2), code="""                
        var data = source.data;
        var amort= source2.data;
        var inv=inv.value
    
        
        var B = offset.value;
        var x = data['x']
        var y = data['y']
        var savings=data['savings']
        var invest=data['invest']

        var E=amort['year']
        var F=amort['y']

        for (var i = 0; i < x.length; i++) {
            if (i==0){
            y[i] = invest[0]*B
            }
            else {
            y[i] = y[i-1]+savings[i]
            }
            
        }
        function find(list) {
            for (var j = 0; j < list.length; j++) {
                if (y[j]>0){
                return j;
                }
        
            }
        }

        F[0]=y[0]
        E[0]=find(y)

        source2.change.emit();
        source.change.emit();
    """)
    #callback.args["inv"] = -212775

    #amp_slider = Slider(start=0.1, end=10, value=1, step=.1,title="Amplitude", callback=callback)
    #callback.args["amp"] = amp_slider
    #
    #freq_slider = Slider(start=0.1, end=10, value=1, step=.1,
    #                     title="Frequency", callback=callback)
    #callback.args["freq"] = freq_slider
    #
    #phase_slider = Slider(start=0, end=6.4, value=0, step=.1,
    #                      title="Phase", callback=callback)
    #callback.args["phase"] = phase_slider

    offset_slider = Slider(start=0, end=2, value=1, step=.1,title=lang_text['det_146'], callback=callback, bar_color="#E31E4C")
    callback.args["offset"] = offset_slider
    callback.args["inv"] = investment



    layout = column(
        plot,
        widgetbox( offset_slider),
    )

    #Store components 
    script, div = components(layout)
    return [script,div]
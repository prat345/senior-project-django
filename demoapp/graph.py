import plotly.express as px
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import numpy as np
import pandas as pd
from .mongo import get_incident, get_all_video

# color1 = '#4da6ff' # auto
# color2 = '#8cff66' # manual
# color3 = 'teal'
color4 = 'red' # con1
color5 = 'blue' # con2
selected_font = 'Verdana'
bg_color = 'white'

def make_plot(df,topic,yaxis,incident_d):
    fig = go.Figure()
    fig = fig.add_trace(go.Scatter(x=df['elasped_time'], y=df[topic], mode='lines', name=yaxis,
                         fill='tozeroy'
                        ))
    fig.update_layout(margin=dict(l=0, r=10, t=0, b=0),
                height=250,
                font_family=selected_font,
                xaxis_title="Elaspe Time", yaxis_title=yaxis,
                # paper_bgcolor=bg_color,
                # plot_bgcolor=bg_color,
                xaxis=dict(
                    tickmode='linear',
                    tick0=0,
                    dtick=60
                    ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5
                    )
                )
    fig.update_traces(
                line_color='rgb(21, 220, 138)',fillcolor='rgba(23, 250, 170, 0.2)', line_width=1,
                hovertemplate="<b>value: %{y} </b><br>"+"<b>time: %{x} </b><br>"
                )
    
    con1 = pd.Series(incident_d['loc1'])
    con2 = pd.Series(incident_d['loc2'])
    t_con1 = df.iloc[con1]['elasped_time']
    t_con2 = df.iloc[con2]['elasped_time']

    fig.add_trace(go.Scatter(mode='markers',x=t_con2,
                            y=np.ones(len(df))*0,
                            marker_symbol='y-up',
                            marker_line_color=color5, opacity=1,
                            marker_line_width=1, marker_size=10,
                            name='Condition 2'
                            ))
    fig.add_trace(go.Scatter(mode='markers',x=t_con1,
                            y=np.ones(len(df))*0,
                            marker_symbol='y-down',
                            marker_line_color=color4, opacity=1,
                            marker_line_width=1, marker_size=10,
                            name='Condition 1'
                            ))
    return fig

def waypoint_chart(df, incident_d, testdrive, station_wp):
    testdrive = testdrive.replace('-','')
    testdrive = testdrive.replace('Chula','CU')
    vehicle,operator,location,date = testdrive.split('_')
    submap = station_wp.loc[location].loc[vehicle]

    con1 = pd.Series(incident_d['loc1'])
    con2 = pd.Series(incident_d['loc2'])

    if 'NBTC' in testdrive.upper():
        tick = 20
    else:
        tick = 50 
    fig = go.Figure()
    fig.add_trace(go.Scatter(mode="markers", x=submap['x'], y=submap['y'], marker_symbol='circle',
                            marker_color='#FFCCFF', marker_line_color='black',
                            marker_line_width=0.5, opacity=1,
                            marker_size=50,
                            name='stations'
                            ))
    fig.add_trace(go.Scatter(x=df['pose.position.x'], y=df['pose.position.y'],mode='lines',
                            name='Route', line_color='rgb(51, 204, 51)',
                            line_width = 3, opacity=0.6,
                            ))
    fig.add_trace(go.Scatter(x=np.array(df['pose.position.x'][0]), y=np.array(df['pose.position.y'][0]),
                            marker_symbol='triangle-up',
                            marker_line_color="black", marker_color="yellow",
                            marker_line_width=1.5, marker_size=15,name='start'
                            ))
    fig.add_trace(go.Scatter(mode="markers", x=df.iloc[con2]['pose.position.x'], y=df.iloc[con2]['pose.position.y'], 
                            marker_symbol='y-up',
                            marker_line_color=color5, marker_color=color5,
                            marker_line_width=1.5, marker_size=15,name='condition 2'
                            ))
    fig.add_trace(go.Scatter(mode="markers", x=df.iloc[con1]['pose.position.x'], y=df.iloc[con1]['pose.position.y'], 
                            marker_symbol='y-down',
                            marker_line_color=color4, marker_color=color4,
                            marker_line_width=1, marker_size=15,name='condition 1'
                            ))
    fig.update_traces(
                customdata = df['elasped_time'], 
                hovertemplate="<b>x: %{x} </b><br>" +
                "<b>y: %{y} </b><br>" +
                "time: %{customdata}"
    )
    fig.update_layout(
                margin=dict(l=10, r=10, t=0, b=20),
                # height=700,
                # width=1000,
                font_family=selected_font,
                # paper_bgcolor=bg_color,
                # plot_bgcolor=bg_color,
                xaxis=dict(tickmode='linear',tick0=0,dtick=tick),
                xaxis_range=[min(df['pose.position.x'])-tick,max(df['pose.position.x'])+tick],
                yaxis_range=[min(df['pose.position.y'])-tick,max(df['pose.position.y'])+tick],
                xaxis_title="X(m)",
                yaxis_title="Y(m)",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5
                    )
                )

    return fig

def make_chart1(info_df):
    fig = px.bar(info_df.dropna(subset='mileages'), x='testdrive', y='mileages',
                hover_data=['p_auto', 'p_manual'], color='p_auto',
                height=450, 
                text_auto='.2s',
                color_continuous_scale='viridis_r')
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig.update_layout(margin=dict(l=0, r=10, t=0, b=0),
                      font_family=selected_font,
                    #   paper_bgcolor=bg_color,
                    #   plot_bgcolor=bg_color,
                    yaxis_range=[0, max(info_df['mileages'])*1.2],
                    xaxis_title="Testdrive",
                    yaxis_title="Mileages(m)",
                    )
    return fig

def make_chart2(info,var):
    info['d_auto'] = info['mileages']*info['p_auto']/100
    by_var = info.groupby(var)
    by_var = by_var.sum(numeric_only=True)
    by_var['p_auto'] = by_var['d_auto']/by_var['mileages']*100
    by_var = by_var.round(0).sort_index()
    total_mil = round(by_var['mileages'].sum())
    auto_list = by_var['p_auto']
    manual_list = 100-by_var['p_auto']
    index = by_var.index
    fig = go.Figure()
    fig.add_trace(go.Bar(x=index, y=auto_list, name='Auto',
                        text=[f'{i}%' for i in auto_list],
                        width = 0.5,
                        marker_color='royalblue'))
    fig.add_trace(go.Bar(x=index, y=manual_list, name='Manual',
                        text=[f'{i}%' for i in manual_list],
                        width = 0.5,
                        marker_color='limegreen'))
    fig.update_layout(margin=dict(l=0, r=10, t=0, b=0),
                      height=245,
                      font_family=selected_font,
                    #   paper_bgcolor=bg_color,
                    #   plot_bgcolor=bg_color,
                      barmode='stack',
                    #   xaxis_title=var,
                      yaxis_title="Percentages",
                      legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="center",
                            x=0.5
                            ))
    fig.update_traces(
                textfont_size=13, textangle=0, textposition="inside", insidetextanchor="middle", cliponaxis=False,
                hovertemplate="<b>%{x} </b><br>" +
                "<b>%{y} </b><br>"
                )

    fig2 = px.pie(names=index,values=by_var['mileages'], height=200, hole=0.7,
                  color_discrete_sequence=px.colors.sequential.RdBu_r)
    fig2.update_traces(hovertemplate=None, textposition='outside',
                       textinfo='label', rotation=180,
                       )
    fig2.update_layout(margin=dict(l=0, r=0, t=0, b=0),
                       font_family=selected_font,
                    #    paper_bgcolor=bg_color,
                    #    plot_bgcolor=bg_color,
                        showlegend=False)
    fig2.add_annotation(dict(x=0.5, y=0.5,  align='center',
                            xref = "paper", yref = "paper",
                            showarrow = False, font_size=20,
                            text=f'{str(total_mil)} m'))
    return fig, fig2

def incident_num_chart():
    incident_d = get_incident()
    videoDB = get_all_video({'tags':{"$ne": ""}})
    print(len(videoDB))
    data = {'all':{},'actual':{}}
    for testdrive,dic in incident_d.items():
        if type(dic) is dict:
            con1 = dic['Condition1']
            con2 = dic['Condition2']
            num = len(con1+con2)
            # print(testdrive, num)
            data['all'][testdrive] = num
    for dic in videoDB:
        if 'testdrive' in dic.keys():
            testdrive = dic['testdrive']
            if testdrive in data['actual']:
                data['actual'][testdrive] += 1
            else:
                data['actual'][testdrive] = 1
    try:
        data['all'].pop('T1_SL_CU_20221229144347')
        data['actual'].pop('T1_SL_CU_20221229144347')
    except:
        pass
    # data['actual'] = {k.replace('-','')[0:-14]+k.replace('-','')[-3:]:v for k,v in data['actual'].items()}
    # data['all'] = {k.replace('-','')[0:-14]+k.replace('-','')[-3:]:v for k,v in data['all'].items()}
    tick_label = []
    for i in list(data['all'].keys()):
        i = i.replace('-','')
        vehicle,driver,location,date = i.split('_')
        tick_label.append(vehicle+'_'+location+'_'+date[-3:])
    fig = go.Figure()
    fig.add_trace(go.Bar(x=list(data['all'].keys()), y=list(data['all'].values()), name='Predicted',
                        text=list(data['all'].values()),
                        # width = 0.5,
                        marker_color='royalblue'))
    fig.add_trace(go.Bar(x=list(data['actual'].keys()), y=list(data['actual'].values()), name='Ground Truth',
                        text=list(data['actual'].values()),
                        # width = 0.5,
                        marker_color='darkorange'))
    fig.update_layout(margin=dict(l=0, r=10, t=0, b=0),
                      height=475,
                      font_family=selected_font,
                    #   paper_bgcolor=bg_color,
                    #   plot_bgcolor=bg_color,
                      barmode='group',
                      xaxis_title="Testdrive",
                      yaxis_title="Numbers of Incident",
                      legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="center",
                            x=0.5
                            ),
                    xaxis = dict(
                            tickmode = 'array',
                            tickvals = list(data['all'].keys()),
                            ticktext = tick_label
                        )
                    )
    fig.update_traces(textfont_size=13, textangle=0, textposition="outside", insidetextanchor="middle", cliponaxis=False,
                    hovertemplate="<b>%{x} </b><br>" +
                    "<b>incidents: %{y} </b><br>"
                    )

    # fig.show()
    return fig

if __name__ == '__main__':
    from mongo import get_incident, get_all_video
    incident_num_chart()
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import app
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import base64

'''=============================== load data and process data======================================================'''

df = pd.read_excel('fleet_availability_analysis_aitken.xls')
print(df.columns)

df['year'] = pd.to_datetime(df['date']).dt.strftime('%Y')
years = np.unique(df['year'])
machines = np.unique(df['machine_type'])
'''============================== create options list ============================================================='''
year_options =[{'label':'All','value':'All'}]
for i in years:
    year_options.append({'label': i,'value':i})

machine_opts=[]
for i in machines:
    machine_opts.append({'label': i,'value':i})

'''=======================================Define graphs============================================================='''


def availabile_machines_graph(input1,input2):
    if input1 == 'All':
        df2 = df[df['machine_type'] == input2]
    else:
        df2 = df[(df['year'] == input1) & (df['machine_type'] == input2)]
        # updating the plot
    return go.Scatter(x=df2['date'], y=df2['no_of_available_machines '],
                     name='no_of_available_machines ',
                     line=dict(width=2, color='#660066'))


def working_hours_hist(input1,input2):

    color_list = ['#003300','#000066','#e60000','#99003d']

    if input1 == 'All':
        df2 = df[df['machine_type'] == input2]
        graph_color = color_list[1]
    else:
        df2 = df[(df['year'] == input1) & (df['machine_type'] == input2)]
        graph_color = color_list[np.random.randint(0,3)]

    return go.Histogram(x=df2['no_of_working_hours'],
                     name='no_of_working_hours',
                     marker_color=graph_color)


def availability_graph(input1,input2):
    if input1 == 'All':
        df2 = df[df['machine_type'] == input2]
    else:
        df2 = df[(df['year'] == input1) & (df['machine_type'] == input2)]
        # updating the plot
    availability = df2['no_of_available_machines ']/(df2['no_of_available_machines ']+df2['no_of_break_down_machines '])
    return go.Scatter(x=df2['date'], y=availability,
                     name='no_of_available_machines ',
                     line=dict(width=2, color='#660066'))

def availability_boxplot(input1):

    fig_layout = go.Layout(title='Availability Distribution for All Machines',
                             hovermode='closest', plot_bgcolor='#99ffcc', height=550)
    fig = go.Figure(layout=fig_layout)

    color_list = ['#0000ff','#00ff00','#cc0052']
    machine_list = np.unique(df['machine_type'])

    for i in range(len(machine_list)):

        if input1 == 'All':
            df2 = df[df['machine_type'] == machine_list[i]]
        else:
            df2 = df[(df['year'] == input1) & (df['machine_type'] == machine_list[i])]

            # updating the plot
        df2['availability'] = df2['no_of_available_machines ']/(
                df2['no_of_available_machines ']+df2['no_of_break_down_machines '])
        fig.add_trace(go.Box(y=df2['availability'], x=df2['machine_type'], name=machine_list[i], fillcolor=color_list[i]))

    return fig


'''====================================set layouts================================================================='''

trace_1 = availabile_machines_graph(input1= 'All',input2= 'ECH')

fig_layout_1 = go.Layout(title='Available ECH Machines',
                   hovermode='closest', plot_bgcolor='#99ffcc', height=550)
fig_1 = go.Figure(data=[trace_1], layout=fig_layout_1)


trace_2 = working_hours_hist(input1= 'All',input2= 'ECH')

fig_layout_2 = go.Layout(title='ECH Machines Working Hours Distribution',
                   hovermode='closest', plot_bgcolor='#99ffcc', height=550)
fig_2 = go.Figure(data=[trace_2], layout=fig_layout_2)


fig_3 = availability_boxplot(input1='All')



'''================================================================================================================'''
image_filename = 'logo.png'# replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read()).decode('ascii')
website = 'https://themaintenanceblog.wordpress.com/dashboards-for-your-business-no-need-to-spend-thousands-of-dollars-on-erps/'

layout1 = html.Div([
    html.Div([html.A([html.Img(src='data:image/png;base64,{}'.format(encoded_image),style={'float':'left','width':'45px',
                                                                                   'height':'45px'})],href=website),
        html.H5("ECH AVAILABLE MACHINES SUMMARY",style={'padding-top':'15px','font-weight': 'bold',
                                                     'color': '#ffffff',
                                                     'text-align': 'center'}),
    ]),

    dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Main",id='main', active=True, href="/apps/app1")),
                dbc.NavItem(dbc.NavLink("Summary",id='summary', href = '/apps/app2')),
                dbc.NavItem(dbc.NavLink("Help", href="/page2.py")),
                dbc.NavItem(dbc.NavLink("About", disabled=True, href="#")),
                dbc.DropdownMenu(
                    [dbc.DropdownMenuItem("ECH Summary",href = '/apps/app2'), dbc.DropdownMenuItem("LCH Summary",href = '/apps/app2')],
                    label="Summary",
                    nav=True,
                )
            ]
        ),




# adding a plot

    dcc.Link([dcc.Graph(id='plot1', figure=fig_1, style={'position':'relative','padding-left':
    '10px','display': 'inline-block','width':'100%','height':'100%','padding-top':'50px'})], href= '/apps/app2')

])

layout2 = html.Div([
    html.Div([html.A([html.Img(src='data:image/png;base64,{}'.format(encoded_image),style={'float':'left','width':'45px',
                                                                                   'height':'45px'})],href=website),
        html.H5("ECH WORKING HOURS SUMMARY",style={'padding-top':'15px','font-weight': 'bold',
                                                     'color': '#ffffff',
                                                     'text-align': 'center'}),
    ]),

    dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Main",id='main', active=True, href="/apps/app1")),
                dbc.NavItem(dbc.NavLink("Summary",id='summary', href = '/apps/app2')),
                dbc.NavItem(dbc.NavLink("Help", href="/page2.py")),
                dbc.NavItem(dbc.NavLink("About", disabled=True, href="#")),
                dbc.DropdownMenu(
                    [dbc.DropdownMenuItem("ECH Summary",href = '/apps/app2'), dbc.DropdownMenuItem("LCH Summary",href = '/apps/app2')],
                    label="Summary",
                    nav=True,
                )
            ]
        ),




# adding a plot

    dcc.Link([dcc.Graph(id='plot1', figure=fig_2, style={'position':'relative','padding-left':
    '10px','display': 'inline-block','width':'100%','height':'100%','padding-top':'50px'})],href='/apps/app2'),

])

layout3 = html.Div([
    html.Div([html.A([html.Img(src='data:image/png;base64,{}'.format(encoded_image),style={'float':'left','width':'45px',
                                                                                   'height':'45px'})],href=website),
        html.H5("ALL MACHINES AVAILABILITY SUMMARY",style={'padding-top':'15px','font-weight': 'bold',
                                                     'color': '#ffffff',
                                                     'text-align': 'center'}),
    ]),

    dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Main",id='main', active=True, href="/apps/app1")),
                dbc.NavItem(dbc.NavLink("Summary",id='summary', href = '/apps/app2')),
                dbc.NavItem(dbc.NavLink("Help", href="/page2.py")),
                dbc.NavItem(dbc.NavLink("About", disabled=True, href="#")),
                dbc.DropdownMenu(
                    [dbc.DropdownMenuItem("ECH Summary",href = '/apps/app2'), dbc.DropdownMenuItem("LCH Summary",href = '/apps/app2')],
                    label="Summary",
                    nav=True,
                )
            ]
        ),




# adding a plot

    html.Div([dcc.Graph(id='plot1', figure=fig_3, style={'position':'relative','padding-left':
    '10px','display': 'inline-block','width':'100%','height':'100%','padding-top':'50px'}),dcc.Link([html.Button('Go Back',
        name='test', style={'font-weight':'bold','position':'absolute','width':'75px','left':'10px','bottom':'20px','height':'25px'})],
        href='/apps/app2')])

])



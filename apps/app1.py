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


trace_1 = go.Scatter(x=df.date, y=df['no_of_available_machines '],
                     name='no_of_available_machines ', mode='lines',
                     line=dict(width=2, color='rgb(204, 0, 0)'))
fig_layout = go.Layout(title='Time Series Plot',
                   hovermode='closest', plot_bgcolor='#99ffcc', height=550)
fig = go.Figure(data=[trace_1], layout=fig_layout)

image_filename = 'logo.png'# replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read()).decode('ascii')
website = 'https://themaintenanceblog.wordpress.com/dashboards-for-your-business-no-need-to-spend-thousands-of-dollars-on-erps/'
'''================================================================================================================'''


layout = html.Div([
    html.Div([html.A([html.Img(src='data:image/png;base64,{}'.format(encoded_image),style={'float':'left','width':'45px',
                                                                                   'height':'45px'})],href=website),
        html.H5("FLEET PERFORMANCE DASHBOARD",style={'padding-top':'15px','font-weight': 'bold',
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
                    [dbc.DropdownMenuItem("ECH Summary", href='/apps/app2'),
                     dbc.DropdownMenuItem("LCH Summary", href='/apps/app2')],
                    label="Summary",
                    nav=True,
                )
            ]
        ),

    html.P([
        html.Label("Select Graph Type"),
        dcc.Dropdown(id='drop_down_graph',
                     options=[{'label': 'Available Machines', 'value': 'Available Machines'},
                              {'label': 'Working Hours Hist', 'value': 'Working Hours Hist'},
                              {'label': 'Availability Plot', 'value': 'Availability Plot'},
                              {'label': 'Availability Box Plot', 'value': 'Availability Box Plot'},
                              ],
                     value='Availability Box Plot'
                     )
    ], style={'width': '400px',
              'fontSize': '15px',
              'padding-right': '10px',
              'float': 'right',
              'display': 'inline-block'}),

    html.P([
            html.Label("Select Machine Type"),
            dcc.Dropdown(id='drop_down_machine',
                         options=machine_opts,
                         value='ECH'
                         )
        ], style={'width': '300px',
                  'fontSize': '15px',
                  'padding-right': '10px',
                  'float':'right',
                  'display': 'inline-block'}),

    # dropdown year
    html.P([
        html.Label("Select Year"),
        dcc.Dropdown(id='drop_down_year', options=year_options,
                     value='2016')
    ], style={'width': '200px',
              'fontSize': '15px',
              'padding-right': '10px',
              'float':'right',
              'display': 'inline-block'}),


# adding a plot

    html.P([dcc.Graph(id='plot', figure=fig)],style={'float':'right','padding-right': '10px','width':'100%'}),

])


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

    fig = go.Figure()
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

@app.callback(Output('plot', 'figure'),
              [Input('drop_down_year', 'value'),
               Input('drop_down_machine', 'value'),
               Input('drop_down_graph', 'value'),])

def update_figure(input1, input2,input3):

    if input3 == 'Available Machines':
        trace_2 = availabile_machines_graph(input1,input2)
        return go.Figure(data=[trace_2], layout=fig_layout)

    if input3 == 'Working Hours Hist':
        trace_2 = working_hours_hist(input1, input2)
        return go.Figure(data=[trace_2], layout=fig_layout)

    if input3 == 'Availability Plot':
        trace_2 = availability_graph(input1, input2)
        return go.Figure(data=[trace_2], layout=fig_layout)

    if input3 == 'Availability Box Plot':
        trace_2 = availability_boxplot(input1)
        return trace_2



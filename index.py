import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import webbrowser

from app import app
from apps import app1, app2,app3

server = app.server
app.layout = html.Div([
    dcc.Location(id='url',pathname='/apps/app1', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/app1':
        return app1.layout
    elif pathname == '/apps/app2':
        return app2.layout
    elif pathname == '/apps/app3/1':
        return app3.layout1
    elif pathname == '/apps/app3/2':
        return app3.layout2
    elif pathname == '/apps/app3/3':
        return app3.layout3
    else:
        return '404'

# or simply open on the default `8050` port


if __name__ == '__main__':
    app.run_server(debug=True)
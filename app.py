import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

external_stylesheets = [
     'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
     'rel': 'stylesheet',
     'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
     'crossorigin': 'anonymous'}]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

df = pd.read_csv('data/nama_10_gdp_1_Data.csv', na_values=':')
df['Value'] = df['Value'].str.replace('.', '')
df['Value'] = df['Value'].str.replace(',', '.').astype(float)

rename = {'Euro area (EA11-2000, EA12-2006, EA13-2007, EA15-2008, EA16-2010, EA17-2013, EA18-2014, EA19)': 'Euro area',
          'Germany (until 1990 former territory of the FRG)': 'Germany',
          'Kosovo (under United Nations Security Council Resolution 1244/99)': 'Kosovo'}
df['GEO'] = df['GEO'].replace(rename)

available_indicators = df['NA_ITEM'].unique()
countries = df['GEO'].unique()
units = df['UNIT'].unique()

app.layout = html.Div([
    html.Div([
        html.H1('FINAL PROJECT - EUROSTAT DATA', style={'text-align': 'center', 'marginBottom': 25}),
        html.Div([
            html.H3('Y-AXIS', style={'text-align': 'center'}),
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '30%', 'float': 'left', 'display': 'inline-block'}),

        html.Div([
            html.H3('X-AXIS', style={'text-align': 'center'}),
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Value added, gross'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '30%', 'margin-left': '5%', 'display': 'inline-block'}),

        html.Div([
            html.H3('METRIC', style={'text-align': 'center'}),
            dcc.Dropdown(
                id='unit0',
                options=[{'label': i, 'value': i} for i in units],
                value='Current prices, million euro'
            )
        ],
        style={'width': '30%', 'float': 'right', 'display': 'inline-block'})

    ]),

    dcc.Graph(id='indicator-graphic'),

    html.Div([
        dcc.Slider(
            id='year--slider',
            min=df['TIME'].min(),
            max=df['TIME'].max(),
            value=df['TIME'].max(),
            step=None,
            marks={str(year): str(year) for year in df['TIME'].unique()}
        )], style={'marginTop': 20, 'marginBottom': 75, 'marginLeft': 50, 'marginRight': 50}),

    html.Div([
        html.Div([
            html.H3('INDICATOR', style={'text-align': 'center'}),
            dcc.Dropdown(
                id='y-axis-indicator',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            )
        ],
        style={'width': '30%', 'float': 'left', 'display': 'inline-block'}),

        html.Div([
            html.H3('COUNTRY', style={'text-align': 'center'}),
            dcc.Dropdown(
                id='country',
                options=[{'label': i, 'value': i} for i in countries],
                value='European Union - 28 countries'
            )
        ],
        style={'width': '30%', 'margin-left': '5%', 'display': 'inline-block'}),

        html.Div([
            html.H3('METRIC', style={'text-align': 'center'}),
            dcc.Dropdown(
                id='unit',
                options=[{'label': i, 'value': i} for i in units],
                value='Current prices, million euro'
            )
        ],
        style={'width': '30%', 'float': 'right', 'display': 'inline-block'})

    ], style={'marginTop': 50, 'marginBottom': 30}),

    dcc.Graph(id='country-graphic'),

    html.Div(id='intermediate-value', style={'display': 'none'}),

], style={'margin': 30})

@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('yaxis-type', 'value'),
     dash.dependencies.Input('unit0', 'value'),
     dash.dependencies.Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 unit, year_value):
    dff = df[(df['TIME'] == year_value) & (df['UNIT'] == unit)]
    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 60, 'b': 40, 't': 10, 'r': 60},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('country-graphic', 'figure'),
    [dash.dependencies.Input('y-axis-indicator', 'value'),
     dash.dependencies.Input('country', 'value'),
     dash.dependencies.Input('unit', 'value')])
def update_graph(indicator, country, unit):
    dff = df[(df['GEO'] == country) & (df['NA_ITEM'] == indicator) & (df['UNIT'] == unit)]
    return {
        'data': [go.Scatter(
            x=dff['TIME'].unique(),
            y=dff['Value'],
            text=country,
            mode='lines+markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'Years',
                'type': 'linear'
            },
            yaxis={
                'title': indicator,
                'type': 'linear'
            },
            margin={'l': 60, 'b': 40, 't': 10, 'r': 60},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('y-axis-indicator', 'value'),
    [dash.dependencies.Input('yaxis-column', 'value')])
def update_graph(value):
    return value

@app.callback(
    dash.dependencies.Output('unit', 'value'),
    [dash.dependencies.Input('unit0', 'value')])
def update_graph(value):
    return value

if __name__ == '__main__':
    app.run_server()

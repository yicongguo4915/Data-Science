import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import csv
import plotly.graph_objs as go

stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=stylesheet)

server = app.server

UFC = pd.read_csv("UFC Data.csv", encoding = "mac_roman") 

# slice metrics that are measured in percentage (metric1)
metric1 = ['Name', 'Str. Acc.', 'Str. Def', 'TD Acc.', 'TD Def.']
UFCmetric1= UFC[metric1]
UFCmetric1col = UFCmetric1.columns.tolist()[1:]

# slice metrics that are measured in inger (metric2)
metric2 = ['Name', 'SLpM', 'SApM', 'TD Avg.', 'Sub. Avg.']
UFCmetric2= UFC[metric2]
UFCmetric2col = UFCmetric2.columns.tolist()[1:]


def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

WeightClass = UFC['WeightClass'].unique()
Name = UFC['Name'].unique()

app.layout = html.Div(style={'backgroundColor': '#111111', 'height' : '100vh'}, children=[
        html.H1(
            children='UFC - ULTIMATE FIGHTING PREDICTIONS',
            style={'textAlign': 'center', 'color': '#7FDBFF'}),   

        html.Div(style={'width':'55%', 'display' : 'inline-block', 'float':'left'}, children=[
            html.Div(style={'width': '46%', 'float': 'left', 'margin-left':'2%', 'textAlign': 'left'}, children=
            [
                html.Label('Ultimate Fighter 1', 
                style={'color':'#E9ECEF','textAlign': 'center', 'fontSize': '30px'}),

                html.Label('Select Weightclass', style={'color':'#E9ECEF', 'fontSize': '20px'}),
                dcc.Dropdown(
                        id='weight1',
                        options=[{'label': i, 'value': i} for i in WeightClass],
                        value='Welterweight',),

                html.Label('Select Fighter', style={'color':'#E9ECEF','fontSize': '20px'}),
                dcc.Dropdown(
                        id='fighter1',
                        options=[{'label': i, 'value': i} for i in Name],
                        value='Colby Covington',),
                html.Br(),
                html.Div(id = 'info1')
            ]),

            html.Div(style={'width': '46%', 'display':'inline-block', 'margin-left':'4%', 'textAlign': 'left'}, children=
            [
                html.Label('Ultimate Fighter 2', 
                style= {'color':'#E9ECEF','textAlign': 'center','fontSize': '30px'}),

                html.Label('Select Weightclass', style={'color':'#E9ECEF', 'fontSize': '20px'}),
                dcc.Dropdown(
                        id='weight2',
                        options=[{'label': i, 'value': i} for i in WeightClass],
                        value='Welterweight'),

                html.Label('Select Fighter', style={'color':'#E9ECEF','fontSize': '20px'}),
                dcc.Dropdown(
                        id='fighter2',
                        options=[{'label': i, 'value': i} for i in Name],
                        value='Jorge Masvidal',),
                html.Br(),
                html.Div(id = 'info2')
            ]),

            html.Br(),

            html.Div(id='winner', style={'margin-left':'5%', 'display':'inline-block', 'textAlign': 'center', 'color':'#E0E00F', 'fontSize': '35px'}),

            html.Br(),

            html.Br(),

            html.Div([
            dcc.Markdown('''
                    **UFC Metric Breakdown**
            **SLpM** - Significant Strikes Landed per Minute

            **Str. Acc.** - Significant Striking Accuracy

            **SApM** - Significant Strikes Absorbed per Minute

            **Str. Def.** - Significant Strike Defence (the % of opponents strikes that did not land)

            **TD Avg.** - Average Takedowns Landed per 15 minutes"

            **TD Acc.** - Takedown Accuracy"

            **TD Def.** - Takedown Defense (the % of opponents TD attempts that did not land)

            **Sub. Avg.** - Average Submissions Attempted per 15 minutes''')], 
            style={'margin-left' : '4%', 'color':'#E9ECEF', 'textAlign': 'left', 'fontSize': '12px', 'display': 'inline-block'})


        ]),

        html.Div(style={'width':'45%', 'display' : 'inline-block'}, children=[
            dcc.Graph(id='stats1', style={'width' : '90%', 'display':'inline-block', 'margin-left':'5%', 'height' : '43vh'}),
            dcc.Graph(id='stats2', style={'width' : '90%', 'display':'inline-block', 'margin-left':'5%', 'height' : '43vh'})
        ]),
    ])


            
# Call back to delcare the winner of the fighting prediction
@app.callback(
    Output(component_id='winner', component_property='children'),
    [Input(component_id='fighter1', component_property='value'),
     Input(component_id='fighter2', component_property='value')])


def find_winner(fight1name , fight2name):
    fight1ability1 = UFCmetric2[UFCmetric2['Name'] == fight1name].iloc[0, 0:5].values.tolist()[1:]
    fight2ability1 = UFCmetric2[UFCmetric2['Name'] == fight2name].iloc[0, 0:5].values.tolist()[1:]
    fight1ability2 = UFCmetric1[UFCmetric1['Name'] == fight1name].iloc[0, 0:5].values.tolist()[1:]
    fight2ability2 = UFCmetric1[UFCmetric1['Name'] == fight2name].iloc[0, 0:5].values.tolist()[1:]
# unlike UFCmetric2, UFCmetric1 are metrics that are measured in percentage, therefore i need to convert 
# UFCmetric1's scale when calculating fighter's overall ability(times a approriate number, i picked 7)
    fighter1overall = sum(fight1ability1) + sum(fight1ability2) * 7
    fighter2overall = sum(fight2ability1) + sum(fight2ability2) * 7

    if fighter1overall > fighter2overall:   
        text = "Predicted Winner - " + fight1name
    elif fighter1overall < fighter2overall:
        text = "Predicted Winner - " + fight2name
    else:
        text = "Predicted Winner - Can't Decide"

    return text

# call back to list fighter1
@app.callback(
    Output(component_id='fighter1', component_property='options'),
    [Input(component_id='weight1', component_property='value')])

def set_f1_fighter(weightclasses):
    return [{'label': i, 'value': i} for i in UFC[UFC['WeightClass'] == weightclasses]['Name'].sort_values()]

# call back to list fighter2
@app.callback(
    Output(component_id='fighter2', component_property='options'),
    [Input(component_id='weight2', component_property='value')])

def set_f2_fighter(weightclasses):
    return [{'label': i, 'value': i} for i in UFC[UFC['WeightClass'] == weightclasses]['Name'].sort_values()]

# call back to list fighter1 Bio
@app.callback(
    Output(component_id='info1', component_property='children'),
    [Input(component_id='fighter1', component_property='value')])

def update_fighter1_info(f1_name):
    f1_data = UFC[UFC['Name'] == f1_name]
    # print(f1_data)
    record = f1_data['Record'].values[0]
    nickname = f1_data['Nickname'].values[0]
    height = f1_data['Height'].values[0]
    reach = f1_data['Reach'].values[0]
    stance = f1_data['STANCE'].values[0]

    return html.Div([
        html.Div(style={'width' : '100%'}, children=['Record - {}'.format(record)]),
        html.Div(style={'width' : '100%'}, children=['Nickname - {}'.format(nickname)]),
        html.Div(style={'width' : '100%'}, children=['Height - {}'.format(height)]),
        html.Div(style={'width' : '100%'}, children=['Reach - {}'.format(reach)]),
        html.Div(style={'width' : '100%'}, children=['STANCE - {}'.format(stance)])
    ], style={'color':'#E9ECEF', 'fontSize': '13px'})

# call back to list fighter2 Bio
@app.callback(
    Output(component_id='info2', component_property='children'),
    [Input(component_id='fighter2', component_property='value')])

def update_fighter2_info(f2_name):
    f2_data = UFC[UFC['Name'] == f2_name]
    # print(f1_data)
    record = f2_data['Record'].values[0]
    nickname = f2_data['Nickname'].values[0]
    height = f2_data['Height'].values[0]
    reach = f2_data['Reach'].values[0]
    stance = f2_data['STANCE'].values[0]

    return html.Div([
        html.Div(style={'width' : '100%'}, children=['Record - {}'.format(record)]),
        html.Div(style={'width' : '100%'}, children=['Nickname - {}'.format(nickname)]),
        html.Div(style={'width' : '100%'}, children=['Height - {}'.format(height)]),
        html.Div(style={'width' : '100%'}, children=['Reach - {}'.format(reach)]),
        html.Div(style={'width' : '100%'}, children=['STANCE - {}'.format(stance)])
    ], style={'color':'#E9ECEF', 'fontSize': '13px'})

# call back to update stats graph1
@app.callback(
    Output(component_id='stats1', component_property='figure'),
    [Input(component_id='fighter1', component_property='value'),
     Input(component_id='fighter2', component_property='value')])


def update_graph(f1g1,f2g1):
    f1g1x = UFCmetric1[UFCmetric1['Name'] == f1g1].iloc[0, 0:5].values.tolist()[1:5]
    f2g1x = UFCmetric1[UFCmetric1['Name'] == f2g1].iloc[0, 0:5].values.tolist()[1:5]


    return {'data': 

                [go.Bar(
                y=UFCmetric1col,
                x=[x for x in f1g1x],
                name=f1g1, orientation='h'), 
        
                go.Bar(
                y=UFCmetric1col,
                x=[x for x in f2g1x],
                name=f2g1, orientation='h')],
            
            'layout': go.Layout(title = 'Efficiency Stats(in %)', xaxis=dict(tickformat=".2%"))}


# call back to update stats graph2
@app.callback(
    Output('stats2', 'figure'),
    [Input('fighter1', 'value'),
     Input('fighter2', 'value')])


def update_graph2(f1g2,f2g2):
    f1g2x = UFCmetric2[UFCmetric2['Name'] == f1g2].iloc[0, 0:5].values.tolist()[1:]
    f2g2x = UFCmetric2[UFCmetric2['Name'] == f2g2].iloc[0, 0:5].values.tolist()[1:]


    return {'data': 

                [go.Bar(
                y=UFCmetric2col,
                x=[x for x in f1g2x],
                name=f1g2, orientation='h'), 
        
                go.Bar(
                y=UFCmetric2col,
                x=[x for x in f2g2x],
                name=f2g2, orientation='h')],

            'layout': go.Layout(title = 'General Stats')}


if __name__ == '__main__':
    app.run_server(debug=True)
# run it locally on the debug mode 

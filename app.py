# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from urllib.request import urlopen
import json
import os
import choropleth_map
import bars
import pies

#configure Dash app
external_stylesheets = [dbc.themes.MATERIA]
app = Dash(__name__, external_stylesheets = external_stylesheets)
server = app.server
app.css.append_css({'external_url': './assets/app.css'})

#import data
with open('./data/korea_geojson2.geojson', encoding='UTF-8') as f:
    #geojson file to make choropleth map
    data = json.load(f)
for x in data['features']:
    x['id'] = x['properties']['CTP_KOR_NM'] 

#demographic data from 2000 to 2022
#dataset source: https://www.kaggle.com/datasets/alexandrepetit881234/korean-demographics-20002022
demographic = pd.read_csv('./data/Korean_demographics_2000-2022.csv')
demographic['year'] = pd.DatetimeIndex(demographic['Date']).year
mapper = {'Gyeonggi-do': '경기도',
            'Seoul': '서울특별시',
            'Chungcheongbuk-do': '충청북도',
            'Incheon': '인천광역시',
            'Chungcheongnam-do': '충청남도',
            'Gwangju': '광주광역시',
            'Busan': '부산광역시',
            'Gangwon-do': '강원도',
            'Jeollanam-do': '전라남도',
            'Daegu': '대구광역시',
            'Jeollabuk-do': '전라북도',
            'Ulsan': '울산광역시',
            'Jeju-do': '제주특별자치도',
            'Gyeongsangbuk-do': '경상북도',
            'Sejong': '세종특별자치시',
            'Gyeongsangnam-do': '경상남도',
            'Daejeon': '대전광역시'}
demographic['geo_region'] = demographic.Region.map(mapper)

# define colors
colors = {'Birth': ['rgb(255, 211, 51)', 'black'], 
          'Death': ['rgb(216, 141, 216)', 'black'], 
          'Marriage': ['rgb(255, 194, 102)', 'black'], 
          'Divorce': ['rgb(102, 140, 255)', 'black']}
gray = ['lightgray', 'lightgray']         
pie_colors = {'Birth': ['rgb(255, 244, 204)', 'rgb(255, 233, 153)', 'rgb(255, 222, 102)', 'rgb(255, 211, 51)', 'rgb(255, 200, 0)'],
              'Death': ['rgb(242, 217, 242)', 'rgb(229, 179, 229)', 'rgb(216, 141, 216)', 'rgb(203, 103, 203)', 'rgb(190, 65, 190)'],
              'Marriage': ['rgb(255, 235, 204)', 'rgb(255, 214, 153)', 'rgb(255, 194, 102)', 'rgb(255, 173, 51)', 'rgb(255, 153, 0)'],
              'Divorce': ['rgb(204, 217, 255)', 'rgb(153, 179, 255)', 'rgb(102, 140, 255)', 'rgb(51, 102, 255)', 'rgb(0, 64, 255)']}
pie_gray = ['#F2F3F4', '#DADEDF', '#C1C7C9', '#A7AFB2', '#8C979A']
bar_colors = {'Birth': 'rgb(255, 222, 102)',
              'Death': 'rgb(216, 141, 216)',
              'Marriage': 'rgb(255, 194, 102)',
              'Divorce': 'rgb(102, 140, 255)'}
bar_gray = 'lightgray'

#default values
mode = 'All'
range_slider_value = [2000, 2022]
location = 'All'

#define figures
fig_map = choropleth_map.map(demographic, data, mode)
fig_bar_birth_death = bars.bars(demographic, 'Birth and Death', bar_colors, range_slider_value, location)
fig_bar_marriage_divorce = bars.bars(demographic, 'Marriage and Divorce', bar_colors, range_slider_value, location)
fig_pie_birth = pies.pies(demographic, 'Birth', pie_colors, range_slider_value)
fig_pie_death = pies.pies(demographic, 'Death', pie_colors, range_slider_value)
fig_pie_marriage = pies.pies(demographic, 'Marriage', pie_colors, range_slider_value)
fig_pie_divorce = pies.pies(demographic, 'Divorce', pie_colors, range_slider_value)

# function to draw number area
def draw_header_number(colors, mode, demographic):
    childern = [html.P(style={'textAlign': 'center', 'color': colors[mode][0]},
                        children = mode, className = 'content-header'),
                html.H6(style={'textAlign':'center', 'color': colors[mode][1]},
                        children='{}'.format(str(int(demographic[mode].sum()/1000)) + 'K'), className = 'content-number')]
    return childern

#layout
app.layout = dbc.Container(
    dbc.Row([
        dbc.Col([
            dbc.Row([html.Div("KOREA DEMOGRAPHIC 2000-2022", className = 'title'), 
                     html.Div('Birth, death, marriage, and divorce in South Korea from 2000 to 2022')],  style={"background": "white", 'margin-bottom': 3}),
            dbc.Row(
                    [
                    dbc.Col(
                        dbc.Row([
                            dbc.Row([
                                dbc.Col(html.Div([dbc.Label("Types", html_for="radio-items", style = {'font-family': 'Helvetica'}),
                                                dbc.RadioItems(
                                                                id="radio-items",
                                                                options=[
                                                                    {"label": "All", "value": "All"},
                                                                    {"label": "Birth", "value": "Birth"},
                                                                    {"label": "Death", "value": "Death"},
                                                                    {"label": "Marriage", "value": "Marriage"},
                                                                    {"label": "Divorce", "value": "Divorce"},
                                                                ],
                                                                value = 'All',
                                                                className="small",
                                                                inputCheckedClassName="border border-success bg-success",
                                                                inline=True
                                                                )
                                                            ])),  
                                dbc.Col(html.Div([dbc.Label("Year", html_for="range-slider", style = {'font-family': 'Helvetica'}),
                                                dcc.RangeSlider(id="range-slider", 
                                                                min=int(demographic['year'].min()), 
                                                                max=int(demographic['year'].max()), 
                                                                value=[demographic['year'].min(), demographic['year'].max()],
                                                                marks = {2000: '2000',
                                                                        2005: '2005',
                                                                        2010: '2010',
                                                                        2015: '2015',
                                                                        2020: '2020',
                                                                        2022: '2022'})])),
                                    ], style={'margin-bottom': '0.3rem'}),


                            dbc.Row([
                                dbc.Col([
                                    dbc.Row(html.Div([dcc.Graph(
                                                    id='fig_map',
                                                    figure=fig_map
                                                )])),
                                    ], 
                                    width=4, 
                                    style={
                                        "margin-left": "0rem",
                                        "margin-right": "0rem"}),

                                dbc.Col([
                                        #number area
                                        dbc.Row([
                                                dbc.Col(html.Div(
                                                    id = 'text-birth',
                                                    children = draw_header_number(colors, "Birth", demographic)
                                                        ), 
                                                        style={'background-color': 'white'}, 
                                                        className="pretty_container", 
                                                        ),
                                                dbc.Col(html.Div(
                                                    id = 'text-death',
                                                    children=draw_header_number(colors, "Death", demographic)
                                                        ), 
                                                        style={'background-color': 'white'}, 
                                                        className="pretty_container", 
                                                        ),
                                                dbc.Col(html.Div(
                                                    id = 'text-marriage',
                                                    children=draw_header_number(colors, "Marriage", demographic)
                                                ), 
                                                        style={'background-color': 'white'}, 
                                                        className="pretty_container", 
                                                        ),
                                                dbc.Col(html.Div(
                                                    id = 'text-divorce',
                                                    children=draw_header_number(colors, "Divorce", demographic)
                                                ), 
                                                        style={'background-color': 'white'}, 
                                                        className="pretty_container", 
                                                        )
                                                ],  style={'margin-left': '0rem', 'margin-right': '-1rem'}),
                                        #bar and pie graph: birth and death
                                        dbc.Row([
                                            dbc.Col(html.Div([dcc.Graph(
                                                                    id = 'fig_pie_birth',
                                                                    figure = fig_pie_birth
                                                                )], className="pretty_container", style={'margin-left': '0rem', 'margin-right': '-1rem'})),
                                            dbc.Col(html.Div([dcc.Graph(
                                                                    id = 'fig_pie_death',
                                                                    figure = fig_pie_death
                                                                )], className="pretty_container", style={'margin-left': '0rem', 'margin-right': '-1rem'})),
                                            dbc.Col(html.Div([dcc.Graph(
                                                                    id = 'fig_pie_marriage',
                                                                    figure = fig_pie_marriage
                                                                )], className="pretty_container", style={'margin-left': '0rem', 'margin-right': '-1rem'})),
                                            dbc.Col(html.Div([dcc.Graph(
                                                                    id = 'fig_pie_divorce',
                                                                    figure = fig_pie_divorce
                                                                )], className="pretty_container", style={'margin-left': '0rem', 'margin-right': '-1rem'})),
                                        ],  style={'margin-top': '0.3rem'}),
                                        #bar and pie graph: marriage and death
                                        dbc.Row([
                                            dbc.Col(html.Div([dcc.Graph(
                                                                    id='fig_bar_birth_death',
                                                                    figure=fig_bar_birth_death
                                                                )], className="pretty_container", style={'margin-left': '0rem', 'margin-right': '-1rem'})),
                                            dbc.Col(html.Div([dcc.Graph(
                                                                    id='fig_bar_marriage_divorce',
                                                                    figure=fig_bar_marriage_divorce
                                                                )], className="pretty_container", style={'margin-left': '0rem', 'margin-right': '-1rem'})),
                                        ],  style={'margin-top': '0.3rem'}),
                                    ])
                            ]),
                        ])
                    )
                    ], style = {"margin-top": "1rem"}),
            ])
        ])
)

@app.callback(
    Output('fig_map', 'figure'),
    Input('radio-items', 'value'),
    Input('range-slider', 'value')
)
def update_graph(radio_item_value, range_slider_value):
    new_demographic = demographic.loc[(demographic['year'] <= range_slider_value[1])&(demographic['year']>=range_slider_value[0])]
    fig_map = choropleth_map.map(new_demographic, data, radio_item_value)
    return fig_map

@app.callback(
    Output('text-birth', 'children'),
    Output('text-death', 'children'),
    Output('text-marriage', 'children'),
    Output('text-divorce', 'children'),
    Input('radio-items', 'value'),
    Input('fig_map', 'clickData'),
    Input('range-slider', 'value')
)
def update_text(radio_item_value, clickData_map, range_slider_value):
    if(clickData_map == None):
        new_demographic = demographic
        pass
    else:
        location = clickData_map['points'][0]['location']
        new_demographic = demographic.loc[demographic['geo_region'] == location]

    new_demographic = new_demographic.loc[(new_demographic['year'] <= range_slider_value[1])&(new_demographic['year']>=range_slider_value[0])]
    if(radio_item_value == 'All'):
        colors = {'Birth': ['rgb(255, 211, 51)', 'black'], 
          'Death': ['rgb(216, 141, 216)', 'black'], 
          'Marriage': ['rgb(255, 194, 102)', 'black'], 
          'Divorce': ['rgb(102, 140, 255)', 'black']}

    elif(radio_item_value == 'Birth'):
        colors = {'Birth': ['rgb(255, 211, 51)', 'black'], 
                'Death': gray, 
                'Marriage': gray, 
                'Divorce': gray}
    
    elif(radio_item_value == 'Death'):
        colors = {'Birth': gray, 
          'Death': ['rgb(216, 141, 216)', 'black'], 
          'Marriage': gray, 
          'Divorce': gray}
    
    elif(radio_item_value == 'Marriage'):
        colors = {'Birth': gray, 
          'Death': gray, 
          'Marriage': ['rgb(255, 194, 102)', 'black'], 
          'Divorce': gray}
    else:
        colors = {'Birth': gray, 
          'Death': gray, 
          'Marriage': gray, 
          'Divorce': ['rgb(102, 140, 255)', 'black']}


    return draw_header_number(colors, 'Birth', new_demographic), draw_header_number(colors, 'Death', new_demographic), draw_header_number(colors, 'Marriage', new_demographic), draw_header_number(colors, 'Divorce', new_demographic)

@app.callback(
    Output('fig_pie_birth', 'figure'),
    Output('fig_pie_death', 'figure'),
    Output('fig_pie_marriage', 'figure'),
    Output('fig_pie_divorce', 'figure'),
    Input('radio-items', 'value'),
    Input('range-slider', 'value')
)
def update_pies(radio_item_value, range_slider_value):
    new_demographic = demographic.loc[(demographic['year'] <= range_slider_value[1])&(demographic['year']>=range_slider_value[0])]
    if(radio_item_value == 'All'):
        new_pie_colors = pie_colors
    elif(radio_item_value == 'Birth'):
        new_pie_colors = {'Birth': pie_colors['Birth'],
                        'Death': pie_gray,
                        'Marriage': pie_gray,
                        'Divorce': pie_gray}
    elif(radio_item_value == 'Death'):
        new_pie_colors = {'Birth': pie_gray,
                    'Death': pie_colors['Death'],
                    'Marriage': pie_gray,
                    'Divorce': pie_gray}
    elif(radio_item_value == 'Marriage'):
        new_pie_colors = {'Birth': pie_gray,
                    'Death': pie_gray,
                    'Marriage': pie_colors['Marriage'],
                    'Divorce': pie_gray}
    else:
        new_pie_colors = {'Birth': pie_gray,
                    'Death': pie_gray,
                    'Marriage': pie_gray,
                    'Divorce': pie_colors['Divorce']}
    return pies.pies(new_demographic, 'Birth', new_pie_colors, range_slider_value), pies.pies(new_demographic, 'Death', new_pie_colors, range_slider_value), pies.pies(new_demographic, 'Marriage', new_pie_colors, range_slider_value), pies.pies(new_demographic, 'Divorce', new_pie_colors, range_slider_value)

@app.callback(
    Output('fig_bar_birth_death', 'figure'),
    Output('fig_bar_marriage_divorce', 'figure'),
    Input('radio-items', 'value'),
    Input('fig_map', 'clickData'),
    Input('range-slider', 'value')
)
def update_bars(radio_item_value, clickData_map, range_slider_value):
    if(clickData_map == None):
        location = 'All'
        new_demographic = demographic
        pass
    else:
        location = clickData_map['points'][0]['location']
        new_demographic = demographic.loc[demographic['geo_region'] == location]
    new_demographic = new_demographic.loc[(new_demographic['year'] <= range_slider_value[1])&(new_demographic['year']>=range_slider_value[0])]
    
    if(radio_item_value == 'All'):
        new_bar_colors = bar_colors
    elif(radio_item_value == 'Birth'):
        new_bar_colors = {
            'Birth': bar_colors['Birth'],
            'Death': bar_gray,
            'Marriage': bar_gray,
            'Divorce': bar_gray
        }
    elif(radio_item_value == 'Death'):
        new_bar_colors = {
            'Birth': bar_gray,
            'Death': bar_colors['Death'],
            'Marriage': bar_gray,
            'Divorce': bar_gray
        }
    elif(radio_item_value == 'Marriage'):
        new_bar_colors = {
            'Birth': bar_gray,
            'Death': bar_gray,
            'Marriage': bar_colors['Marriage'],
            'Divorce': bar_gray
        }
    elif(radio_item_value == 'Divorce'):
        new_bar_colors = {
            'Birth': bar_gray,
            'Death': bar_gray,
            'Marriage': bar_gray,
            'Divorce': bar_colors['Divorce']
        }
    
   
    return bars.bars(new_demographic, 'Birth and Death', new_bar_colors, range_slider_value, location), bars.bars(new_demographic, 'Marriage and Divorce', new_bar_colors, range_slider_value, location)



if __name__ == '__main__':
    app.run_server(debug=True)
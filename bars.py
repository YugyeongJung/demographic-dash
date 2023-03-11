import plotly.graph_objects as go

def bars(demographic, mode, bar_colors, range_slider_value, location):
    #mode: draw birth_death bars or marriage_divorce bars
    fig_bars = go.Figure()
    demographic = demographic.groupby(['year']).sum().reset_index()
    if(mode == 'Birth and Death'):
        fig_bars.add_trace(go.Bar(x=demographic.year, y=demographic.Birth,
                    base=0,
                    marker_color=bar_colors['Birth'],
                    name='birth',
                    ))
        fig_bars.add_trace(go.Bar(x=demographic.year, y=demographic.Death,
                    base=demographic.Death * -1,
                    marker_color=bar_colors['Death'],
                    name='death'))

    else:
        fig_bars.add_trace(go.Bar(x=demographic.year, y=demographic.Marriage,
                    base=0,
                    marker_color=bar_colors['Marriage'],
                    name='marriage',
                    ))

        fig_bars.add_trace(go.Bar(x=demographic.year, y=demographic.Divorce,
                    base=demographic.Divorce * -1,
                    marker_color=bar_colors['Divorce'],
                    name='divorce'))
                
    fig_bars.update_layout(
            barmode='relative',
            margin=dict(l=20, r=0, t=25, b=0),
            width = 350,
            height = 170,
            plot_bgcolor='white',
            legend=dict(font=dict(size= 8), 
           )
        )
    fig_bars.update_layout(legend_x=1, legend_y=1, font_family = "Roboto-Light", showlegend = False,  
                           title = {'text': '{}: {} - {}, {}'.format(mode, range_slider_value[0], range_slider_value[1], location),
                                    'xanchor': 'center',
                                    'x':0.55},
                           font = dict(
                                        family="Helvetica",
                                        size=9,
                                    ))
    fig_bars.update_yaxes(showticklabels=False)
    fig_bars.update_xaxes(tickfont_size=10)
    return fig_bars

import plotly.graph_objects as go

def pies(demographic, mode, pie_colors, range_slider_value):
    demographic = demographic.groupby(['Region']).sum().reset_index()
    if(mode == 'Birth'):
        demographic = demographic.sort_values(by='Birth')[:5]
        fig_pies = go.Figure(data=[go.Pie(labels=demographic.Region, 
                                          values=demographic.Birth, 
                                          hole=.3,
                                          marker_colors = pie_colors['Birth']
                                         )])
    elif(mode == 'Death'):
        demographic = demographic.sort_values(by='Death')[:5]
        fig_pies = go.Figure(data=[go.Pie(labels=demographic.Region, 
                                          values=demographic.Death, 
                                          hole=.3, 
                                          marker_colors = pie_colors['Death'])])
    elif(mode == 'Marriage'):
        demographic = demographic.sort_values(by='Marriage')[:5]
        fig_pies = go.Figure(data=[go.Pie(labels=demographic.Region, 
                                          values=demographic.Marriage, 
                                          hole=.3,
                                          marker_colors = pie_colors['Marriage'])])
    else:
        demographic = demographic.sort_values(by='Divorce')[:5]
        fig_pies = go.Figure(data=[go.Pie(labels=demographic.Region, 
                                          values=demographic.Divorce, 
                                          hole=.3,
                                          marker_colors = pie_colors['Divorce'])])
    
    fig_pies.update_layout(margin=dict(l=0, r=0, t=25, b=0), 
                           width = 160, 
                           height = 170,
                           showlegend = False,
                           title = {'text': '{}: {} - {}'.format(mode, range_slider_value[0], range_slider_value[1]),
                                    'xanchor': 'center',
                                    'x':0.55},
                           font = dict(
                                        family="Helvetica",
                                        size=9,
                                    )) 
    fig_pies.update_traces(textinfo='label+percent', textposition='inside', textfont_size=7)
    return fig_pies

import plotly.express as px

def map(df_map, data, mode):
    df_sum = df_map.groupby(['Region', 'geo_region']).sum().reset_index()
    df_sum['sum'] = df_sum['Birth'] + df_sum['Death'] + df_sum['Marriage'] + df_sum['Divorce']

    if (mode == 'All'):
        fig_map = px.choropleth_mapbox(
                                        df_sum,
                                        geojson=data, 
                                        locations='geo_region', 
                                        color='sum',
                                        color_continuous_scale=px.colors.sequential.Redor,
                                        mapbox_style="carto-positron",
                                        zoom=5.5, 
                                        center = {"lat": 35.757981, "lon": 127.661132},
                                        opacity=0.6
                                        )
    else: 
        fig_map = px.choropleth_mapbox(
                                        df_sum,
                                        geojson=data, 
                                        locations='geo_region', 
                                        color=mode,
                                        color_continuous_scale=px.colors.sequential.Redor,
                                        mapbox_style="carto-positron",
                                        zoom=5.5, 
                                        center = {"lat": 35.757981, "lon": 127.661132},
                                        opacity=0.6
                                        )
    fig_map.update_coloraxes(showscale=False)
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, 
                        mapbox_style="carto-positron")
    return fig_map
import dash
from dash import dcc
from dash import html
import plotly.express as px
import json
import seaborn as sns
from matplotlib import pyplot as plt

from bars.get_data_bars import *


class Bars():

    def __init__(self, application=None):
        data_bars = init_data_bars()
        data_revenus = init_data_revenus()
        code_commune = init_code_commune()
        barNumber = init_barNumber()
        departements = json.load(open('./bars/data/departements-version-simplifiee.geojson'))

        fig_by_department = px.choropleth_mapbox(barNumber, geojson=departements,
                                                 locations='Département', featureidkey='properties.code',  # join keys
                                                 color='Nombre de bars',
                                                 color_continuous_scale=px.colors.sequential.turbid,
                                                 mapbox_style="carto-positron",
                                                 range_color=(0, 1000),
                                                 zoom=4.5, center={"lat": 47, "lon": 2},
                                                 opacity=0.75,
                                                 labels={'prix': 'Nombre de bars'}
                                                 )
        fig_by_department.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig2 = px.choropleth_mapbox(barNumber.sort_values(by='Nombre de bars'), geojson=departements,
                                    locations='Département', featureidkey='properties.code',  # join keys
                                    color='Nombre de bars', color_continuous_scale=px.colors.sequential.turbid,
                                    mapbox_style="carto-positron",
                                    range_color=(0, 1000),
                                    zoom=3.8, center={"lat": 47, "lon": 2},
                                    opacity=0.75,
                                    animation_frame='Nombre de bars',
                                    labels={'prix': 'Nombre de bars'}
                                    )
        fig2.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

        fig3 = px.density_mapbox(data_bars, lat='Latitude', lon='Longitude', z='Département', radius=4.3,
                                 color_continuous_scale=px.colors.sequential.Plasma,
                                 zoom=4.5, center={"lat": 47, "lon": 2},
                                 mapbox_style="stamen-terrain", )

        fig3.update_layout(mapbox_style="carto-darkmatter")
        fig3.update_layout(margin=dict(b=0, t=0, l=0, r=0))

        fig4 = px.density_mapbox(data_bars, lat='Latitude', lon='Longitude', z='Département', radius=4.3,
                                 animation_frame='Département',
                                 zoom=3.8, center={"lat": 47, "lon": 2},
                                 mapbox_style="stamen-terrain", )

        fig4.update_layout(mapbox_style="carto-darkmatter")
        fig4.update_layout(margin=dict(b=0, t=0, l=0, r=0))

        data_bars_revenus = init_data_bars_revenus(data_bars, data_revenus)
        nbBar_revenu_byCp = init_nbBar_revenu_byCp(data_bars_revenus)
        data_bars_revenus_unique = data_bars_revenus.iloc[:, :6].drop_duplicates().merge(
            nbBar_revenu_byCp[['Postal code', 'Revenu fiscal de référence par foyer fiscal']], on=['Postal code'],
            how='inner')

        fig5 = px.density_mapbox(data_bars_revenus_unique, lat='Latitude', lon='Longitude',
                                 z='Revenu fiscal de référence par foyer fiscal', radius=5,
                                 color_continuous_scale=px.colors.carto.Temps,
                                 zoom=4.5, center={"lat": 47, "lon": 2},
                                 mapbox_style="stamen-terrain", )

        fig5.update_layout(mapbox_style="carto-darkmatter")
        fig5.update_layout(margin=dict(b=0, t=0, l=0, r=0))

        code_postaux_geo = json.load(open('./bars/data/contours-codes-postaux.geojson'))
        tmp = nbBar_revenu_byCp.drop('Revenu fiscal de référence par foyer fiscal', axis=1)
        tmp['Revenu par foyer fiscal'] = nbBar_revenu_byCp['Revenu fiscal de référence par foyer fiscal'].round(
            decimals=1)

        fig6 = px.choropleth_mapbox(tmp, geojson=code_postaux_geo,
                                    locations='Postal code', featureidkey='properties.codePostal',  # join keys
                                    color='Nombre de bars', color_continuous_scale=px.colors.carto.Redor,
                                    mapbox_style="carto-positron",
                                    hover_data=['Revenu par foyer fiscal'],
                                    range_color=(0, 150),
                                    zoom=10, center={"lat": 48.857381, "lon": 2.34453},
                                    opacity=0.75,
                                    labels={'prix': 'Nombre de bars'}
                                    )
        fig6.update_layout(mapbox_style="carto-darkmatter", margin={"r": 0, "t": 0, "l": 0, "b": 0})

        fig7 = px.scatter(data_frame=nbBar_revenu_byCp, x='Nombre de bars',
                          y='Revenu fiscal de référence par foyer fiscal', log_y=True)

        mean_by_bar_number = init_mean_by_bar_number(nbBar_revenu_byCp)
        fig8 = px.line(mean_by_bar_number, x="Nombre de bars", y="Revenu fiscal de référence par foyer fiscal",
                       title='Revenu fiscal de référence moyen en fonction du nombre de bars dans une commune', labels={
                "Revenu fiscal de référence par foyer fiscal": "Revenu fiscal de référence moyen",
            })

        fig9 = px.histogram(data_frame=mean_by_bar_number, x='Revenu fiscal de référence par foyer fiscal',
                            y='Nombre de bars')
        fig10 = px.scatter(data_frame=mean_by_bar_number, y='Revenu fiscal de référence par foyer fiscal',
                           x=mean_by_bar_number['Nombre de bars'], log_y=True)

        nbBar_revenu_byCp = data_bars_revenus.groupby('Nom')[
            'Revenu fiscal de référence par foyer fiscal'].mean().reset_index()
        fig11 = px.scatter(data_frame=nbBar_revenu_byCp, x='Revenu fiscal de référence par foyer fiscal',
                           y=nbBar_revenu_byCp.index, log_y=True,  labels={
                "index": "Bar n°"})

        fig12 = px.scatter(data_frame=nbBar_revenu_byCp, y='Revenu fiscal de référence par foyer fiscal',
                           x=nbBar_revenu_byCp.index, labels={
                "index": "Bar n°",
                "Revenu fiscal de référence par foyer fiscal": "Revenu fiscal de référence moyen",

            }, )
        fig12.update_xaxes(tickformat="0")

        fig13 = px.line(x=np.arange(len(nbBar_revenu_byCp)),
                      y=np.sort(nbBar_revenu_byCp['Revenu fiscal de référence par foyer fiscal']), log_y=True,
                      title='Revenu fiscal de référence des %d bars' % len(nbBar_revenu_byCp), labels={
                "y": "Revenu fiscal de référence par foyer fiscal"})
        fig13.update_xaxes(tickformat="0")
        self.main_layout = html.Div(children=[
            html.H3(children='Répartition des bars en France'),
            dcc.Markdown("""
                    Les bars font partie intégrante de la vie des français.
                Après le boulot, pour fêter un évènement ou encore pour sortir entre amis, on y passe tous un jour.
                
                Leur répartition en France n'est pas homogène, en effet des régions en habritent plus que d'autres.
                Est-ce justifié par le taux de concentration du nombre d'habitant ? Des catégories sociales des habitants? Ou bien simplement d'être breton ?
                
                Nous avons essayé ici de prendre les paramètres géographiques de ces régions afin d'émettre des hypothèses quant à leur répartition en France.

                    """),
            html.Div(
                [dcc.Graph(id='sond_t2', figure=fig_by_department)], style={'width': '100%', }),
            html.Br(),
            dcc.Markdown(""" Sur ce graphique nous pouvons observer le taux de bars par département.
                        Nous remarquons que dans des régions comme la Bretagne, le Nord-Pas-de-Calais ou encore l'Ile de France le nombre de bars est plus élévé que la moyenne."""),
            html.Div(
                [dcc.Graph(id='sond_t2', figure=fig2)], style={'width': '100%', }),
            html.Br(),
            dcc.Markdown("""Les graphiques sont interactifs et s'animent lorsque l'utilisateur clique sur 'Play'"""),
            html.Div(
                [dcc.Graph(id='sond_t2', figure=fig3)], style={'width': '100%', }),
            html.Br(),
            html.Div(
                [dcc.Graph(id='sond_t2', figure=fig4)], style={'width': '100%', }),
            html.Br(),
            html.Div(
                [dcc.Graph(id='sond_t2', figure=fig5)], style={'width': '100%', }),
            html.Br(),
            html.Div(
                [dcc.Graph(id='sond_t2', figure=fig6)], style={'width': '100%', }),
            html.Br(),
            html.Div(
                [dcc.Graph(id='sond_t2', figure=fig7)], style={'width': '100%', }),
            html.Br(),
            html.Div(
                [dcc.Graph(id='sond_t2', figure=fig8)], style={'width': '100%', }),
            html.Br(),
            html.Div(
                [dcc.Graph(id='sond_t2', figure=fig9)], style={'width': '100%', }),
            html.Br(),
            html.Div(
                [dcc.Graph(id='sond_t2', figure=fig10)], style={'width': '100%', }),
            html.Br(),
            html.Div(
                [dcc.Graph(id='sond_t2', figure=fig11)], style={'width': '100%', }),
            html.Br(),
            html.Div(
                [dcc.Graph(id='sond_t2', figure=fig12)], style={'width': '100%', }),
            html.Br(),
            html.Div(
                [dcc.Graph(id='sond_t2', figure=fig13)], style={'width': '100%', }),
            html.Br(),

            dcc.Markdown("""
            En conclusion, nous avons vu que le taux de bars dépendait de :
            * Nombre d'habitants (logique, plus il y a d'habitants plus il y a de bars)
            * Par conséquent du département (là où il y a plus ou moins d'habitants)
            Nous avons aussi cherché à voir si la classe sociale de la population avait un impact sur leur nombre.
            Nous en avons déduit que les communes aux plus petits revenus étaient celles qui possédaient le plus de bars.
            """)
        ], style={
            'backgroundColor': 'white',
            'padding': '10px 50px 10px 50px',
        }
        )

        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout


if __name__ == '__main__':
    bars = Bars()
    bars.app.run_server(debug=True, port=8051)

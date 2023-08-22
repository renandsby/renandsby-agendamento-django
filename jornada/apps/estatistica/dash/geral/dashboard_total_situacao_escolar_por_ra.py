import dash
import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc, html
from django_plotly_dash import DjangoDash
from estatistica.utils import Utils


class Dashboard:
    @staticmethod
    def situacao_escolar_por_ra():
        app = DjangoDash("situacaoescolar")
        ### Situação Escolar
        data = Utils.situacao_escolar_por_ra()
        if data:
            df = pd.DataFrame(
                {
                    "RA": data["ra"],
                    "Situação Escolar": data["situacao"],
                    "Total": data["total"],
                    "total_sum": data["total_sum"],
                }
            )

            # Calculo porcentagem
            df['Percentual'] = (df['Total'] / df['total_sum'] * 100).round(1).astype(str) + "%"
        fig = px.bar(
            df, x="RA", y="Total", text="Percentual", color="Situação Escolar", barmode="relative"
        )
        fig.update_layout(font_size=18, xaxis_tickangle=-45)
        fig.update_yaxes(dtick=1)

        ### Por RA
        data2 = Utils.situacao_escolar_por_ra()
        if data2:
            df2 = pd.DataFrame(
                {
                    "RA": data2["labels_ra"],
                    "Total": data2["total_ra"],
                }
            )
            df2 = df2.sort_values(by="Total")
            df2["percent"] = (
                df2["Total"].apply(lambda x: 100 * x / float(df2["Total"].sum())).values
            )

        #        data3 = Utils.situacao_escolar_por_ra_idade()
        #        if data3:
        #            df3 = pd.DataFrame(
        #                {
        #                    "RA": data3["ras"],
        #                    "Situação Escolar": data3["situacoes"],
        #                    "Idade": data3["idades"],
        #                    "Total": data3["total"],
        #                }
        #            )
        #            print(df3)
        #        fig3 = px.sunburst(
        #            df3, path=["RA", "Situação Escolar", "Idade"], values="Total", color="RA"
        #        )
        #        fig3.update_traces(
        #            textinfo="label+percent entry",
        #            texttemplate="%{label}<br>%{percentEntry:.1%}",
        #            hovertemplate="<b>%{label}</b><br><b>%{percentParent:.1%}</b><br><b>%{value}</b>",
        #            insidetextorientation="radial",
        #        )
        #        fig3.update_layout(font_size=18, margin=dict(t=0, l=0, r=0, b=0))
        #

        ### Gênero
        data4 = Utils.total_por_genero()
        if data4:
            df4 = pd.DataFrame(
                {
                    "Gênero": data4["genero"],
                    "Total": data4["total"],
                }
            )
        fig4 = px.pie(df4, values="Total", names="Gênero")
        fig4.update_traces(textposition="inside", textinfo="percent+value", textfont_size=20)
        fig4.update_layout(title_font_size=30, legend_font_size=20)

        ### Por Idade
        data5 = Utils.total_por_idade()
        if data5:
            df5 = pd.DataFrame(
                {
                    "Unidade": data5["unidades_sigla"],
                    "Total": data5["total"],
                    "Idade": data5["idade_label"],
                }
            )

        app.layout = html.Div(
            style={"backgroundColor": "white"},
            children=[
                html.Div(
                    [
                        html.H2(
                            [
                                html.I(className="fa-solid fa-chart-pie"),
                                " Dados Gerais",
                            ],
                            style={"textAlign": "center", "color": "#777"},
                        ),
                        html.Div(
                            [
                                html.Br(),
                                html.H4(
                                    [
                                        html.I(className="fa-solid fa-venus-mars"),
                                        " Adolescentes por gênero",
                                    ],
                                    style={"textAlign": "center", "color": "#777"},
                                ),
                                dcc.Graph(id='graph-genero', figure=fig4),
                            ],
                            className='col-md-5',
                        ),
                        html.Div(
                            [
                                html.Br(),
                                html.H4(
                                    [
                                        html.I(className="fa-solid fa-child"),
                                        " Adolescentes por idade",
                                    ],
                                    style={"textAlign": "center", "color": "#777"},
                                ),
                                dcc.Graph(id='graph-idade'),
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            df5["Unidade"].unique(),
                                            placeholder="Selecione a unidade...",
                                            id="tipo-column-unidade",
                                        )
                                    ],
                                    style={
                                        "width": "60%",
                                        "display": "block",
                                        "text-align": "center",
                                        "margin": "0 auto",
                                    },
                                ),
                            ],
                            className='col-md-7 text-center',
                        ),
                    ],
                    className='row',
                ),
                html.Div(
                    [
                        html.Br(),
                        html.Br(),
                        html.H2(
                            [
                                html.I(className="fa-solid fa-chart-simple"),
                                " Adolescentes por ra",
                            ]
                        ),
                    ],
                    style={"textAlign": "center", "color": "#777"},
                ),
                html.Br(),
                html.Div(
                    [
                        dcc.Dropdown(
                            df2["RA"].unique(),
                            placeholder="Selecione a RA...",
                            id="tipo-column2",
                        ),
                    ],
                    style={
                        "width": "50%",
                        "display": "block",
                        "text-align": "center",
                        "margin": "0 auto",
                    },
                ),
                dcc.Graph(id="example-graph2"),
                ###
                html.Br(),
                html.Br(),
                html.Div(
                    [
                        html.H2(
                            [
                                html.I(className="fa-solid fa-chart-simple"),
                                " Situação Escolar",
                            ]
                        )
                    ],
                    style={"textAlign": "center", "color": "#777"},
                ),
                html.Br(),
                dcc.Graph(id="example-graph", figure=fig),
                ###
                #                html.Br(),
                #                html.H1(children="RAs", style={"textAlign": "center"}),
                #                html.Div(
                #                    children="""
                #                        Quantitativo de adolescentes por ra, situação escolar e idade.
                #                        """,
                #                    style={"textAlign": "center"},
                #                ),
                #                html.Br(),
                #                dcc.Graph(id="graph-sunburst", figure=fig3),
            ],
        )

        @app.callback(
            Output("example-graph2", "figure"),
            Input("tipo-column2", "value"),
        )
        def byTipoUnidade(tipo_column):
            if tipo_column:
                dff2 = df2[df2["RA"] == tipo_column]
                fig = px.bar(
                    dff2,
                    x="RA",
                    y="Total",
                    text="Total",
                    color="RA",
                    # title="Adolescentes por RA",
                )
                fig.update_layout(font_size=15, xaxis_tickangle=-45)
                fig.update_traces(
                    hovertemplate="<b>%{label}</b><br><b>%{text}</b><br><b>%{y}</b><br>"
                )
                return fig

            fig = px.bar(
                df2,
                x="RA",
                y="Total",
                text=df2["percent"].apply(lambda x: '{0:.1f}%'.format(x)),
                color="RA",
                # title="Adolescentes por ra",
            )
            fig.update_layout(font_size=15, xaxis_tickangle=-45)
            fig.update_traces(hovertemplate="<b>%{label}</b><br><b>%{text}</b><br><b>%{y}</b><br>")
            return fig

        @app.callback(
            dash.dependencies.Output("graph-idade", "figure"),
            [dash.dependencies.Input("tipo-column-unidade", "value")],
        )
        def byTipoUnidade(tipo_column):
            if tipo_column:
                dff = df5[df5["Unidade"] == tipo_column]
                dff['Idade'] = dff['Idade'].astype(str)
                fig = px.bar(
                    dff,
                    x="Idade",
                    y="Total",
                    text="Total",
                    color="Idade",
                    # title="Adolescentes por idade",
                )
                fig.update_yaxes(dtick=1)
                return fig

            df5['Idade'] = df5['Idade'].astype(str)
            df_5 = df5.groupby(['Idade'], as_index=False).sum()
            fig = px.bar(
                df_5,
                x="Idade",
                y="Total",
                text="Total",
                color="Idade",
                # title="Adolescentes por idade",
            )
            return fig

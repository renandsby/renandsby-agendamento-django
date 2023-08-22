import dash
import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc, html
from django_plotly_dash import DjangoDash
from estatistica.utils import Utils


class Dashboard:
    @staticmethod
    def tipo_atividade():
        app = DjangoDash("tipoatividade")
        data = Utils.total_tipo_atividade()
        if data:
            df = pd.DataFrame(
                {
                    "Atividade": data["atividade"],
                    "Total": data["total"],
                }
            )
            app.layout = html.Div(
                style={"backgroundColor": "white"},
                children=[
                    html.H1(children="Unidades", style={"textAlign": "center"}),
                    html.Div(
                        children="""
                            Quantitativo de atividades realizadas por adolescentes.
                            """,
                        style={"textAlign": "center"},
                    ),
                    html.Br(),
                    html.Div(
                        [
                            dcc.Dropdown(
                                df["Atividade"].unique(),
                                placeholder="Selecione o tipo de atividade...",
                                id="tipo-column",
                            ),
                        ],
                        style={
                            "width": "50%",
                            "display": "block",
                            "text-align": "center",
                            "margin": "0 auto",
                        },
                    ),
                    dcc.Graph(id="example-graph"),
                ],
            )

            @app.callback(
                dash.dependencies.Output("example-graph", "figure"),
                [dash.dependencies.Input("tipo-column", "value")],
            )
            def byTipoEntrada(tipo_column):
                if tipo_column:
                    dff = df[df["Atividade"] == tipo_column]
                    fig = px.pie(
                        dff,
                        values="Total",
                        names="Atividade",
                        # title="Tipo de atividade",
                    )
                    fig.update_traces(textposition="inside", textinfo="value", textfont_size=50)
                    fig.update_layout(title_font_size=30, legend_font_size=20)
                    return fig
                fig = px.pie(
                    df,
                    values="Total",
                    names="Atividade",
                    # title="Tipo de atividade",
                    height=500,
                )
                fig.update_traces(textposition="inside", textinfo="percent+value", textfont_size=20)
                fig.update_layout(title_font_size=30, legend_font_size=20)
                return fig

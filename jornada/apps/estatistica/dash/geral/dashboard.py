import dash
import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc, html
from django_plotly_dash import DjangoDash
from estatistica.utils import Utils


class Dashboard:
    @staticmethod
    def por_unidade():
        app = DjangoDash("Geral")
        data = Utils.total_por_unidade()
        if data:
            df = pd.DataFrame(
                {
                    "Unidade": data["unidades_sigla"],
                    "Total": data["total"],
                    "Tipo": data["tipo_unidade_descricao"],
                }
            )
            df = df.sort_values(by="Total")
            app.layout = html.Div(
                style={"backgroundColor": "white"},
                children=[
                    html.H1(children="Unidades", style={"textAlign": "center"}),
                    html.Div(
                        children="""
                            Quantitativo de adolescentes por unidade.
                            """,
                        style={"textAlign": "center"},
                    ),
                    html.Br(),
                    html.Div(
                        [
                            dcc.Dropdown(
                                df["Tipo"].unique(),
                                placeholder="Selecione o tipo de unidade...",
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
            def byTipoUnidade(tipo_column):
                if tipo_column:
                    dff = df[df["Tipo"] == tipo_column]
                    fig = px.bar(
                        dff,
                        x="Unidade",
                        y="Total",
                        text="Total",
                        color="Unidade",
                        # title="Adolescentes por unidade",
                    )
                    return fig

                fig = px.bar(
                    df,
                    x="Unidade",
                    y="Total",
                    text="Total",
                    color="Unidade",
                    # title="Adolescentes por unidade",
                )
                return fig

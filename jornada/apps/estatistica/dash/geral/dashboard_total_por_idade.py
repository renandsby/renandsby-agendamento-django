import dash
import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc, html
from django_plotly_dash import DjangoDash
from estatistica.utils import Utils


class Dashboard:
    @staticmethod
    def por_idade():
        app = DjangoDash("porIdade")
        data = Utils.total_por_idade()
        if data:
            df = pd.DataFrame(
                {
                    "Unidade": data["unidades_sigla"],
                    "Total": data["total"],
                    "Idade": data["idade_label"],
                }
            )
            app.layout = html.Div(
                style={"backgroundColor": "white"},
                children=[
                    html.H1(children="Unidades", style={"textAlign": "center"}),
                    html.Div(
                        children="""
                            Quantitativo de adolescentes por idade.
                            """,
                        style={"textAlign": "center"},
                    ),
                    html.Br(),
                    html.Div(
                        [
                            dcc.Dropdown(
                                df["Unidade"].unique(),
                                placeholder="Selecione a unidade...",
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
                    dff = df[df["Unidade"] == tipo_column]
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

                df['Idade'] = df['Idade'].astype(str)
                df2 = df.groupby(['Idade'], as_index=False).sum()
                fig = px.bar(
                    df2,
                    x="Idade",
                    y="Total",
                    text="Total",
                    color="Idade",
                    # title="Adolescentes por idade",
                )
                return fig

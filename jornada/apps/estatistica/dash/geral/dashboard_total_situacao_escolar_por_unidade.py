import dash
import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc, html
from django_plotly_dash import DjangoDash
from estatistica.utils import Utils


class Dashboard:
    @staticmethod
    def situacao_escolar_por_unidade():
        app = DjangoDash("situacaoescolar")
        data = Utils.situacao_escolar_por_unidade()
        if data:
            df = pd.DataFrame(
                {
                    "Situação Escolar": data["character"],
                    "Unidade": data["parent"],
                    "Total": data["value"],
                }
            )
            fig = px.sunburst(
                df, path=["Unidade", "Situação Escolar"], values="Total", color="Unidade"
            )
            fig.update_traces(
                textinfo="label+percent entry",
                texttemplate="%{label}<br>%{percentEntry:.1%}",
                hovertemplate="<b>Situação Escolar: %{label}</b><br><b>%{percentParent:.1%}</b><br><b>%{value}</b>",
                insidetextorientation="radial",
            )
            fig.update_layout(font_size=18, margin=dict(t=0, l=0, r=0, b=0))

            app.layout = html.Div(
                style={"backgroundColor": "white"},
                children=[
                    html.H1(children="Unidades", style={"textAlign": "center"}),
                    html.Div(
                        children="""
                            Quantitativo de adolescentes por situação escolar.
                            """,
                        style={"textAlign": "center"},
                    ),
                    html.Br(),
                    dcc.Graph(id="example-graph", figure=fig),
                ],
            )

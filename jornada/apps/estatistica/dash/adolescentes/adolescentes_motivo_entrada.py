import dash
import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc, html
from django_plotly_dash import DjangoDash
from datetime import datetime
from estatistica.extracao.adolescentes_motivo_entrada import get_adolescentes_motivo_entrada


@staticmethod
def dashboard_adolescente_motivo_entrada():
    app = DjangoDash("porMotivoEntrada")
    df = pd.DataFrame.from_dict(get_adolescentes_motivo_entrada(), orient="columns")
    df["percent"] = (
        df["tipo_entrada__descricao__count"]
        .apply(lambda x: 100 * x / float(df["tipo_entrada__descricao__count"].sum()))
        .values
    )
    df = df.sort_values(by="tipo_entrada__descricao__count")
    fig = px.bar(
        df,
        x="tipo_entrada__descricao",
        y="tipo_entrada__descricao__count",
        # text="idade__count",
        text=df["percent"].apply(lambda x: '{0:.1f}%'.format(x)),
        labels={
            "tipo_entrada__descricao": "Tipo Entrada",
            "tipo_entrada__descricao__count": "Total",
            "percent": "Percent",
        },
    )
    fig.update_yaxes(
        range=[0, (df["tipo_entrada__descricao__count"].max() + 2)], dtick=1, visible=False
    )
    fig.update_layout(
        font_size=18,
        # paper_bgcolor="rgba(0,0,0,0)",
        # plot_bgcolor="rgba(0,0,0,0)",
        margin_t=40,
        margin_b=10,
    )
    fig.update_traces(
        hovertemplate="<b>Tipo Entrada:</b><b>%{x}</b><br><b>Percent:</b><b>%{text}</b><br><b>Qtd:</b><b>%{y}</b><br>",
        textposition="outside",
    )

    app.layout = html.Div(
        style={"backgroundColor": "white"},
        children=[
            html.Br(),
            html.H2(
                [
                    html.I(className="fa-solid fa-chart-column"),
                    " Percentual de Entradas",
                ],
                style={"textAlign": "center", "color": "#777"},
            ),
            html.Br(),
            html.Div(
                [
                    dcc.Graph(id="example-graph", figure=fig),
                    html.Br(),
                    html.Div(
                        [
                            html.Button("Download csv", id="btn", className="btn btn-primary"),
                            dcc.Download(id="download"),
                        ],
                        className="text-center",
                    ),
                    html.Br(),
                    html.P(
                        ["Fonte: Sistema Jornada - ", datetime.now().strftime("%d/%m/%Y %H:%M")],
                        className="text-muted font-italic p-2",
                    ),
                ]
            ),
        ],
    )

    @app.callback(Output("download", "data"), Input("btn", "n_clicks"), prevent_initial_call=True)
    def generate_csv(n_nlicks):
        return dcc.send_data_frame(df.to_csv, "jornada.csv")

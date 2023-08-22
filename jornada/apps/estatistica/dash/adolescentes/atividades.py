import dash
import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc, html
from django_plotly_dash import DjangoDash
from datetime import datetime
from estatistica.extracao.atividades import get_atividades


@staticmethod
def dashboard_atividades():
    app = DjangoDash("atividades")
    df = pd.DataFrame.from_dict(get_atividades(), orient="columns")
    df["percent"] = (
        df["atividade__descricao__count"]
        .apply(lambda x: 100 * x / float(df["atividade__descricao__count"].sum()))
        .values
    )
    df = df.sort_values(by="atividade__descricao__count")
    fig = px.bar(
        df,
        y="atividade__descricao__count",
        x="atividade__descricao",
        # text="idade__count",
        text=df["percent"].apply(lambda x: '{0:.1f}%'.format(x)),
        labels={
            "atividade__descricao": "Atividade",
            "atividade__descricao__count": "Total",
            "percent": "Percent",
        },
    )
    fig.update_yaxes(
        range=[0, (df["atividade__descricao__count"].max() + 2)], dtick=1, visible=False
    )
    fig.update_layout(
        font_size=18,
        # paper_bgcolor="rgba(0,0,0,0)",
        # plot_bgcolor="rgba(0,0,0,0)",
        margin_t=40,
        margin_b=10,
    )
    fig.update_traces(
        hovertemplate="<b>Atividade:</b><b>%{x}</b><br><b>Percent:</b><b>%{text}</b><br><b>Qtd:</b><b>%{y}</b><br>",
        textposition="outside",
    )

    app.layout = html.Div(
        style={"backgroundColor": "white"},
        children=[
            html.Br(),
            html.H2(
                [
                    html.I(className="fa-solid fa-chart-column"),
                    " Percentual de Atividades",
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

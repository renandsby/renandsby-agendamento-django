import dash
import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc, html
from django_plotly_dash import DjangoDash
from datetime import datetime
from estatistica.extracao.situacao_escolar import get_situacao_escolar


@staticmethod
def dashboard_situacao_escolar():
    external_stylesheets = ["/static/css/bootstrap.min.css"]
    app = DjangoDash("SituacaoEscolar", external_stylesheets=external_stylesheets)
    df = pd.DataFrame.from_dict(get_situacao_escolar(), orient="columns")
    df["percent"] = (
        df["situacao_escolar__descricao__count"]
        .apply(lambda x: 100 * x / float(df["situacao_escolar__descricao__count"].sum()))
        .values
    )
    df = df.sort_values(by="situacao_escolar__descricao__count")
    fig = px.bar(
        df,
        x="situacao_escolar__descricao__count",
        y="situacao_escolar__descricao",
        orientation="h",
        text=df["percent"].apply(lambda x: '{0:.1f}%'.format(x)),
        labels={
            "situacao_escolar__descricao": "Situação Escolar",
            "situacao_escolar__descricao__count": "Total",
            "percent": "Percent",
        },
    )
    fig.update_xaxes(
        range=[0, (df["situacao_escolar__descricao__count"].max() + 2)], dtick=1, visible=False
    )
    fig.update_layout(
        font_size=18,
        # paper_bgcolor="rgba(0,0,0,0)",
        # plot_bgcolor="rgba(0,0,0,0)",
        # margin_r=40,
        # margin_l=10,
    )
    fig.update_traces(
        hovertemplate="<b>Situação Escolar:</b><b>%{y}</b><br><b>Percent:</b><b>%{text}</b><br><b>Qtd:</b><b>%{x}</b><br>",
        textposition="outside",
    )

    app.layout = html.Div(
        style={"backgroundColor": "white"},
        children=[
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

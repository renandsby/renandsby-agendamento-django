import dash
import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc, html
from django_plotly_dash import DjangoDash
from datetime import datetime
from estatistica.extracao.adolescentes_lotados import get_adolescentes_lotados


@staticmethod
def dashboard_adolescentes_lotados():
    external_stylesheets = ["/static/css/bootstrap.min.css"]
    app = DjangoDash("AdolescentesLotados", external_stylesheets=external_stylesheets)
    df = pd.DataFrame.from_dict(get_adolescentes_lotados(), orient="columns")
    df["percent"] = (
        df["unidade__tipo_unidade__descricao__count"]
        .apply(lambda x: 100 * x / float(df["unidade__tipo_unidade__descricao__count"].sum()))
        .values
    )
    df = df.sort_values(by="unidade__tipo_unidade__descricao__count")
    fig = px.bar(
        df,
        y="unidade__tipo_unidade__descricao",
        x="unidade__tipo_unidade__descricao__count",
        orientation="h",
        # text="idade__count",
        text=df["percent"].apply(lambda x: '{0:.1f}%'.format(x)),
        labels={
            "unidade__tipo_unidade__descricao": "Tipo Unidade",
            "unidade__tipo_unidade__descricao__count": "Total",
            "percent": "Percent",
        },
    )
    fig.update_xaxes(
        range=[0, (df["unidade__tipo_unidade__descricao__count"].max() + 2)], dtick=1, visible=False
    )
    fig.update_layout(
        font_size=18,
        # paper_bgcolor="rgba(0,0,0,0)",
        # plot_bgcolor="rgba(0,0,0,0)",
        # margin_r=40,
        # margin_l=10,
    )
    fig.update_traces(
        hovertemplate="<b>Tipo Unidade:</b><b>%{y}</b><br><b>Percent:</b><b>%{text}</b><br><b>Qtd:</b><b>%{x}</b><br>",
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

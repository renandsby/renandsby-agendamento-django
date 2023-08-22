import dash
import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc, html
from django_plotly_dash import DjangoDash
from datetime import datetime
from estatistica.extracao.solicitacoes import get_solicitacoes, get_month


@staticmethod
def dashboard_solicitacoes():
    external_stylesheets = ["/static/css/bootstrap.min.css"]
    app = DjangoDash("Solicitacoes", external_stylesheets=external_stylesheets)
    df = pd.DataFrame.from_dict(get_solicitacoes(), orient="columns")
    if not df.empty:
        df = df.sort_values(by="data_solicitacao")
        df = df.groupby(["mes", "acao_solicitada__descricao"]).sum().reset_index()
        df["mes"] = df["mes"].apply(lambda x: get_month(x)).values
        fig = px.bar(
            df,
            x="mes",
            y=df.columns,
            color="acao_solicitada__descricao",
            barmode="group",
            # markers=True,
            # text="idade__count",
            # text=df["acao_solicitada__descricao__count"],
            labels={
                "mes": "Mês",
                "acao_solicitada__descricao__count": "Total",
                "acao_solicitada__descricao": "Solicitação",
            },
        )
        # fig.update_xaxes(dtick="M1", tickformat="%b\n%Y", ticklabelmode="period")
        fig.update_yaxes(
            # range=[0, (df["acao_solicitada__descricao__count"].max() + 2)],
            # dtick=1,
            visible=False
        )
        fig.update_layout(
            autosize=True,
            font_size=18,
            # paper_bgcolor="rgba(0,0,0,0)",
            # plot_bgcolor="rgba(0,0,0,0)",
            # margin_r=40,
            # margin_l=10,
        )
        fig.update_traces(
            hovertemplate="<b>Mês:</b><b>%{x}</b><br><b>Total:</b><b>%{y}</b>",
            # textposition="outside",
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
                            [
                                "Fonte: Sistema Jornada - ",
                                datetime.now().strftime("%d/%m/%Y %H:%M"),
                            ],
                            className="text-muted font-italic p-2",
                        ),
                    ]
                ),
            ],
        )
    else:
        app = DjangoDash("Solicitacoes", external_stylesheets=external_stylesheets)
        app.layout = html.Div(dcc.Graph())

    @app.callback(Output("download", "data"), Input("btn", "n_clicks"), prevent_initial_call=True)
    def generate_csv(n_nlicks):
        return dcc.send_data_frame(df.to_csv, "jornada.csv")

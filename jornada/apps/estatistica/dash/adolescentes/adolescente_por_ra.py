import dash
import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc, html
from django_plotly_dash import DjangoDash
from estatistica.extracao.adolescentes_por_ra import get_adolescentes_por_ra
from datetime import datetime


@staticmethod
def dashboard_adolescente_por_ra():
    app = DjangoDash("AdolescentePorRa")
    df = pd.DataFrame(get_adolescentes_por_ra())
    df.columns = ["RA", "Quantidade"]
    df["percent"] = df["Quantidade"].apply(lambda x: 100 * x / float(df["Quantidade"].sum())).values

    df = df.sort_values(by="Quantidade")
    fig = px.bar(
        df,
        x="RA",
        y="Quantidade",
        text=df["percent"].apply(lambda x: '{0:.1f}%'.format(x)),
    )
    fig.update_yaxes(range=[0, (df["Quantidade"].max() + 2)], dtick=1, visible=False)
    fig.update_layout(
        font_size=18,
        # paper_bgcolor="rgba(0,0,0,0)",
        # plot_bgcolor="rgba(0,0,0,0)",
        margin_t=40,
        margin_b=10,
    )
    fig.update_traces(
        hovertemplate="<b>RA:</b><b>%{x}</b><br><b>Percent:</b><b>%{text}</b><br><b>Qtd:</b><b>%{y}</b><br>",
        textposition="outside",
    )

    app.layout = html.Div(
        style={"backgroundColor": "white"},
        children=[
            html.Br(),
            html.H2(
                [
                    html.I(className="fa-solid fa-chart-column"),
                    " Adolescentes Por RA",
                ],
                style={"textAlign": "center", "color": "#777"},
            ),
            dcc.Graph(id="adolescente-por-ra", figure=fig),
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
        ],
    )

    @app.callback(Output("download", "data"), Input("btn", "n_clicks"), prevent_initial_call=True)
    def generate_csv(n_nlicks):
        return dcc.send_data_frame(df.to_csv, "jornada.csv")

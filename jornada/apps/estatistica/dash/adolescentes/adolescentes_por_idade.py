import dash
import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc, html
from django_plotly_dash import DjangoDash
from datetime import datetime
from estatistica.extracao.adolescentes_por_idade import get_adolescentes_por_idade


@staticmethod
def dashboard_adolescente_por_idade():
    app = DjangoDash("porIdade")
    df = pd.DataFrame.from_dict(get_adolescentes_por_idade(), orient="columns")
    df["percent"] = (
        df["idade__count"].apply(lambda x: 100 * x / float(df["idade__count"].sum())).values
    )

    app.layout = html.Div(
        style={"backgroundColor": "white"},
        children=[
            html.Br(),
            html.H2(
                [
                    html.I(className="fa-solid fa-chart-column"),
                    " Percentual de Adolescentes Por Idade",
                ],
                style={"textAlign": "center", "color": "#777"},
            ),
            html.Br(),
            html.Div(
                [
                    dcc.Dropdown(
                        df["unidade__sigla"].unique(),
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

    @app.callback(
        dash.dependencies.Output("example-graph", "figure"),
        dash.dependencies.Input("tipo-column", "value"),
    )
    def byTipoUnidade(tipo_column):
        print(tipo_column)
        if tipo_column:
            dff = df[df["unidade__sigla"] == tipo_column]
            dff["percent"] = (
                dff["idade__count"]
                .apply(lambda x: 100 * x / float(dff["idade__count"].sum()))
                .values
            )
            dff['idade'] = dff['idade'].astype(str)
            dff = dff.groupby(['idade'], as_index=False).sum()
            fig = px.bar(
                dff,
                x="idade",
                y="idade__count",
                # text="idade__count",
                text=dff["percent"].apply(lambda x: '{0:.1f}%'.format(x)),
                labels={"idade": "Idade", "idade__count": "Total", "percent": "Percent"}
                # title="Adolescentes por idade",
            )
            fig.update_yaxes(range=[0, (dff["idade__count"].max() + 2)], dtick=1, visible=False)
            fig.update_layout(
                font_size=18,
                # paper_bgcolor="rgba(0,0,0,0)",
                # plot_bgcolor="rgba(0,0,0,0)",
                margin_t=10,
            )
            fig.update_traces(
                hovertemplate="<b>Idade:<b><b>%{x}</b><br><b>Percent:</b><b>%{text}</b><br><b>Qtd:</b><b>%{y}</b><br>",
                textposition="outside",
            )
            return fig

        df['idade'] = df['idade'].astype(str)
        df2 = df.groupby(['idade'], as_index=False).sum()
        fig = px.bar(
            df2,
            x="idade",
            y="idade__count",
            # text="idade__count",
            text=df2["percent"].apply(lambda x: '{0:.1f}%'.format(x)),
            labels={"idade": "Idade", "idade__count": "Total", "percent": "Percent"},
            # title="Adolescentes por idade",
        )
        fig.update_yaxes(range=[0, (df2["idade__count"].max() + 2)], dtick=1, visible=False)
        fig.update_layout(
            font_size=18,
            # paper_bgcolor="rgba(0,0,0,0)",
            # plot_bgcolor="rgba(0,0,0,0)",
            margin_t=40,
            margin_b=10,
        )
        fig.update_traces(
            hovertemplate="<b>Idade:</b><b>%{x}</b><br><b>Percent:</b><b>%{text}</b><br><b>Qtd:</b><b>%{y}</b><br>",
            textposition="outside",
        )
        return fig

import pandas as pd
import os
import plotly.io as pio
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

CURR_PATH = os.path.abspath(os.path.dirname(__file__))
DATA_PATH = os.path.join(CURR_PATH, "widget_data.gzip")

df_all = pd.read_parquet(DATA_PATH)


def make_fig(mstat=2, pwages=80000, swages=0, item=0, businc=0, sstb=0):
    df_filter = df_all.loc[
        (df_all["mstat"] == mstat)
        & (df_all["pwages"] == pwages)
        & (df_all["swages"] == swages)
        & (df_all["mortgage"] == item)
        & (df_all["businc"] == businc)
        & (df_all["sstb"] == sstb)
    ]

    base_trace = go.Scatter(
        x=df_filter["year"],
        y=df_filter["combined_base"],
        name="Current Law",
        hoverinfo="none",
        opacity=0.8,
        mode="lines",
    )
    base_trace.line = {"width": 4}
    biden_trace = go.Scatter(
        x=df_filter["year"],
        y=df_filter["combined_biden"],
        name="Biden 2020 Proposal",
        hoverinfo="none",
        opacity=0.7,
        mode="lines",
    )
    biden_trace.line = {"width": 4}
    layout = go.Layout(yaxis_title="Total Federal Tax Liability", plot_bgcolor="white")
    fig = go.Figure(data=[base_trace, biden_trace], layout=layout)

    fig.update_layout(
        yaxis_tickprefix="$",
        yaxis_tickformat=",.",
        legend=dict(orientation="h", yanchor="bottom", y=1.10, xanchor="left"),
    )
    # fig.update_yaxes(rangemode="tozero")

    return df_filter, fig


app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    url_base_pathname=os.environ.get("URL_BASE_PATHNAME", "/"),
)

widgets = dbc.Col(
    [
        dbc.FormGroup(
            [
                dbc.Label(
                    "Marital Status", style={"margin-top": 20, "margin-left": 20}
                ),
                dcc.Dropdown(
                    id="mstat",
                    options=[
                        {"label": "Single", "value": 1},
                        {"label": "Married", "value": 2},
                    ],
                    value=2,
                    style={"padding-left": 20}
                    # labelStyle={"display": "inline-block"},
                ),
            ]
        ),
        # dbc.FormGroup(
        #     [
        #         dbc.Label("Dependents"),
        #         dcc.Dropdown(
        #             id="deps",
        #             options=[
        #                 {"label": "0 Kids", "value": 0},
        #                 {"label": "1 Kid", "value": 1},
        #                 {"label": "2 Kids", "value": 2},
        #                 {"label": "3 Kids", "value": 3},
        #                 {"label": "4 Kids", "value": 4},
        #             ],
        #             value=0,
        #         ),
        #     ]
        # ),
        dbc.FormGroup(
            [
                html.Div(
                    id="pwages_label", style={"margin-left": 20, "margin-bottom": 10}
                ),
                dcc.Slider(
                    id="pwages",
                    value=80000,
                    min=0,
                    max=1000000,
                    step=20000,
                    updatemode="drag",
                ),
            ]
        ),
        dbc.FormGroup(
            id="swages_container",
            children=[
                html.Div(
                    id="swages_label", style={"margin-left": 20, "margin-bottom": 10}
                ),
                dcc.Slider(
                    id="swages",
                    value=0,
                    min=0,
                    max=1000000,
                    step=20000,
                    updatemode="drag",
                ),
            ],
        ),
        # dbc.FormGroup(
        #     [
        #         html.Div(id='salt_label',
        #             style={'margin-left': 20, 'margin-bottom': 10}),
        #         dcc.Slider(id="salt", value=0, min=0,
        #             max=50000, step=10000, updatemode='drag'),
        #     ]
        # ),
        dbc.FormGroup(
            [
                html.Div(
                    id="item_label", style={"margin-left": 20, "margin-bottom": 10}
                ),
                dcc.Slider(
                    id="item", value=0, min=0, max=100000, step=20000, updatemode="drag"
                ),
            ]
        ),
        dbc.FormGroup(
            [
                html.Div(
                    id="businc_label", style={"margin-left": 20, "margin-bottom": 10}
                ),
                dcc.Slider(
                    id="businc",
                    value=0,
                    min=0,
                    max=1000000,
                    step=20000,
                    updatemode="drag",
                ),
            ]
        ),
        dbc.FormGroup(
            id="sstb_container",
            children=[
                dbc.Label("Type of Business", style={"margin-left": 20}),
                dcc.Dropdown(
                    id="sstb",
                    options=[
                        {"label": "Professional Services", "value": 1},
                        {"label": "Other", "value": 0},
                    ],
                    value=1,
                    style={"padding-left": 20}
                    # labelStyle={"display": "inline-block"},
                ),
            ],
        ),
    ]
)


app.layout = dbc.Container(
    [
        html.H2(
            "How would your taxes change under Joe Biden's Tax Plan?",
            style={"margin-bottom": 10, "padding-top": 20},
        ),
        dcc.Markdown(
            """
            *Powered by [Tax-Cruncher](https://www.ospc.org/tax-cruncher/students)*
            """,
            style={"margin-bottom": 40},
        ),
        # html.Hr(),
        dbc.Row(
            [
                dbc.Col(dbc.Card(widgets), style={"padding-bottom": 100}),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.Row(
                                [
                                    html.P(
                                        "Under Joe Biden's tax plan, your filer's 2021 taxes will:",
                                        style={"margin-left": 30},
                                    ),
                                    html.P("Stay the same", id="diff_label"),
                                ],
                                style={"padding-top": 10},
                            ),
                            dcc.Graph(
                                id="chart",
                                config={"displayModeBar": False},
                                style={"padding-left": 20},
                            ),
                        ]
                    ),
                    style={"padding-bottom": 100},
                    md=8,
                ),
            ],
            align="center",
        ),
    ],
    fluid=True,
    style={"background-color": "#fcfcfc", "height": "100%"},
)


@app.callback(
    # output is figure
    [
        Output("chart", "figure"),
        Output("pwages_label", "children"),
        Output("swages_container", "style"),
        Output("swages_label", "children"),
        Output("item_label", "children"),
        Output("businc_label", "children"),
        Output("sstb_container", "style"),
        Output("diff_label", "children"),
        Output("diff_label", "style"),
    ],
    [
        Input("mstat", "value"),
        Input("pwages", "value"),
        Input("swages", "value"),
        Input("item", "value"),
        Input("businc", "value"),
        Input("sstb", "value"),
    ],
)
def update(mstat, pwages, swages, item, businc, sstb):
    # call function that constructs figure
    if mstat == 2:
        swages_disp = {"display": ""}
    else:
        swages_disp = {"display": "none"}
        swages = 0

    if businc == 0:
        sstb_disp = {"display": "none"}
        sstb = 0
    else:
        sstb_disp = {"display": ""}

    if not isinstance(swages, int):
        swages = 0

    if not isinstance(sstb, int):
        sstb = 0

    df_filter, fig = make_fig(mstat, pwages, swages, item, businc, sstb)

    biden_tax = df_filter[df_filter["year"] == 2021]["combined_biden"]
    base_tax = df_filter[df_filter["year"] == 2021]["combined_base"]
    diff_tax = biden_tax - base_tax

    pwages_str = "Primary Filer Wages: ${:0,.0f}".format(pwages)
    swages_str = "Spouse Wages: ${:0,.0f}".format(swages)
    item_str = "Itemizable Deductions: ${:0,.0f}".format(item)
    businc_str = "Business Income: ${:0,.0f}".format(businc)

    if (diff_tax == 0).bool():
        diff_str = "Stay the same"
        diff_col = {"color": "purple", "margin-left": 10, "font-weight": "bold"}
    elif (diff_tax > 0).bool():
        diff_str = "Increase by ${:0,.0f}".format(abs(diff_tax.to_numpy()[0]))
        diff_col = {"color": "red", "margin-left": 10, "font-weight": "bold"}
    elif (diff_tax < 0).bool():
        diff_str = "Decrease by ${:0,.0f}".format(diff_tax.to_numpy()[0])
        diff_col = {"color": "green", "margin-left": 10, "font-weight": "bold"}

    return (
        fig,
        pwages_str,
        swages_disp,
        swages_str,
        item_str,
        businc_str,
        sstb_disp,
        diff_str,
        diff_col,
    )


server = app.server
# turn debug=False for production
if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=True)

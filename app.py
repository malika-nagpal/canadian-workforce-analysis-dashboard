"""Interactive Canadian Workforce Analysis Dashboard. Run: python app.py"""
from pathlib import Path
import dash
from dash import Input, Output, dcc, html
import pandas as pd
import plotly.express as px

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

essential_services = pd.read_csv(DATA_DIR / "essential_services.csv")
engineering = pd.read_csv(DATA_DIR / "data_engineering.csv")
gender_employment = pd.read_csv(DATA_DIR / "data_gender_employment.csv")

def clean_numeric_columns(frame, columns):
    frame = frame.copy()
    for column in columns:
        frame[column] = pd.to_numeric(
            frame[column].astype(str).str.replace(",", "", regex=False)
            .str.replace('"', "", regex=False).str.strip(),
            errors="coerce",
        )
    return frame

regions = [c for c in essential_services.columns if c not in {"Geography", "Canada"}]
essential_services = clean_numeric_columns(essential_services, regions)
engineering = clean_numeric_columns(engineering, regions)
gender_columns = list(gender_employment.columns[2:])
gender_employment = clean_numeric_columns(gender_employment, gender_columns)

NOC_MAPPING = {
    "0": "0 Legislative and senior management occupations",
    "1": "1 Business, finance and administration occupations",
    "2": "2 Natural and applied sciences and related occupations",
    "3": "3 Health occupations",
    "4": "4 Occupations in education, law and social, community and government services",
    "5": "5 Occupations in art, culture, recreation and sport",
    "6": "6 Sales and service occupations",
    "7": "7 Trades, transport and equipment operators and related occupations",
    "8": "8 Natural resources, agriculture and related production occupations",
    "9": "9 Occupations in manufacturing and utilities",
}

# Original population values retained to preserve the original per-capita analysis.
population_data = {
    "Province": regions,
    "Population": [
        520000, 160000, 980000, 780000, 8600000, 14700000,
        1380000, 1180000, 4400000, 5100000, 42000, 45000, 39000,
    ],
}
df_population = pd.DataFrame(population_data)

COLORS = {
    "navy": "#172554", "blue": "#4F6BED", "orange": "#E69A3A",
    "red": "#D95D5D", "green": "#239B75", "grid": "#E8EDF5",
}
GRAPH_CONFIG = {"displaylogo": False, "responsive": True,
                "modeBarButtonsToRemove": ["lasso2d", "select2d"]}

def style_figure(fig, height=430):
    fig.update_layout(
        template="plotly_white", height=height,
        margin=dict(l=55, r=30, t=75, b=90),
        font=dict(family="Inter, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif",
                  color=COLORS["navy"], size=12),
        title=dict(x=.02, xanchor="left", font=dict(size=17)),
        paper_bgcolor="white", plot_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(showgrid=False, automargin=True),
        yaxis=dict(gridcolor=COLORS["grid"], zeroline=False, automargin=True),
    )
    return fig

def section_heading(number, title, subtitle):
    return html.Div([
        html.Div(number, className="section-number"),
        html.Div([html.H2(title, className="section-title"),
                  html.P(subtitle, className="section-subtitle")],
                 className="section-heading-copy")
    ], className="section-heading")

def card(children):
    return html.Section(children, className="dashboard-card")

app = dash.Dash(__name__, title="Canadian Workforce Analysis",
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])
server = app.server

app.layout = html.Div([
    html.Header([
        html.Div("CANADIAN WORKFORCE INSIGHTS", className="eyebrow"),
        html.H1("Canadian Workforce Analysis", className="hero-title"),
        html.P("Explore essential services, employment patterns, and engineering talent "
               "across Canada's provinces and territories.", className="hero-description"),
        html.Div([
            html.Span("4 interactive analyses", className="hero-chip"),
            html.Span("13 provinces and territories", className="hero-chip"),
            html.Span("Python · Pandas · Dash · Plotly", className="hero-chip"),
        ], className="hero-chips")
    ], className="hero"),
    html.Main([
        card([
            section_heading("01", "Essential services distribution",
                "Compare nurses, police, and firefighters across provinces and territories."),
            html.Div([
                html.Div([
                    html.Label("Occupation group", className="control-label"),
                    dcc.Dropdown(id="service-selector",
                        options=[{"label": s, "value": s} for s in ["Nurses", "Police", "Firefighters"]],
                        value="Nurses", clearable=False)
                ], className="control control-wide"),
                html.Div([
                    html.Label("Measure", className="control-label"),
                    dcc.RadioItems(id="normalization-toggle",
                        options=[{"label": "Raw counts", "value": "raw"},
                                 {"label": "Per 100k population", "value": "per_capita"}],
                        value="raw", inline=True, className="radio-control")
                ], className="control")
            ], className="controls-row"),
            dcc.Graph(id="services-chart", config=GRAPH_CONFIG)
        ]),
        card([
            section_heading("02", "Gender employment by NOC category",
                "Compare reported employment for men and women by geography and NOC major group."),
            html.Div([
                html.Div([
                    html.Label("Province or territory", className="control-label"),
                    dcc.Dropdown(id="province-selector",
                        options=[{"label": r, "value": r} for r in regions],
                        value="Ontario", clearable=False)
                ], className="control"),
                html.Div([
                    html.Label("NOC major group", className="control-label"),
                    dcc.Dropdown(id="noc-selector",
                        options=[{"label": f"{k}: {v[2:]}", "value": k}
                                 for k, v in NOC_MAPPING.items()],
                        value="2", clearable=False)
                ], className="control control-wide")
            ], className="controls-row"),
            dcc.Graph(id="gender-pie", config=GRAPH_CONFIG),
            html.Div(id="gender-gap-indicator", className="insight-strip")
        ]),
        card([
            section_heading("03", "EV factory suitability analysis",
                "Identify regions whose engineering workforce meets a selected threshold."),
            html.Div([
                html.Div([
                    html.Label("Engineering discipline", className="control-label"),
                    dcc.Dropdown(id="discipline-selector", options=[
                        {"label": "All engineering (selected disciplines)", "value": "all"},
                        {"label": "Computer engineering", "value": "Computer engineering"},
                        {"label": "Electrical, electronics and communications engineering",
                         "value": "Electrical, electronics and communications engineering"},
                        {"label": "Mechanical engineering", "value": "Mechanical engineering"},
                    ], value="all", clearable=False)
                ], className="control control-wide")
            ], className="controls-row"),
            html.Div([
                html.Div([
                    html.Label("Minimum engineering workforce", className="control-label"),
                    dcc.Slider(id="threshold-slider", min=0, max=100000, step=5000,
                        value=50000, marks={i: f"{i//1000}k" for i in range(0, 100001, 20000)},
                        tooltip={"placement": "bottom"})
                ], className="slider-wrap"),
                html.Div(id="threshold-display", className="threshold-pill")
            ], className="threshold-row"),
            dcc.Graph(id="engineering-bars", config=GRAPH_CONFIG),
            html.Div(id="ev-recommendation", className="recommendation-panel"),
            html.P("This is a workforce-size screening exercise, not a complete site-selection model. "
                   "It does not account for land, infrastructure, logistics, costs, or policy.",
                   className="method-note")
        ]),
        card([
            section_heading("04", "Engineering talent heatmap",
                "Explore engineering workforce counts by discipline and geography."),
            html.Div([
                html.Label("Scale", className="control-label"),
                dcc.RadioItems(id="heatmap-scale",
                    options=[{"label": "Absolute numbers", "value": "absolute"},
                             {"label": "Per 100k population", "value": "per_capita"}],
                    value="absolute", inline=True, className="radio-control")
            ], className="control"),
            dcc.Graph(id="engineering-heatmap", config=GRAPH_CONFIG)
        ]),
        html.Footer([
            html.P("Canadian Workforce Analysis Dashboard", className="footer-title"),
            html.P("Population denominators are retained from the original project. "
                   "See the README for interpretation notes.", className="footer-note")
        ], className="footer")
    ], className="content")
], className="page-shell")

@app.callback(Output("services-chart", "figure"),
              Input("service-selector", "value"),
              Input("normalization-toggle", "value"))
def update_services(service, norm_type):
    match = essential_services.loc[essential_services["Geography"] == service, regions]
    if match.empty:
        raise ValueError(f"No essential-services data found for '{service}'.")
    counts = match.iloc[0].astype(float)
    if norm_type == "per_capita":
        population = df_population.set_index("Province").loc[regions, "Population"]
        values = counts.div(population).mul(100000)
        y_title, measure = "Count per 100,000 population", "Per 100k population"
    else:
        values = counts
        y_title, measure = "Workforce count", "Raw counts"
    data = pd.DataFrame({"Region": regions, "Count": values.values})
    fig = px.bar(data, x="Region", y="Count", text="Count",
                 title=f"{service} workforce by region · {measure}",
                 color_discrete_sequence=[COLORS["blue"]])
    fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside",
                      cliponaxis=False, hovertemplate="%{x}<br>%{y:,.1f}<extra></extra>")
    fig.update_layout(yaxis_title=y_title, xaxis_title=None, margin=dict(b=115, t=75))
    fig.update_xaxes(tickangle=-28)
    return style_figure(fig, 440)

@app.callback(Output("gender-pie", "figure"),
              Output("gender-gap-indicator", "children"),
              Input("province-selector", "value"),
              Input("noc-selector", "value"))
def update_gender(province, noc_code):
    column = NOC_MAPPING[noc_code]
    selected = gender_employment[gender_employment["Geography"] == province].set_index("Gender")
    men, women = float(selected.loc["Men", column]), float(selected.loc["Women", column])
    total = men + women
    ratio = women / men if men else float("inf")
    if ratio < .8:
        interpretation = "Men represent a larger share of reported employment."
    elif ratio < 1.2:
        interpretation = "Reported employment is relatively balanced between men and women."
    else:
        interpretation = "Women represent a larger share of reported employment."
    fig = px.pie(names=["Men", "Women"], values=[men, women],
                 title=f"{column.split(' ', 1)[1]} · {province}", hole=.58,
                 color=["Men", "Women"],
                 color_discrete_map={"Men": COLORS["blue"], "Women": COLORS["orange"]})
    fig.update_traces(texttemplate="%{label}<br>%{value:,.0f} (%{percent})",
                      textposition="inside", insidetextorientation="auto")
    fig.update_layout(showlegend=True, margin=dict(t=75, b=25),
                      legend=dict(orientation="h", y=-.08, x=.5, xanchor="center"))
    style_figure(fig, 420)
    ratio_text = f"{ratio:.2f}" if men else "N/A"
    indicator = html.Div([
        html.Div([
            html.Span("Women-to-men employment ratio", className="insight-label"),
            html.Strong(ratio_text, className="insight-value")
        ], className="insight-metric"),
        html.P(interpretation, className="insight-copy"),
        html.Span(f"Combined reported employment: {total:,.0f}", className="insight-footnote")
    ], className="insight-content")
    return fig, indicator

@app.callback(Output("engineering-bars", "figure"),
              Output("threshold-display", "children"),
              Output("ev-recommendation", "children"),
              Input("discipline-selector", "value"),
              Input("threshold-slider", "value"))
def update_engineering(discipline, threshold):
    disciplines = ["Computer engineering",
        "Electrical, electronics and communications engineering",
        "Mechanical engineering"]
    if discipline == "all":
        selected = engineering[engineering["Engineering Discipline"].isin(disciplines)]
        title = "Combined selected engineering disciplines"
    else:
        selected = engineering[engineering["Engineering Discipline"] == discipline]
        title = discipline
    melted = selected.melt(id_vars=["Engineering Discipline"],
                           var_name="Province", value_name="Count")
    if discipline == "all":
        melted = melted.groupby("Province", as_index=False)["Count"].sum()
    melted["Above Threshold"] = melted["Count"] >= threshold
    melted["Status"] = melted["Above Threshold"].map(
        {True: "Meets threshold", False: "Below threshold"})
    suitable = melted.loc[melted["Above Threshold"], "Province"].tolist()
    fig = px.bar(melted, x="Province", y="Count", color="Status",
        title=f"{title} · workforce by province and territory",
        color_discrete_map={"Meets threshold": COLORS["green"], "Below threshold": COLORS["red"]},
        text="Count", category_orders={"Province": regions})
    fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside",
                      cliponaxis=False)
    fig.update_layout(yaxis_title="Engineering workforce count", xaxis_title=None,
                      legend_title_text="Threshold status", margin=dict(b=115, t=75))
    fig.update_xaxes(tickangle=-28)
    style_figure(fig, 455)
    threshold_display = html.Span(f"{threshold:,.0f} engineers", className="threshold-value")
    if suitable:
        recommendation = html.Div([
            html.Div([html.Strong(str(len(suitable))),
                      html.Span(" regions meet the selected threshold")],
                     className="recommendation-summary"),
            html.Ul([html.Li(region) for region in suitable], className="recommendation-list")
        ])
    else:
        recommendation = html.P(
            "No province or territory reaches the selected workforce threshold.",
            className="recommendation-empty")
    return fig, threshold_display, recommendation

@app.callback(Output("engineering-heatmap", "figure"),
              Input("heatmap-scale", "value"))
def update_heatmap(scale_type):
    data = engineering.set_index("Engineering Discipline")[regions].copy()
    if scale_type == "per_capita":
        population = df_population.set_index("Province").loc[regions, "Population"]
        data = data.div(population, axis="columns").mul(100000)
        title, color_label = "Engineering workforce per 100,000 population", "Count per 100k"
    else:
        title, color_label = "Engineering workforce by discipline and region · absolute counts", "Workforce count"
    fig = px.imshow(data, labels={"x": "Province or territory", "y": "Discipline",
        "color": color_label}, title=title, color_continuous_scale="Tealgrn", aspect="auto")
    fig.update_layout(margin=dict(l=190, r=35, t=75, b=100), height=490)
    fig.update_xaxes(tickangle=-28)
    return style_figure(fig, 490)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8050, debug=False)

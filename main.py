# Importing Toolkits
import pandas as pd
import sklearn

import numpy as np
import plotly.express as px
import json
import requests

# Importing Dash Components
import dash
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import dash_loading_spinners as dls

import home
import internet
import other

used_color = ["#ADA2FF", "#FCDDB0", "#FF9F9F", "#EDD2F3"]
# ----------- Loading Dataset -----------
df = pd.read_csv("Telco-Customer-Churn.csv")

# First: We have to Replace Any Space With 0
df["TotalCharges"] = df["TotalCharges"].replace(" ", 0)

# Converting Data Type From Object Into Float
df["TotalCharges"] = df["TotalCharges"].astype(float)

# Replace 0 With The Median
df["TotalCharges"] = df["TotalCharges"].replace(0, df["TotalCharges"].median())

df.replace(["No internet service", "No phone service"], "No", inplace=True)

payment_method = df["PaymentMethod"].unique().tolist()
payment_method.insert(0, "All")

contracts = df["Contract"].unique().tolist()
contracts.insert(0, "All")

churn = df["Churn"].unique().tolist()
churn = ["Left" if i == "Yes" else "Stayed" for i in churn]
churn.insert(0, "All")

churn = {
    "All": "All",
    "Stayed": "No",
    "Left": "Yes"
}

transformer = pd.read_pickle("transformer.pkl")

# *******************************************************************************************************
# ** Notice: The Data Exploration & Preprocessing of This DataSet has Already Done In Jupyter Notebook **
# *******************************************************************************************************

# -------------- Start The Dash App ------------------ #
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG], suppress_callback_exceptions=True)

# To render on web app
server = app.server

# Pages Navigator
pages_dict = {
    "Home": "/",
    "Internet Services": "/InternetServices",
    "Other Services": "/OtherServices",
    "Churn Prediction": "/ChurnPrediction",
}

# Sidebar Style
sidebar_style = {
    "position": "fixed",
    "width": "17rem",
    "height": "100vh",
    "top": "0",
    "bottom": "0",
    "left": "0",
    "padding": "15px",
    "background-color": "#171B2E",
    "border-right": "2px solid #222",
    "overflow": "hidden"
}

# Page Content Style
content_style = {
    "margin-left": "17rem",
    "margin-right": "0",
    "padding": "5px",
    "height": "100%",
}

# DropDown Filter Style
filter_style = {
    "border-width": "0px",
    "font-family": "arial",
    "margin-bottom": "20px",
    "background-color": "#111526",
    "width": "100%",
}

# -------------- Start The App Layout ------------------ #
# Creating The SideBar
sidebar = html.Div(
    [
        dcc.Dropdown(
            id="theme-toggle",
            options=[
                {
                    "label": html.Span(
                        [
                            html.Img(src="/assets/light-mode.png", height=25),
                            html.Span("Light", style={'font-size': 14, 'padding-left': 10, "color": "#999"}),
                        ], style={'align-items': 'center', 'justify-content': 'center'}
                    ),
                    "value": "Light",
                },
                {
                    "label": html.Span(
                        [
                            html.Img(src="/assets/dark-mode.png", height=25),
                            html.Span("Dark", style={'font-size': 14, 'padding-left': 10, "color": "#999"}),
                        ], style={'align-items': 'center', 'justify-content': 'center'}
                    ),
                    "value": "Dark",
                }
            ],
            value="Light",
            multi=False,
            clearable=False,
            searchable=False,
            style=filter_style

        ),

        html.H1("Customer Churn",
                style={"font": "bold 36px arial",
                       "margin-top": "30px",
                       "margin-bottom": "20px",
                       "color": "#fefefe",
                       "text-align": "center"}),
        html.Hr(style={"border-color": "#444"}),

        dbc.Nav(
            [
                dbc.NavLink(f"{k}", href=f"{v}",
                            className="btn", active="exact",
                            style={"margin-bottom": "20px", "font-weight": "bold"})

                for k, v in pages_dict.items()
            ],
            vertical=True,
            pills=True,

        ),
        html.Br(),
        dbc.Label("Contract Type", id="contract-label", style={"font-size": "14px"}),

        dcc.Dropdown(
            id="contracts-filter",
            options=[
                {"label": html.Span([i], style={'color': '#D67BFF', 'font': "bold 16px arial", "margin": "12px 5px"}),
                 "value": i} for i in contracts
            ],
            value="All",

            multi=False,
            searchable=False,
            clearable=False,
            optionHeight=40,

            style=filter_style
        ),

        # html.Hr(),
        dbc.Label(id="filter-label", children="Payment Methods", style={"font-size": "14px"}),

        dcc.Dropdown(
            id="payment-method-filter",
            options=[
                {"label": html.Span([i], style={'color': '#D67BFF', 'font': "bold 16px arial", "margin": "12px 5px"}),
                 "value": i, } for i in payment_method

            ],
            value="All",
            multi=False,
            optionHeight=40,
            clearable=False,
            searchable=True,
            style=filter_style
        ),

        dcc.Dropdown(
            id="churn-filter",
            options=[
                {"label": html.Span([k], style={'color': '#D67BFF', 'font': "bold 16px arial", "margin": "12px 5px"}),
                 "value": v, } for k, v in churn.items()

            ],
            value="All",
            multi=False,
            optionHeight=40,
            clearable=False,
            searchable=True,
            style={"display": "none"}
        ),
    ],
    style=sidebar_style
)

# page content
content = html.Div(id="page-content", children=[], style=content_style)


# ►►► App Layout


def filter_the_payment_method(the_df, the_payment_method):
    df_filtered = the_df.copy()

    if the_payment_method != "All":
        f = the_df["PaymentMethod"] == the_payment_method
        df_filtered = the_df[f].copy()

    return df_filtered


def filter_the_contract(the_df, contracts_type):
    df_filtered = the_df.copy()

    if contracts_type != "All":
        f = the_df["Contract"] == contracts_type
        df_filtered = the_df[f].copy()

    return df_filtered


def filter_the_churn_status(the_df, churn_status):
    df_filtered = the_df.copy()

    if churn_status != "All":
        f = the_df["Churn"] == churn_status
        df_filtered = the_df[f].copy()

    return df_filtered


options_style = {'color': '#B51B75', 'font': "bold 16px arial", "margin": "12px 5px"}

model_inputs_style = {
    "border-width": "0px",
    "font": "bold 16px arial",
    "margin-bottom": "20px",
    "background-color": "#ededed",
    "width": "100%",
    "color": "#B51B75",
    "padding": "8px 12px",
    "border-radius": "5px",
    "border": "none"

}
model_drop_down_style = {
    "border-width": "0px",
    "font-family": "arial",
    "margin-bottom": "20px",
    "background-color": "#ededed",
    "width": "100%",
    "color": "#D67BFF",
    "border-radius": "5px",
    "border": "none"
}
card_style = {
    "text-align": "center",
    "padding-top": "25px",
    "padding-bottom": "25px",
    "border": f"3px solid #999",
    "border-radius": "5px",
    "margin-bottom": "5px",
    "box-shadow": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    "opacity": 0.8
}

prediction_layout = html.Div([
    html.Br(),
    dbc.Row([
        html.H1("Customer Churn Forecasting 🚀",
                style={"font": "bold 40px arial", "text-align": "center",
                       "color": "#444"})
    ]),
    html.Br(),

    dbc.Row([
        dbc.Col(
            [
                dbc.Label(children="Gender", style={"font-size": "14px", "color": "#222"}),
                dcc.Dropdown(
                    id="gender",
                    options=[
                        {'label': html.Span("Male", style=options_style), 'value': 'Male', },
                        {'label': html.Span("Female", style=options_style), 'value': 'Female'},
                    ],
                    value="Male",
                    multi=False,
                    searchable=False,
                    clearable=False,
                    optionHeight=40,

                    style=model_drop_down_style
                ),

                dbc.Label(children="Customer Life Time", style={"font-size": "14px", "color": "#222"}),
                dcc.Input(
                    id="tenure", type="number", placeholder="Enter Customer Life Time",
                    min=0, max=80, step=1, value=15,
                    style=model_inputs_style
                ),

                dbc.Label(children="Internet Services", style={"font-size": "14px", "color": "#222"}),

                dcc.Dropdown(
                    id="internet-services",
                    options=[
                        {'label': html.Span("No", style=options_style), 'value': 'No'},
                        {'label': html.Span("Fiber optic", style=options_style), 'value': 'Fiber optic'},
                        {'label': html.Span("DSL", style=options_style), 'value': 'DSL'},
                    ],
                    value="DSL",
                    multi=False,
                    searchable=False,
                    clearable=False,
                    optionHeight=40,

                    style=model_drop_down_style
                ),

            ], lg=3, sm=12
        ),
        dbc.Col(
            [
                dbc.Label(children="Is Senior Citizen", style={"font-size": "14px", "color": "#222"}),
                dcc.Dropdown(
                    id="is-senior",
                    options=[
                        {'label': html.Span("Less Than 65", style=options_style), 'value': 0},
                        {'label': html.Span("Greater Than 65", style=options_style), 'value': 1},
                    ],
                    value=0,
                    multi=False,
                    searchable=False,
                    clearable=False,
                    optionHeight=40,
                    style=model_drop_down_style
                ),

                dbc.Label(children="Monthly Charges", style={"font-size": "14px", "color": "#222"}),
                dcc.Input(
                    id="monthly-charges", type="number", placeholder="Enter Monthly Charges",
                    min=18, max=500, step=0.01, value=22.5,
                    style=model_inputs_style
                ),

                dbc.Label(children="Contract Status", style={"font-size": "14px", "color": "#222"}),
                dcc.Dropdown(
                    id="contract",
                    options=[
                        {'label': html.Span("Month-to-Month", style=options_style), 'value': 'Month-to-month'},
                        {'label': html.Span("Two Year ", style=options_style), 'value': 'Two year'},
                        {'label': html.Span("One Year", style=options_style), 'value': 'One year'},
                    ],
                    value="Two year",
                    multi=False,
                    searchable=False,
                    clearable=False,
                    optionHeight=40,

                    style=model_drop_down_style
                ),

            ], lg=3, sm=12
        ),
        dbc.Col(
            [
                dbc.Label(children="Has Partner", style={"font-size": "14px", "color": "#222"}),

                dcc.Dropdown(
                    id="partner",
                    options=[
                        {'label': html.Span("Yes", style=options_style), 'value': 1},
                        {'label': html.Span("No", style=options_style), 'value': 0},
                    ],
                    value=1,
                    multi=False,
                    searchable=False,
                    clearable=False,
                    optionHeight=40,
                    style=model_drop_down_style
                ),

                dbc.Label(children="Total Charges", style={"font-size": "14px", "color": "#222"}),

                dcc.Input(
                    id="total-charges", type="number", placeholder="Enter Total Charges",
                    min=18, max=10000, step=0.01, value=630,
                    style=model_inputs_style
                ),

                dbc.Label(children="Payment Methods", style={"font-size": "14px", "color": "#222"}),
                dcc.Dropdown(
                    id="payment-method",
                    options=[
                        {'label': html.Span("Credit Card", style=options_style), 'value': 'Credit card (automatic)'},
                        {'label': html.Span("Electronic Check", style=options_style), 'value': 'Electronic check'},
                        {'label': html.Span("Bank Transfer", style=options_style),
                         'value': 'Bank transfer (automatic)'},
                        {'label': html.Span("Mailed Check", style=options_style), 'value': 'Mailed check'},
                    ],
                    value="Electronic check",
                    multi=False,
                    searchable=False,
                    clearable=False,
                    optionHeight=40,

                    style=model_drop_down_style
                ),

            ], lg=3, sm=12
        ),
        dbc.Col(
            [
                dbc.Label(children="Has Dependents", style={"font-size": "14px", "color": "#222"}),
                dcc.Dropdown(
                    id="dependents",
                    options=[
                        {'label': html.Span("Yes", style=options_style), 'value': 0},
                        {'label': html.Span("No", style=options_style), 'value': 1},
                    ],
                    value=0,
                    multi=False,
                    searchable=False,
                    clearable=False,
                    optionHeight=40,
                    style=model_drop_down_style
                ),

                dbc.Label(children="Phone Services", style={"font-size": "14px", "color": "#222"}),
                dcc.Dropdown(
                    id="phone-services",
                    options=[
                        {'label': html.Span("Yes", style=options_style), 'value': 1},
                        {'label': html.Span("No", style=options_style), 'value': 0},
                    ],
                    value=1,
                    multi=False,
                    searchable=False,
                    clearable=False,
                    optionHeight=40,
                    style=model_drop_down_style
                ),

            ], lg=3, sm=12
        )
    ]),
    html.Br(),

    html.Button('Forecasting 🚀', id='submit-button', n_clicks=0),

    html.Br(),

    # Cards
    dbc.Row([
        dcc.Loading(
            children=[
                dbc.Col([
                    html.H3(style={"color": "#555", "font": "bold 25px tahoma", "text-align": "center"},
                            id='output-div'),

                    html.Img(id="prediction-image", src="", height=100, style={"margin": "auto", "display": "flex"})
                ]),
            ],
            type="circle",
            fullscreen=False,
            color="purple"
        )

    ]),
])


# url = "http://128.0.0.1:8000/churn_prediction"

# Deep Learning API
url = "https://modyehab810-customer-churn-api.hf.space/churn_prediction"


# Define callback for Prediction Page
@app.callback(Output('output-div', 'children'),
              Output('prediction-image', 'src'),

              Input('submit-button', 'n_clicks'),

              State('gender', 'value'),
               State('is-senior', 'value'),
               State('partner', 'value'),
               State('dependents', 'value'),
               State('tenure', 'value'),
               State('phone-services', 'value'),
               State('internet-services', 'value'),
               State('contract', 'value'),
               State('payment-method', 'value'),
               State('monthly-charges', 'value'),
               State('total-charges', 'value'),

               )
def update_output(n_clicks, gender, senior_citizen, partner, dependents, tenure, phone_services,
                  internet_services, contract, payment_method_val, monthly_charges, total_charges):
    if n_clicks > 0:
        input_dict = {
            'gender': [gender],
            'SeniorCitizen': [senior_citizen],
            'Partner': [partner],
            'Dependents': [dependents],
            'tenure': [tenure],
            'PhoneService': [phone_services],
            'InternetService': [internet_services],
            'Contract': [contract],
            'PaymentMethod': [payment_method_val],
            'MonthlyCharges': [monthly_charges],
            'TotalCharges': [total_charges]
        }

        input_dict = pd.DataFrame(input_dict)
        input_dict = transformer.transform(input_dict)[0]

        key_list = ["GenderMale",
                    "InternetServiceFiberOptic",
                    "InternetServiceNo",
                    "ContractOneYear",
                    "ContractTwoYear",
                    "PaymentMethodCreditCard",
                    "PaymentMethodElectronicCheck",
                    "PaymentMethodMailedCheck",
                    "SeniorCitizen",
                    "Partner",
                    "Dependents",
                    "tenure",
                    "PhoneService",
                    "MonthlyCharges",
                    "TotalCharges"]

        model_dictionary = {}

        for i in range(len(key_list)):
            model_dictionary[key_list[i]] = input_dict[i]

        json_input = json.dumps(model_dictionary)
        response = requests.post(url, data=json_input)
        
        if response.status_code == 200:
            image_src = "/assets/happy-face.png"

            if response.text.__contains__("Leave"):
                image_src = "/assets/sad.png"
            return [response.text, image_src]

        else:
            return ["Sorry, Server is Crashed", "/assets/sad.png"]


    else:
        return [input_dict, '']


app.layout = html.Div([
    dcc.Location(id="page-url"),
    sidebar,
    content,
    html.Div(dls.Grid(id='loading', show_initially=True, fullscreen=True, color="#435278", width=100, margin=10),
             id="loading-container")
], className="container-fluid", style={"padding-right": "0"})


# CallBack Functions
@app.callback(
    Output(component_id="contract-label", component_property="style"),
    Output(component_id="contracts-filter", component_property="style"),
    Output(component_id="loading-container", component_property="style"),
    Output(component_id="filter-label", component_property="children"),
    Output(component_id="payment-method-filter", component_property="style"),
    Output(component_id="churn-filter", component_property="style"),

    Output(component_id="page-content", component_property="children"),
    Output(component_id="page-content", component_property="style"),

    # For Page Routing
    Input(component_id="page-url", component_property="pathname"),

    # Get Values From Contracts Filter Select Box
    Input(component_id="contracts-filter", component_property="value"),

    # Get Values From Payment Methods Filter Select Box
    Input(component_id="payment-method-filter", component_property="value"),

    # Get Values From Churn Filter Select Box
    Input(component_id="churn-filter", component_property="value"),

    Input(component_id="theme-toggle", component_property="value"),

)
def get_content_layout(pathname, contract_val, payment_method_val, churn_val, target_theme):
    page_theme = {
        "title_color": "#333",
        "text_color": "#777",
        "app_theme": "#F8F8F8",

        "chart_theme": "plotly_white",
        "chart_border": "#F8F8F8",

        "card_bg": "#fff",
        "card_bg_border": "#fafafa",
        "card_font_color": "#333",

    }

    if target_theme == "Dark":
        page_theme["title_color"] = "#fefefe"

        page_theme["text_color"] = "#eee"

        page_theme["app_theme"] = "#111526"

        page_theme["chart_theme"] = "plotly_dark"
        page_theme["chart_border"] = "#171C31"

        page_theme["card_bg"] = "#171C31"
        page_theme["card_bg_border"] = "#171C31"
        page_theme["card_font_color"] = "#fafafa"

    card_style = {
        "background-color": page_theme["card_bg"],
        "text-align": "center",
        "padding-top": "25px",
        "padding-bottom": "25px",
        "border": f"3px solid {page_theme['card_bg_border']}",
        "border-radius": "5px",
        "margin-bottom": "5px",
        "box-shadow": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
        "opacity": 0.8
    }

    graph_style = {
        "margin-bottom": "10px",
        "height": "560px",
        "border": f"3px solid {page_theme['chart_border']}",
        "border-radius": "4px"
    }

    the_app_theme = {
        "margin-left": "16rem",
        "margin-right": "0rem",
        "padding": "20px",
        "height": "100%",
        "background-color": page_theme['app_theme']
    }

    if pathname == "/":
        dff = filter_the_contract(df, contract_val)

        dff = filter_the_payment_method(dff, payment_method_val)

        customer_count, charges, churn_customer = home.create_home_cards(dff, contract_val, payment_method_val)
        return [
            {"display": "block"},

            filter_style,
            {"display": "none"},
            "Payment Methods",  # Filter Label
            filter_style,  # Payment Methods Filter Style
            {"display": "none"},  # Remove Churn Filter in This Page

            html.Div([
                html.Br(),
                dbc.Row([
                    html.H1("Customer Churn Analysis 📊",
                            style={"font": "bold 40px arial", "text-align": "center",
                                   "color": page_theme['title_color']})
                ]),

                html.Br(),

                # Cards
                dbc.Row([
                    dbc.Col([
                        dbc.Card(
                            dbc.CardBody([
                                html.H3(customer_count,
                                        style={"color": page_theme['card_font_color'], "font": "bold 30px tahoma"},
                                        id='customer-count-crd'),
                                html.H3("Customers",
                                        style={"font": "bold 20px tahoma", "color": page_theme['card_font_color']}),
                            ]), style=card_style,
                        ),

                    ]),
                    dbc.Col([
                        dbc.Card(
                            dbc.CardBody([
                                html.H3(charges,
                                        style={"color": page_theme['card_font_color'], "font": "bold 30px tahoma"},
                                        id='charges-crd'),
                                html.H3("Total Charges", style={"font": "bold 20px tahoma",
                                                                "color": page_theme['card_font_color']}),
                            ]), style=card_style
                        ),

                    ]),
                    dbc.Col([
                        dbc.Card(
                            dbc.CardBody([
                                html.H3(churn_customer,
                                        style={"color": page_theme['card_font_color'], "font": "bold 30px tahoma"},
                                        id='left-customer-crd'),
                                html.H3("(%) Left Customer", style={"font": "bold 20px tahoma",
                                                                    "color": page_theme['card_font_color']}),
                            ]), style=card_style
                        ),
                    ]),
                ]),
                html.Br(),

                dbc.Row(
                    [
                        dbc.Col(

                            [
                                dcc.Graph(id="gender-chart",
                                          config={'displayModeBar': False},
                                          figure=home.count_viz_func(dff, "gender", title="Gender Distributions",
                                                                     x_label="Gender", y_label="Frequency in PCT(%)",
                                                                     hover_template="Gender: %{x}<br>Frequency in PCT(%): %{y:0.2f}%",
                                                                     chart_theme=page_theme['chart_theme']),
                                          style=graph_style)
                            ]
                        ),
                        dbc.Col(
                            [
                                dcc.Graph(id="senior-citizen-chart",
                                          config={'displayModeBar': False},
                                          figure=home.count_senior_citizen(dff, "SeniorCitizen",
                                                                           title="Senior Citizen Distributions",
                                                                           x_label="Senior Citizen",
                                                                           y_label="Frequency in PCT(%)",
                                                                           hover_template="Senior Citizen: %{x}<br>Frequency in PCT(%): %{y:0.0f}%",
                                                                           chart_theme=page_theme['chart_theme']),
                                          style=graph_style)
                            ]
                        )
                    ]
                ),

                html.Br(),
                dbc.Row([
                    dbc.Col(
                        [
                            dcc.Graph(id="dependents",
                                      config={'displayModeBar': False},
                                      figure=home.count_viz_func(dff, "Dependents", title="Dependents Distributions",
                                                                 x_label="Dependents", y_label="Frequency in PCT(%)",
                                                                 hover_template="Dependents: %{x}<br>Frequency in PCT(%): %{y:0.2f}%",
                                                                 chart_theme=page_theme['chart_theme']),
                                      style=graph_style)
                        ]
                    ),
                    dbc.Col(
                        [
                            dcc.Graph(id="phone-service-status",
                                      config={'displayModeBar': False},
                                      figure=home.phone_service_chart(dff, "PhoneService",
                                                                      title="Phone Services Status",
                                                                      hover_template="Phone Services Status: %{label}<br>Frequency: %{value}",
                                                                      chart_theme=page_theme['chart_theme']),
                                      style=graph_style)
                        ]
                    )
                ]),
                html.Br(),
                dbc.Row([
                    dbc.Col(
                        [
                            dcc.Graph(id="churn",
                                      config={'displayModeBar': False},
                                      figure=home.count_customer_churn(dff, "Churn",
                                                                       title="Customer Status Distributions",
                                                                       x_label="Customer Status",
                                                                       y_label="Frequency in PCT(%)",
                                                                       hover_template="Churn Status: %{x}<br>Frequency in PCT(%): %{y:0.2f}%",
                                                                       chart_theme=page_theme['chart_theme'],
                                                                       ),
                                      style=graph_style)
                        ]
                    )
                ]),
                html.Br(),

                dbc.Row([
                    dbc.Col(
                        [
                            dcc.Graph(id="customer_by_tenure",
                                      figure=home.count_customer_tenure(dff, "tenure",
                                                                        title="Number of Customers Via Tenure (Months)",
                                                                        hover_template="Tenure (Months): %{x}<br>Frequency of Customer: %{y:,.0f}",
                                                                        chart_theme=page_theme['chart_theme'],
                                                                        ),
                                      style=graph_style)
                        ]
                    )
                ])

            ]),

            # App Theme Dark Or Light
            the_app_theme
        ]

    if pathname == "/InternetServices":
        dff = filter_the_contract(df, contract_val)

        dff = filter_the_churn_status(dff, churn_val)

        return [
            {"display": "block"},

            filter_style,
            {"display": "none"},

            "Churn Status",  # Filter Label
            {"display": "none"},  # Remove Payment Methods Filter Style
            filter_style,  # Display Churn Status Filter

            html.Div([
                html.Br(),
                dbc.Row([
                    html.H1("Internet Services 🌐",
                            style={"font": "bold 40px arial", "text-align": "center",
                                   "color": page_theme['title_color']})
                ]),

                html.Br(),

                dbc.Row(
                    [
                        dbc.Col(

                            [
                                dcc.Graph(id="online-backup-chart",

                                          config={'displayModeBar': False},
                                          figure=internet.count_online_backup(dff, "OnlineBackup",
                                                                              title="Online Backup Status",
                                                                              hover_template="Online Backup: %{label}<br>Frequency in PCT(%): %{percent}<br>Count: %{value:,.0f}",
                                                                              chart_theme=page_theme['chart_theme']),
                                          style=graph_style)
                            ]
                        ),
                        dbc.Col(
                            [
                                dcc.Graph(id="online-security-chart",
                                          config={'displayModeBar': False},
                                          figure=internet.count_viz_func(dff, "OnlineSecurity",
                                                                         title="Online Security Status",
                                                                         x_label="Online Security",
                                                                         y_label="Frequency in PCT(%)",
                                                                         hover_template="Online Security Status: %{x}<br>Frequency in PCT(%): %{y:0.0f}%",
                                                                         chart_theme=page_theme['chart_theme']),
                                          style=graph_style)
                            ]
                        )
                    ]
                ),

                html.Br(),
                dbc.Row([
                    dbc.Col(
                        [
                            dcc.Graph(id="internet-service-status",
                                      config={'displayModeBar': False},

                                      figure=internet.count_viz_func(dff, "InternetService",
                                                                     title="Internet Services Status Distribution",
                                                                     x_label="Internet Service",
                                                                     y_label="Frequency in PCT(%)",
                                                                     hover_template="Internet Service: %{x}<br>Frequency in PCT(%): %{y:0.2f}%",
                                                                     chart_theme=page_theme['chart_theme']),
                                      style=graph_style)
                        ]
                    )
                ]),

            ]),

            # App Theme Dark Or Light
            the_app_theme
        ]

    if pathname == "/OtherServices":
        dff = filter_the_contract(df, contract_val)

        dff = filter_the_payment_method(dff, payment_method_val)

        return [
            {"display": "block"},

            filter_style,
            {"display": "none"},

            "",  # Filter Label
            {"display": "none"},  # Remove Churn Filter in This Page
            {"display": "none"},  # Remove Churn Filter in This Page

            html.Div([
                html.Br(),
                dbc.Row([
                    html.H1("Other Services 📊",
                            style={"font": "bold 40px arial", "text-align": "center",
                                   "color": page_theme['title_color']})
                ]),

                html.Br(),

                dbc.Row(
                    [
                        dbc.Col(

                            [
                                dcc.Graph(id="device-protection-chart",
                                          config={'displayModeBar': False},
                                          figure=other.count_viz_func(dff, "DeviceProtection",
                                                                      title="Device Protection Subscription",
                                                                      x_label="Status", y_label="Frequency in PCT(%)",
                                                                      hover_template="Status: %{x}<br>Frequency in PCT(%): %{y:0.2f}%",
                                                                      chart_theme=page_theme['chart_theme']),
                                          style=graph_style)
                            ]
                        ),
                        dbc.Col(
                            [
                                dcc.Graph(id="tech-support-chart",
                                          config={'displayModeBar': False},
                                          figure=other.tech_support_chart(dff, "TechSupport",
                                                                          title="Tech Support Subscription",
                                                                          hover_template="Tech Support: %{label}<br>Frequency in PCT(%): %{percent}<br>Count: %{value:,.0f}",
                                                                          chart_theme=page_theme['chart_theme']),
                                          style=graph_style)
                            ]
                        )
                    ]
                ),

                html.Br(),
                dbc.Row([
                    dbc.Col(
                        [
                            dcc.Graph(id="StreamingTV",
                                      config={'displayModeBar': False},
                                      figure=other.count_viz_func(dff, "StreamingTV", title="Streaming TV Subscription",
                                                                  x_label="Streaming TV", y_label="Frequency in PCT(%)",
                                                                  hover_template="Status: %{x}<br>Frequency in PCT(%): %{y:0.2f}%",
                                                                  chart_theme=page_theme['chart_theme']),
                                      style=graph_style)
                        ]
                    ),
                    dbc.Col(
                        [
                            dcc.Graph(id="PaperlessBilling",
                                      config={'displayModeBar': False},
                                      figure=other.count_viz_func(dff, "PaperlessBilling",
                                                                  title="Paperless Billing Subscription",
                                                                  x_label="Paperless Billing",
                                                                  y_label="Frequency in PCT(%)",
                                                                  hover_template="Status: %{x}<br>Frequency in PCT(%): %{y:0.2f}%",
                                                                  chart_theme=page_theme['chart_theme']),
                                      style=graph_style)
                        ]
                    )
                ]),
                html.Br(),
                dbc.Row([
                    dbc.Col(
                        [
                            dcc.Graph(id="PaymentMethod",
                                      config={'displayModeBar': False},
                                      figure=other.count_viz_func(dff, "PaymentMethod",
                                                                  title="Payment Methods Distribution",
                                                                  x_label="Payment Method",
                                                                  y_label="Frequency in PCT(%)",
                                                                  hover_template="Payment Method: %{x}<br>Frequency in PCT(%): %{y:0.2f}%",
                                                                  chart_theme=page_theme['chart_theme'],
                                                                  ),
                                      style=graph_style)
                        ]
                    )
                ]),

            ]),

            # App Theme Dark Or Light
            the_app_theme
        ]

    if pathname == "/ChurnPrediction":
        dff = filter_the_contract(df, contract_val)

        dff = filter_the_payment_method(dff, payment_method_val)

        return [
            {"display": "none"},

            {"display": "none"},
            {"display": "none"},

            "",  # Filter Label
            {"display": "none"},  # Remove Churn Filter in This Page
            {"display": "none"},  # Remove Churn Filter in This Page
            prediction_layout,

            # App Theme Dark Or Light
            {
                "margin-left": "16rem",
                "margin-right": "0rem",
                "padding": "20px",
                "height": "100%",
                "background-color": "#F8F8F8"
            }
        ]


# Run The App
if __name__ == "__main__":
    app.run_server(debug=True)

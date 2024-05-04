# Importing Toolkits
import pandas as pd
import numpy as np
import plotly.express as px

used_color = ["#ADA2FF", "#FCDDB0", "#FF9F9F", "#EDD2F3", "#7FE9DE", "#84DFFF"]


# Custom function for chart layout
def update_layout(fig, title_font_size=28, hover_font_size=16, hover_bgcolor="#111", showlegend=False):
    fig.update_layout(
        showlegend=showlegend,
        title={
            "font": {
                "size": title_font_size,
                "family": "tahoma"
            }
        },
        hoverlabel={
            "bgcolor": hover_bgcolor,
            "font_size": hover_font_size,
            "font_family": "tahoma"
        }
    )


# ---------------------- Visualizations Graphs Functions ----------------------
# ====================== Home Page ================================3

def create_home_cards(the_df, the_contract, the_payment_method):
    customer_counts = the_df["customerID"].nunique()

    total_charges = the_df["TotalCharges"].sum()

    churn_customer = (len(the_df[the_df["Churn"] == "Yes"]) / len(the_df)) * 100

    return f"{customer_counts:,d}", f"${total_charges:,.2f}", f"{churn_customer:0.2f}%"


# Main Visualization Function
def count_viz_func(data_frame, column_name, title="Chart Title",
                   title_font_size=30, x_label="X", y_label="Y",
                   showlegend=False, hover_template="None", chart_theme="plotly_dark"):
    # Get Value Count For Any Column in df
    value_counts = data_frame[column_name].value_counts(normalize=1) * 100

    fig = px.bar(
        data_frame=value_counts,
        x=value_counts.index,
        y=value_counts,
        color=value_counts.index,
        color_discrete_sequence=used_color,
        title=title,
        labels={"index": x_label, "y": y_label},
        template=chart_theme,
        text=value_counts.apply(lambda x: f"{x:0.1f}%")
    )

    if chart_theme == "plotly_dark":
        fig.update_layout(
            paper_bgcolor='#171C31',
            plot_bgcolor='rgba(255,255,255,0)',
        )

    fig.update_layout(

        showlegend=showlegend,
        title={
            "font": {
                "size": title_font_size,
                "family": "tahoma"
            }
        },
        hoverlabel={
            "bgcolor": "#222",
            "font_size": 16,
            "font_family": "tahoma"
        }
    )

    fig.update_traces(
        textfont={
            "size": 18,
            "family": "tahoma",
            "color": "#222"
        },

        hovertemplate=hover_template,
    )

    return fig


def count_senior_citizen(data_frame, column_name, title="Chart Title",
                         title_font_size=30, x_label="X", y_label="Y",
                         showlegend=False, hover_template="None", chart_theme="plotly_dark"):
    senior_citizen = data_frame[column_name].value_counts(normalize=1) * 100

    fig = px.bar(
        data_frame=senior_citizen,
        x=["Greater Than 65" if i == 1 else "Less Than 65" for i in senior_citizen.index],
        y=senior_citizen,
        color=["Greater Than 65" if i == 1 else "Less Than 65" for i in senior_citizen.index],
        color_discrete_sequence=used_color,
        title=title,
        labels={"x": x_label, "y": y_label},
        template=chart_theme,
        text=senior_citizen.apply(lambda x: f"{x:0.1f}%")
    )

    if chart_theme == "plotly_dark":
        fig.update_layout(
            paper_bgcolor='#171C31',
            plot_bgcolor='rgba(255,255,255,0)',
        )

    fig.update_layout(

        showlegend=showlegend,
        title={
            "font": {
                "size": title_font_size,
                "family": "tahoma"
            }
        },
        hoverlabel={
            "bgcolor": "#222",
            "font_size": 16,
            "font_family": "tahoma"
        }
    )

    fig.update_traces(
        textfont={
            "size": 18,
            "family": "tahoma",
            "color": "#222"
        },

        hovertemplate=hover_template,
    )

    return fig


def phone_service_chart(data_frame, column_name, title="Chart Title",
                        title_font_size=30, showlegend=False,
                        hover_template="None", chart_theme="plotly_dark"):
    phone_services = data_frame[column_name].value_counts()

    fig = px.pie(
        names=phone_services.index,
        values=phone_services,
        title=title,
        color_discrete_sequence=used_color,
        hole=0.4,
    )
    fig.update_layout(

        showlegend=showlegend,
        title={
            "font": {
                "size": title_font_size,
                "family": "tahoma"
            }
        },
        hoverlabel={
            "bgcolor": "#222",
            "font_size": 16,
            "font_family": "tahoma"
        }
    )

    # Function That Give The Chart a custom Format
    if chart_theme == "plotly_dark":
        fig.update_layout(
            paper_bgcolor='#171C31',
            plot_bgcolor='rgba(255,255,255,0)',
        )
        fig.update_layout(

            showlegend=showlegend,
            title={
                "font": {
                    "color": "#fff",
                    "size": title_font_size,
                    "family": "tahoma"
                }
            },
            hoverlabel={
                "bgcolor": "#222",
                "font_size": 16,
                "font_family": "tahoma"
            }
        )

    fig.update_traces(
        textinfo='label+percent',

        textfont={
            "size": 18,
            "family": "tahoma",
            "color": "#222"
        },

        hovertemplate=hover_template,
        marker=dict(line=dict(color='#333', width=0.5)),
    )

    return fig


def count_customer_churn(data_frame, column_name, title="Chart Title",
                         title_font_size=30, x_label="X", y_label="Y",
                         showlegend=False, hover_template="None", chart_theme="plotly_dark"):
    churn = data_frame[column_name].value_counts(normalize=1) * 100

    fig = px.bar(
        data_frame=churn,
        x=["Left" if i == "Yes" else "Stayed" for i in churn.index],
        y=churn,
        color=["Left" if i == "Yes" else "Stayed" for i in churn.index],
        color_discrete_sequence=used_color,
        title=title,
        labels={"x": x_label, "y": y_label},
        template=chart_theme,
        text=churn.apply(lambda x: f"{x:0.1f}%"),
    )

    if chart_theme == "plotly_dark":
        fig.update_layout(
            paper_bgcolor='#171C31',
            plot_bgcolor='rgba(255,255,255,0)',
        )

    fig.update_layout(

        showlegend=showlegend,
        title={
            "font": {
                "size": title_font_size,
                "family": "tahoma"
            }
        },
        hoverlabel={
            "bgcolor": "#222",
            "font_size": 16,
            "font_family": "tahoma"
        }
    )

    fig.update_traces(
        textfont={
            "size": 18,
            "family": "tahoma",
            "color": "#222"
        },

        hovertemplate=hover_template,
    )

    return fig


def count_customer_tenure(data_frame, column_name, title="Chart Title",
                          title_font_size=30,
                          showlegend=False, hover_template="None", chart_theme="plotly_dark"):
    def tenure_bins(x):
        if x >= 0 and x <= 12:
            return "0-12 Months"

        if x > 12 and x <= 24:
            return "13-24 Months"

        if x > 24 and x <= 36:
            return "25-36 Months"

        if x > 36 and x <= 48:
            return "37-48 Months"

        if x > 48 and x <= 60:
            return "49-60 Months"

        if x > 60 and x <= 72:
            return "61-72 Months"

    customer_via_tenure = data_frame[column_name].apply(tenure_bins).value_counts().sort_index()

    fig = px.scatter(
        data_frame=customer_via_tenure,
        color=customer_via_tenure.index,
        size=customer_via_tenure,
        color_discrete_sequence=used_color,
        title=title,
        labels={"index": "Tenure (Months)", "value": "Frequency of Customers"},
        template=chart_theme,
        opacity=0.8
    )

    if chart_theme == "plotly_dark":
        fig.update_layout(
            paper_bgcolor='#171C31',
            plot_bgcolor='rgba(255,255,255,0)',
        )

    fig.update_layout(

        showlegend=showlegend,
        title={
            "font": {
                "size": title_font_size,
                "family": "tahoma"
            }
        },
        hoverlabel={
            "bgcolor": "#222",
            "font_size": 16,
            "font_family": "tahoma"
        }
    )

    fig.update_traces(
        textfont={
            "size": 18,
            "family": "tahoma",
            "color": "#222"
        },

        hovertemplate=hover_template,
        marker=dict(line=dict(color='#333', width=1)),
    )

    return fig

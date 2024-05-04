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


def count_online_backup(data_frame, column_name, title="Chart Title",
                        title_font_size=30, showlegend=False,
                        hover_template="None", chart_theme="plotly_dark"):
    phone_services = data_frame[column_name].value_counts()

    fig = px.pie(
        names=phone_services.index,
        values=phone_services,
        title=title,
        color_discrete_sequence=used_color,
        hole=0.5,
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

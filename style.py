import plotly.express as px
from dash_bootstrap_templates import load_figure_template
from const import *

colors = {
    'background': '#111111',
    'text': '#32fbe2'
}

templates = [
    "vapor",
]

load_figure_template(templates)

#"colorway": ["#6829ad", "#e14b56", "#06a843", "#f7c200", "#51a0f6"], "font": {"color": "#32fbe2", 

# PLOTS
dist_colors = ['#30123b', '#4145ab', '#4675ed', '#39a2fc', '#1bcfd4', '#24eca6', '#61fc6c', '#a4fc3b',
               '#d1e834', '#f3c63a', '#fe9b2d', '#f36315', '#d93806', '#b11901', '#7a0402']

dist_plot_cmap = px.colors.sequential.Turbo

template = templates[0]

# CARDS
card_style = {
    'background': '#6829ad',
    'color':'white',
    'text-align': 'center',
    'font-size': '12px',
    'font-weight': 600,
}

join_card_style = {
    'background': '#6829ad',
    'color':'white',
    'text-align': 'center',
    'font-size': '12px',
    'font-weight': 600,
    'margin-left': '10px',
    'margin-right': '10px'
}

intro_card_style = {
    'background': '#6829ad',
    'color':'white',
    'text-align': 'left',
    'font-size': '12px',
    'font-weight': 600,
    'margin':'50px'
}

calc_card_style = {
    'background': '#6829ad',
    'text-align': 'left',
    'margin':'25px'
}

card_row_style = {
    'padding':'10px',
    'align-items': 'center',
    'justify-content': 'center',
}

# TABS
tab_style = {
    "background": "#6829ad",
    'text-transform': 'uppercase',
    'color': 'white',
    'border': 'grey',
    'font-size': '14px',
    'font-weight': 600,
    'align-items': 'center',
    'justify-content': 'center',
    'border-radius': '4px',
    'padding':'6px',
    'border-radius': '0px'
}

selected_tab_style = {
    "background": "#4145ab",
    'text-transform': 'uppercase',
    'border-style': 'solid',
    'border-color': '#4675ed',
    'color': 'white',
    'font-size': '14px',
    'font-weight': 600,
    'align-items': 'center',
    'justify-content': 'center',
    'border-radius': '0px',
    'padding':'6px',
    'border-radius': '0px'
}

tab_row_style = {
    'padding': '5px'
}

# RADIO BUTTONS
radio_style = {
    'color':'white',
    'font-size': '16px',
    'padding':'6px',
    'padding-right':'65px',
    'text-align': 'right',
}

radio_input_style = {
    "margin-right": "5px",
    "margin-left": "20px",
    "margin-top": "25px",
    'justify-content': 'right',
    'align-items': 'right',
}

# DATE PICKER
date_picker_style = {
    "margin-left": "100px",
    "margin-top": "20px",
}

period_style = {
    "margin-left": "0px",
    "margin-top": "10px",
    'color':'black',
}

# TABLES
table_style_data = {
    'backgroundColor': '#30123b',
    'color': 'white',
    'font-size':'13px'
}

table_style_data_conditional = [
    {
        'if': {'row_index': 'odd'},
        'backgroundColor': '#6829ad',
    },
    {
        'if': {'filter_query': '{legend} eq "current time"'},
        'backgroundColor': 'green',
    },
]

table_style_cell = {
    'padding-left':'10px',
    'padding-right': '10px',
    'font-size':'13px'
}

table_style_cell_conditional = [
    {
        'if': {'column_id': 'Date'},
        'textAlign': 'left'
    },
    {
        'if': {'column_id': 'Start time'},
        'textAlign': 'left'
    },
    {
        'if': {'column_id': 'End time'},
        'textAlign': 'left'
    },
]

table_style_header = {
    'backgroundColor': 'rgb(30, 30, 30)',
    'color': 'white',
    'fontWeight': 'bold',
    'font-size':'13px'
}

table_style_header_conditional = [

]

period_table_style_data = {
    'backgroundColor': '#30123b',
    'color': 'white',
    'margin-right' : '30px',
    'padding-right': '20px',
}

title_style = {
                'textAlign': 'left',
                'color': 'white',
                'margin-left': '0px'
            }

text_style = {
                'textAlign': 'left',
                'color': 'white',
                'font-size': '11px',
                'margin': '20px'
            }

dropdown_style = {
    'color':'black',
    'font-size': '20px',
    'padding':'6px',
    'padding-right':'10px',
}

dropdown_style_ = {
    'color':'black',
}

table_style_cell_cheapest = {
    'padding-left':'10px',
    'padding-right':'10px',
    'margin-right': '250px',
    'font-size':'12px'
}
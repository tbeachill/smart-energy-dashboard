import plotly.express as px
from dash_bootstrap_templates import load_figure_template

templates = [
    "vapor",
]

load_figure_template(templates)

#"colorway": ["#6829ad", "#e14b56", "#06a843", "#f7c200", "#51a0f6"], "font": {"color": "#32fbe2", 

# PLOTS
dist_colors = ['#30123b', '#4145ab', '#4675ed', '#39a2fc', '#1bcfd4', '#24eca6', '#61fc6c', '#a4fc3b', '#d1e834', '#f3c63a', '#fe9b2d', '#f36315', '#d93806', '#b11901', '#7a0402']

dist_plot_cmap = px.colors.sequential.Turbo

template = templates[0]

# CARDS
card_style = {
    'background': 'red',
    'align-items': 'center',
    'justify-content': 'center',
    'text-align': 'center',
    'font-size': '14px',
    'font-weight': 600,
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
    'padding':'6px'
}


tabs_styles_hidden = {
    'display':'inline'
}

tabs_styles_display = {
    'display':'none'
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
    'padding':'6px'
}

from dash import html
from style import *

colors = {
    'background': '#111111',
    'text': '#32fbe2'
}

# regions
r_codes = [
    {"label": "East England", "value": 'A'},
    {"label": "East Midlands", "value": 'B'},
    {"label": "London", "value": 'C'},
    {"label": "Merseyside and North Wales", "value": 'D'},
    {"label": "West Midlands", "value": 'E'},
    {"label": "North-East England", "value": 'F'},
    {"label": "North-West England", "value": 'G'},
    {"label": "South England", "value": 'H'},
    {"label": "South-East England", "value": 'J'},
    {"label": "South Wales", "value": 'K'},
    {"label": "South-West England", "value": 'L'},
    {"label": "Yorkshire", "value": 'M'},
    {"label": "South Scotland", "value": 'N'},
    {"label": "North Scotland", "value": 'P'},
]

# products
p_codes = {
    "Agile" : "A",
    "Cosy" : "C",
    "Flux" : "F",
    "Go" : "G",
    "Tracker" : "T",
    "Intelligent" : "I"
}

p_codes_r = dict(map(reversed, p_codes.items()))

intro_text = [html.H1("Smart Energy Dashboard"),
              html.H2("Select a region from the dropdown at the top to get started.", style={'color':'white'}),

              ]

intro_text_2 = [
              html.P("Smart tariffs can save you money if you are able to move you energy usage outside of certain times, all you need is a smart meter. This website will allow you to view the different smart tariffs offered by Octopus Energy and compare the prices over time.\nAn overview of the different smart tariffs are below.", style={'font-size':'16px', 'color':'white', 'font-weight': 'bold'}),
              html.Br(),
              html.H5("Agile Octopus"),
              html.P("With Agile Octopus, you get access to half-hourly energy prices, tied to wholesale prices and updated daily. So when wholesale electricity prices drop, your bills can too particularly if you can shift your daily electricity use outside of peak times.", style={'font-size':'16px', 'color':'white'}),
              html.H5("Octopus Tracker"),
              html.P("Tracker is a tariff for gas and electric where the price is updated each day based on wholesale prices.", style={'font-size':'16px', 'color':'white'}),
              html.H5("Octopus Go"),
              html.P("Octopus Go is designed for electric vehicle owners and gives 4 hours of cheap electricity each night.", style={'font-size':'16px', 'color':'white'}),
              html.H5("Cosy Octopus"),
              html.P("Cosy Octopus is designed for owners of heat-pumps. You get two 3-hour periods of cheap electricity per day.", style={'font-size':'16px', 'color':'white'}),
              html.H5("Octopus Flux"),
              html.P("Octopus Flux is an import and export tariff optimised to give you the best rates for consuming and selling your energy and supporting the grid during peak periods.", style={'font-size':'16px', 'color':'white'}),
              html.H5("Intelligent Octopus"),
              html.P("Intelligent Octopus is designed for electric vehicle owners. Intelligent Octopus pairs with your EV or charger to always smart charge on your super cheap rate, and at the very greenest times. You get 6 hours of cheap energy each night.", style={'font-size':'16px', 'color':'white'}),

]

card_style = {"width": "10rem",
                'textAlign': 'center',
                    'color': colors['text']}

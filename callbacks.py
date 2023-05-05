from dash import html, dash_table, dcc, Input, Output
from datetime import date
import dash_bootstrap_components as dbc
from dateutil.relativedelta import relativedelta
from const import *
from dash.exceptions import PreventUpdate
from graph_utils import graph_utils as g
from cards import cards
from style import *

def get_callbacks(app):
        # enable the tariff tabs and remove the intro text once a region has been selected
    @app.callback(
        [Output("A", "disabled"), Output("T", "disabled"), Output("G", "disabled"), Output("C", "disabled"), Output("F", "disabled"), Output("I", "disabled"), Output("intro", "hidden")],
        Input('region-dropdown', 'value'),
        prevent_initial_call=True
    )
    def enable_tab(region):
        return False, False, False, False, False, False, True
    
    @app.callback(
        [Output("tariff-tabs", "style")],
        Input('region-dropdown', 'value'),
        prevent_initial_call=True
    )
    def enable_tab(region):
        return tabs_styles_display

    @app.callback(Output('card-row', 'children'),
                [Input('tariff-tabs', 'value'), Input("region-dropdown", "value")], prevent_initial_call=True)
    def render_cards(tab, region):
        if tab != 'C' and tab != 'T':    
            return html.Div([html.Div([dbc.Card(id='sc-card')],style={'width': '32%', 'display': 'inline-block'}), html.Div([dbc.Card(id='current-price-1')],style={'width': '32%', 'display': 'inline-block'}), html.Div([dbc.Card(id='current-price-2')],style={'width': '32%', 'display': 'inline-block'})])
        else:
            return html.Div([html.Div([dbc.Card(id='sc-card')],style={'width': '32%', 'display': 'inline-block'}), html.Div([dbc.Card(id='current-price-1')],style={'width': '32%', 'display': 'inline-block'})])
        
    # display content for each tab once selected
    @app.callback(Output('tab-content', 'children'),
                [Input('tariff-tabs', 'value'), Input("region-dropdown", "value")])
    def render_content(tab, region):
        if tab == 'A':
            return html.Div([
                            dcc.RadioItems(['Electricity', 'Gas'], 'Electricity', id='energy-type', inline=True, style={'display': 'none'}),                        
                            dcc.RadioItems(['Import', 'Export'], 'Import', id='impex', inline=True),
                            dcc.DatePickerRange(
                                id='datepicker1',
                                display_format='DD/MM/YYYY',
                                min_date_allowed=date(2022, 12, 1),
                                max_date_allowed=date(date.today().year, date.today().month, date.today().day),
                                initial_visible_month=date(date.today().year, date.today().month, 1),
                                start_date=date.today() - relativedelta(days=1),
                                end_date=date.today() + relativedelta(days=2)
                            ),
                            dcc.Graph(id='im-ex'),
                            dcc.Graph(id='agile-dist'),
                            dash_table.DataTable(id='table-a-dist'),
                            dash_table.DataTable(id='table-a', hidden_columns=['legend'], style_data_conditional=[
                                {
                                    'if': {
                                        'filter_query': '{legend} eq "current time"'
                                    },
                                    'backgroundColor': 'green',
                                },
                            ])
                        ])
        if tab == 'T':
            return html.Div([
                            dcc.RadioItems(['Electricity', 'Gas'], 'Electricity', id='energy-type', inline=True),
                            dcc.DatePickerRange(
                                id='datepicker2',
                                display_format='DD/MM/YYYY',
                                min_date_allowed=date(2022, 12, 1),
                                max_date_allowed=date(date.today().year, date.today().month, date.today().day),
                                initial_visible_month=date(date.today().year, date.today().month, 1),
                                start_date=date.today() - relativedelta(months=1),
                                end_date=date.today() + relativedelta(days=2)
                            ),
                            dcc.Graph(id='gas-elec'),
                            dcc.Graph(id='tracker-dist'),
                            dash_table.DataTable(id='table-t-dist'),
                            dash_table.DataTable(id='table-t', hidden_columns=['legend'], style_data_conditional=[
                                {
                                    'if': {
                                        'filter_query': '{legend} eq "current time"'
                                    },
                                    'backgroundColor': 'green',
                                },
                            ])
                    ])
        if tab == 'G':
            return html.Div([
                            dcc.RadioItems(['Electricity', 'Gas'], 'Electricity', id='energy-type', inline=True, style={'display': 'none'}),
                            dcc.DatePickerRange(
                                id='datepicker3',
                                display_format='DD/MM/YYYY',
                                min_date_allowed=date(2022, 12, 1),
                                max_date_allowed=date(date.today().year, date.today().month, date.today().day),
                                initial_visible_month=date(date.today().year, date.today().month, 1),
                                start_date=date.today() - relativedelta(days=1),
                                end_date=date.today() + relativedelta(days=2)
                            ),
                            dcc.Graph(id='im-ex-g'),
                            dash_table.DataTable(id='table-g', hidden_columns=['legend'], style_data_conditional=[
                                {
                                    'if': {
                                        'filter_query': '{legend} eq "current time"'
                                    },
                                    'backgroundColor': 'green',
                                },
                            ])
                    ])
        if tab == 'C':
            return html.Div([
                            dcc.RadioItems(['Electricity', 'Gas'], 'Electricity', id='energy-type', inline=True, style={'display': 'none'}),
                            dcc.DatePickerRange(
                                id='datepicker4',
                                display_format='DD/MM/YYYY',
                                min_date_allowed=date(2022, 12, 1),
                                max_date_allowed=date(date.today().year, date.today().month, date.today().day),
                                initial_visible_month=date(date.today().year, date.today().month, 1),
                                start_date=date.today() - relativedelta(days=1),
                                end_date=date.today() + relativedelta(days=2)
                            ),
                            dcc.Graph(id='im-ex-c'),
                            dash_table.DataTable(id='table-c', hidden_columns=['legend'], style_data_conditional=[
                                {
                                    'if': {
                                        'filter_query': '{legend} eq "current time"'
                                    },
                                    'backgroundColor': 'green',
                                },
                            ])
                    ])
        if tab == 'F':
            return html.Div([
                            dcc.RadioItems(['Electricity', 'Gas'], 'Electricity', id='energy-type', inline=True, style={'display': 'none'}),
                            dcc.RadioItems(['Import', 'Export'], 'Import', id='impex-2', inline=True),
                            dcc.DatePickerRange(
                                id='datepicker5',
                                display_format='DD/MM/YYYY',
                                min_date_allowed=date(2022, 12, 1),
                                max_date_allowed=date(date.today().year, date.today().month, date.today().day),
                                initial_visible_month=date(date.today().year, date.today().month, 1),
                                start_date=date.today() - relativedelta(days=1),
                                end_date=date.today() + relativedelta(days=2)
                            ),
                            dcc.Graph(id='im-ex-f'),
                            dash_table.DataTable(id='table-f', hidden_columns=['legend'], style_data_conditional=[
                                {
                                    'if': {
                                        'filter_query': '{legend} eq "current time"'
                                    },
                                    'backgroundColor': 'green',
                                },
                            ])
                    ])
        if tab == 'I':
            return html.Div([
                            dcc.RadioItems(['Electricity', 'Gas'], 'Electricity', id='energy-type', inline=True, style={'display': 'none'}),
                            dcc.DatePickerRange(
                                id='datepicker6',
                                display_format='DD/MM/YYYY',
                                min_date_allowed=date(2022, 12, 1),
                                max_date_allowed=date(date.today().year, date.today().month, date.today().day),
                                initial_visible_month=date(date.today().year, date.today().month, 1),
                                start_date=date.today() - relativedelta(days=1),
                                end_date=date.today() + relativedelta(days=2)
                            ),
                            dcc.Graph(id='im-ex-i'),
                            dash_table.DataTable(id='table-i', hidden_columns=['legend'], style_data_conditional=[
                                {
                                    'if': {
                                        'filter_query': '{legend} eq "current time"'
                                    },
                                    'backgroundColor': 'green',
                                },
                            ])
                    ])


    # standing charge card to update with tariff and region
    @app.callback(
        Output("sc-card", "children"),
        [Input("region-dropdown", "value"), Input("tariff-tabs", "value"), Input("energy-type", "value")],
        prevent_initial_call=True
    )
    def update_options(region, tariff, energy_type):
        if not region:
            raise PreventUpdate
        
        global tabs_disabled
        tabs_disabled = False

        return cards.sc(tariff, region, energy_type)

    # current price card
    @app.callback(
        Output("current-price-1", "children"),
        [Input("region-dropdown", "value"), Input("tariff-tabs", "value"), Input("energy-type", "value")]
    )
    def card_one(region, tariff, energy_type):
        if not region or not tariff:
            raise PreventUpdate

        return cards.one(tariff, region, energy_type)

    # card 3
    @app.callback(
        Output("current-price-2", "children"),
        [Input("region-dropdown", "value"), Input("tariff-tabs", "value")]
    )
    def card_two(region, tariff):
        if not region or not tariff:
            raise PreventUpdate
        
        return cards.two(tariff, region)


    # return import or export graph based on selection
    @app.callback(
        [Output("im-ex", "figure"), Output("table-a", "data")],
        [Input("impex", "value"), Input("region-dropdown", "value"), Input("tariff-tabs", "value"), Input("datepicker1", "start_date"), Input("datepicker1", "end_date")]
    )
    def change_impex(value, region, tariff, start_date, end_date):
        if not region or not tariff:
            raise PreventUpdate
        
        return g.price(tariff, region, start_date, end_date, value)
        
    # return import or export FLUX graph based on selection
    @app.callback(
        [Output("im-ex-f", "figure"), Output("table-f", "data")],
        [Input("impex-2", "value"), Input("region-dropdown", "value"), Input("tariff-tabs", "value"), Input("datepicker5", "start_date"), Input("datepicker5", "end_date")]
    )
    def change_impex(value, region, tariff, start_date, end_date):
        if not region or not tariff:
            raise PreventUpdate
        
        return g.price(tariff, region, start_date, end_date, value)
        
        
    # return go import graph
    @app.callback(
        [Output("im-ex-g", "figure"), Output("table-g", "data")],
        [Input("region-dropdown", "value"), Input("tariff-tabs", "value"), Input("datepicker3", "start_date"), Input("datepicker3", "end_date")]
    )
    def change_impex(region, tariff, start_date, end_date):
        if not region or not tariff:
            raise PreventUpdate
        
        return g.price(tariff, region, start_date, end_date)

    # return cosy import graph
    @app.callback(
        [Output("im-ex-c", "figure"), Output("table-c", "data")],
        [Input("region-dropdown", "value"), Input("tariff-tabs", "value"), Input("datepicker4", "start_date"), Input("datepicker4", "end_date")]
    )
    def change_impex(region, tariff, start_date, end_date):
        if not region or not tariff:
            raise PreventUpdate
        
        return g.price(tariff, region, start_date, end_date)

    # return intelligent import graph
    @app.callback(
        [Output("im-ex-i", "figure"), Output("table-i", "data")],
        [Input("region-dropdown", "value"), Input("tariff-tabs", "value"), Input("datepicker6", "start_date"), Input("datepicker6", "end_date")]
    )
    def change_impex(region, tariff, start_date, end_date):
        if not region or not tariff:
            raise PreventUpdate
        
        return g.price(tariff, region, start_date, end_date)

    # return agile distribution graph based on date selection
    @app.callback(
        [Output("agile-dist", "figure"), Output("table-a-dist", "data")],
        [Input("impex", "value"), Input("region-dropdown", "value"), Input("datepicker1", "start_date"), Input("datepicker1", "end_date"), Input("tariff-tabs", "value")]
    )
    def change_distribution(direction, region, start_date, end_date, tariff):
        if not region or not tariff:
            raise PreventUpdate
        
        return g.dist(tariff, region, start_date, end_date, direction=direction)
        
    # return tracker gas or electric graph based on selection
    @app.callback(
        [Output("gas-elec", "figure"), Output("table-t", "data")],
        [Input("energy-type", "value"), Input("region-dropdown", "value"), Input("tariff-tabs", "value"), Input("datepicker2", "start_date"), Input("datepicker2", "end_date")]
    )
    def change_energy(energy_type, region, tariff, start_date, end_date):
        if not region or not tariff:
            raise PreventUpdate
        
        return g.price(tariff, region, start_date, end_date, type=energy_type)

    # return tracker distribution graph based on date selection
    @app.callback(
        [Output("tracker-dist", "figure"), Output("table-t-dist", "data")],
        [Input("energy-type", "value"), Input("region-dropdown", "value"), Input("datepicker2", "start_date"), Input("datepicker2", "end_date"), Input("tariff-tabs", "value")]
    )
    def change_distribution(energy_type, region, start_date, end_date, tariff):
        if not region or not tariff:
            raise PreventUpdate
        
        return g.dist(tariff, region, start_date, end_date, type=energy_type)

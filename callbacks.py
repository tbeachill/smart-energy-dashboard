from dash import html, dash_table, dcc, Input, Output
from datetime import date
import dash_bootstrap_components as dbc
from dateutil.relativedelta import relativedelta
from const import *
from dash.exceptions import PreventUpdate
from graph_utils import graph_utils as g
from cards import cards
from style import *
from dash.dash_table.Format import Format, Group, Scheme, Symbol
from stats_utils import stats_utils as s

def get_callbacks(app):   
    @app.callback(
            [Output("tariff-tabs", "children"), Output("intro", "hidden")],
            Input('region-dropdown', 'value'),
            prevent_initial_call=True
    )
    def show_tabs(region):
        return [[
        dcc.Tab(label='Agile',       style=tab_style, selected_style=selected_tab_style, value='A', id='A'),
        dcc.Tab(label='Tracker',     style=tab_style, selected_style=selected_tab_style, value='T', id='T'),
        dcc.Tab(label='Go',          style=tab_style, selected_style=selected_tab_style, value='G', id='G'),
        dcc.Tab(label='Cosy',        style=tab_style, selected_style=selected_tab_style, value='C', id='C'),
        dcc.Tab(label='Flux',        style=tab_style, selected_style=selected_tab_style, value='F', id='F'),
        dcc.Tab(label='Intelligent', style=tab_style, selected_style=selected_tab_style, value='I', id='I'),
    ], True]
    
    @app.callback(Output('card-row', 'children'),
                [Input('tariff-tabs', 'value'), Input("region-dropdown", "value")], prevent_initial_call=True)
    def render_cards(tab, region):
        if tab != 'C' and tab != 'T':    
            return dbc.Row([dbc.Col(dbc.Card(id='sc-card')), dbc.Col(dbc.Card(id='current-price-1')), dbc.Col(dbc.Card(id='current-price-2'))])
        else:
            return dbc.Row([dbc.Col(dbc.Card(id='sc-card')), dbc.Col(dbc.Card(id='current-price-1'))])
        
    # display content for each tab once selected
    @app.callback(Output('tab-content', 'children'),
                [Input('tariff-tabs', 'value'), Input("region-dropdown", "value")])
    def render_content(tab, region):
        if tab == 'A':
            return html.Div([
                            dash_table.DataTable(id='table-stats-today', style_header=table_style_header, style_data=table_style_data, style_as_list_view=True),
                            dbc.Row([
                                dcc.RadioItems(['Electricity', 'Gas'], 'Electricity', id='energy-type', inline=True, style={'display': 'none'}),                        
                                dbc.Col(dcc.DatePickerRange(
                                    id='datepicker1',
                                    display_format='DD/MM/YYYY',
                                    min_date_allowed=date(2022, 12, 1),
                                    max_date_allowed=date(date.today().year, date.today().month, date.today().day),
                                    initial_visible_month=date(date.today().year, date.today().month, 1),
                                    start_date=date.today() - relativedelta(days=1),
                                    end_date=date.today() + relativedelta(days=2),
                                    style=date_picker_style
                                ), width=6),
                                dbc.Col(dcc.RadioItems(['Import', 'Export'], 'Import', id='impex', inline=True, style=radio_style, inputStyle=radio_input_style), width=6)], justify='between'),
                            dcc.Graph(id='im-ex'),
                            dbc.Row([dbc.Col(html.Div(children='Find cheapest time period', style=title_style))]),
                            dbc.Row([dbc.Col(dcc.Dropdown([{'label': '0:30', 'value': 1}, {'label': '1:00', 'value': 2}, {'label': '1:30', 'value': 3}, {'label': '2:00', 'value': 4}, {'label': '2:30', 'value': 5}, {'label': '3:00', 'value': 6}, {'label': '3:30', 'value': 7}, {'label': '4:00', 'value': 8}, {'label': '4:30', 'value': 9}, {'label': '5:00', 'value': 10}, {'label': '5:30', 'value': 11}, {'label': '6:00', 'value': 12}, ], '0:30', id='cheapest-dropdown', style=date_picker_style)),
                                     dbc.Col(width=1),
                                     dbc.Col(dash_table.DataTable(id='table-cheapest', style_header=table_style_header, style_data=table_style_data, style_cell=table_style_cell_cheapest)),
                                     dbc.Col(width=1)]),
                            dcc.Graph(id='agile-dist'),
                            dash_table.DataTable(id='table-a-dist', style_header=table_style_header, style_data=table_style_data),
                            dcc.Graph(id='box-a'),
                            dash_table.DataTable(id='table-a', hidden_columns=['legend'], style_data=table_style_data, style_data_conditional=table_style_data_conditional, style_header=table_style_header, style_header_conditional=table_style_header_conditional, style_cell=table_style_cell, style_cell_conditional=table_style_cell_conditional, style_as_list_view=True)
                        ])
        if tab == 'T':
            return html.Div([
                            dbc.Row([
                                dbc.Col(dcc.DatePickerRange(
                                    id='datepicker2',
                                    display_format='DD/MM/YYYY',
                                    min_date_allowed=date(2022, 12, 1),
                                    max_date_allowed=date(date.today().year, date.today().month, date.today().day),
                                    initial_visible_month=date(date.today().year, date.today().month, 1),
                                    start_date=date.today() - relativedelta(months=1),
                                    end_date=date.today() + relativedelta(days=2),
                                    style=date_picker_style
                                ), width=6),
                                dbc.Col(dcc.RadioItems(['Electricity', 'Gas'], 'Electricity', id='energy-type', inline=True, style=radio_style, inputStyle=radio_input_style), width=6)], justify='between'),
                            dcc.Graph(id='gas-elec'),
                            dcc.Graph(id='tracker-dist'),
                            dash_table.DataTable(id='table-t-dist', style_header=table_style_header, style_data=table_style_data),
                            dcc.Graph(id='box-t'),
                            dash_table.DataTable(id='table-t', hidden_columns=['legend'], style_data=table_style_data, style_data_conditional=table_style_data_conditional, style_header=table_style_header, style_header_conditional=table_style_header_conditional, style_cell=table_style_cell, style_cell_conditional=table_style_cell_conditional, style_as_list_view=True)
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
                                end_date=date.today() + relativedelta(days=2),
                                style=date_picker_style
                            ),
                            dcc.Graph(id='im-ex-g'),
                            dash_table.DataTable(id='table-g', hidden_columns=['legend'], style_data=table_style_data, style_data_conditional=table_style_data_conditional, style_header=table_style_header, style_header_conditional=table_style_header_conditional, style_cell=table_style_cell, style_cell_conditional=table_style_cell_conditional, style_as_list_view=True)
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
                                end_date=date.today() + relativedelta(days=2),
                                style=date_picker_style
                            ),
                            dcc.Graph(id='im-ex-c'),
                            dash_table.DataTable(id='table-c', hidden_columns=['legend'], style_data=table_style_data, style_data_conditional=table_style_data_conditional, style_header=table_style_header, style_header_conditional=table_style_header_conditional, style_cell=table_style_cell, style_cell_conditional=table_style_cell_conditional, style_as_list_view=True)
                    ])
        if tab == 'F':
            return html.Div([
                            dcc.RadioItems(['Electricity', 'Gas'], 'Electricity', id='energy-type', inline=True, style={'display': 'none'}),
                            dbc.Row([
                                    dbc.Col(dcc.DatePickerRange(
                                        id='datepicker5',
                                        display_format='DD/MM/YYYY',
                                        min_date_allowed=date(2022, 12, 1),
                                        max_date_allowed=date(date.today().year, date.today().month, date.today().day),
                                        initial_visible_month=date(date.today().year, date.today().month, 1),
                                        start_date=date.today() - relativedelta(days=1),
                                        end_date=date.today() + relativedelta(days=2),
                                        style=date_picker_style
                                    ), width=6),
                                    dbc.Col(dcc.RadioItems(['Import', 'Export'], 'Import', id='impex-2', inline=True, style=radio_style, inputStyle=radio_input_style), width=6)
                            ], justify="between"),
                            dcc.Graph(id='im-ex-f'),
                            dash_table.DataTable(id='table-f', hidden_columns=['legend'], style_data=table_style_data, style_data_conditional=table_style_data_conditional, style_header=table_style_header, style_header_conditional=table_style_header_conditional, style_cell=table_style_cell, style_cell_conditional=table_style_cell_conditional, style_as_list_view=True)
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
                                end_date=date.today() + relativedelta(days=2),
                                style=date_picker_style
                            ),
                            dcc.Graph(id='im-ex-i'),
                            dash_table.DataTable(id='table-i', hidden_columns=['legend'], style_data=table_style_data, style_data_conditional=table_style_data_conditional, style_header=table_style_header, style_header_conditional=table_style_header_conditional, style_cell=table_style_cell, style_cell_conditional=table_style_cell_conditional, style_as_list_view=True)
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
    
    @app.callback(
            Output("table-cheapest", "data"),
            [Input("impex", "value"), Input("region-dropdown", "value"), Input("cheapest-dropdown", "value")]
    )
    def get_cheapest(direction, region, period):
        if not region:
            raise PreventUpdate
        
        return s.cheapest_time(direction, region, period)
    
    @app.callback(
        Output("table-stats-today", "data"),
        [Input("impex", "value"), Input("region-dropdown", "value"), Input("tariff-tabs", "value")]
    )
    def stats_today(direction, region, tariff):
        return s.today(tariff, region, direction)
    
    @app.callback(
        Output("box-a", "figure"),
        [Input("impex", "value"), Input("region-dropdown", "value"), Input("tariff-tabs", "value")]
    )
    def box_plot_a(direction, region, tariff):
        if not region or not tariff:
            raise PreventUpdate
        
        return g.box_6m(tariff, region, direction=direction)
    
    @app.callback(
        Output("box-t", "figure"),
        [Input("energy-type", "value"), Input("region-dropdown", "value"), Input("tariff-tabs", "value")]
    )
    def box_plot_t(energy_type, region, tariff):
        if not region or not tariff:
            raise PreventUpdate
        
        return g.box_6m(tariff, region, energy_type=energy_type)
        
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

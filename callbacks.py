from dash import Input, Output, dash
from datetime import date
from dateutil.relativedelta import relativedelta
from const import *
from dash.exceptions import PreventUpdate
from graph_utils import graph_utils as g
from cards import cards
from style import *
from stats_utils import stats_utils as s
from flask import Flask, request, send_from_directory

def get_callbacks(app):
    @app.callback(
            [Output("region-dropdown", "value"), Output("tabs", "value")],
            Input("url", "pathname")
    )
    def display_page(pathname):
        paths = [x for x in pathname.split('/') if x]

        if len(paths) > 1:
            return [paths[0], p_codes[paths[1]]]
        else:
            return [paths[0], dash.no_update]
        

def get_callbacks(app):
    @app.server.route('/robots.txt')
    @app.server.route('/sitemap.xml')
    def static_from_root():
        return send_from_directory(app.server.static_folder, request.path[1:])
    

    @app.callback(
            Output("download", "data"),
            Input("url", "pathname")
    )
    def display_document(pathname):
        paths = [x for x in pathname.split('/') if x]

        if paths[0] == "robots.txt":
            print(paths)
            return dict(content="/robots.txt", filename="robots.txt")
        else:
            raise PreventUpdate


    @app.callback(
        Output("url", "pathname"),
        [Input("region-dropdown", "value"), Input("tabs", "value")]
    )
    def update_url(region, tariff):
        if not region:
            raise PreventUpdate
        
        if tariff == "tab-1":
            return "/" + region
        else:
            return f"/{region}/{p_codes_r[tariff]}"
    

    @app.callback(
        [Output("tariff-tab-div", "hidden"), Output("intro", "hidden"),
         Output("intro2", "hidden"), Output("intro-card", "hidden")],
        Input("region-dropdown", "value")
    )
    def show_tabs(region):
        if not region:
            raise PreventUpdate
        
        return [False, True, True, True]
    

    @app.callback(
        [Output("card-row-div", "hidden"), Output("card-2", "hidden"), 
         Output("stats-today-tab-div", "hidden"), Output("date-direction-div", "hidden"),
         Output("date-picker-div", "hidden"), Output("date-picker", "start_date"),
         Output("date-picker", "end_date"),
         Output("price-plot-div", "hidden"), Output("price-calculator-title-div", "hidden"),
         Output("price-calculator-div", "hidden"), Output("dist-plot-div", "hidden"),
         Output("dist-tab-div", "hidden"), Output("box-plot-div", "hidden"),
         Output("data-tab-div", "hidden"), Output("type-radio-div", "hidden"),
         Output("type-radio", "options"), Output("type-radio", "value")],
        [Input("tabs", "value"), Input("region-dropdown", "value")],
        prevent_initial_call=True
    )
    def switch_tab(tab, region):
        if not tab or not region or tab == "tab-1":
            raise PreventUpdate
        
        T, F = True, False
        if tab != 'T':
            start = date.today() - relativedelta(days=1)
            end = date.today() + relativedelta(days=2)
        else:
            start = date.today() - relativedelta(months=1)
            end = date.today() + relativedelta(days=2)
        
        if tab == 'A':
            return [F, F, F, F, F, start, end, F, F, F, F, F, F, F, F, ["Import", "Export"], "Import"]
        elif tab == 'T':
            return [F, T, T, F, F, start, end, F, T, T, F, F, F, F, F, ["Electricity", "Gas"], "Electricity"]
        elif tab == 'F':
            return [F, F, T, F, T, start, end, F, T, T, T, T, T, F, F, ["Import", "Export"], "Import"]
        elif tab == 'C':
            return [F, T, T, F, T, start, end, F, T, T, T, T, T, F, T, ["Import", "Export"], "Import"]
        elif tab == 'G':
            return [F, F, T, F, T, start, end, F, T, T, T, T, T, F, T, ["Import", "Export"], "Import"]
        else:
            return [F, F, T, F, T, start, end, F, T, T, T, T, T, F, T, ["Import", "Export"], "Import"]


    @app.callback(
        [Output("join-card", "children"), Output("sc-card", "children"),
         Output("card-1", "children"), Output("card-2", "children")],
        [Input("tabs", "value"), Input("region-dropdown", "value"), Input("type-radio", "value")],
         prevent_initial_call=True
    )
    def get_card_data(tariff, region, td):
        if not region or not tariff or tariff == "tab-1":
            raise PreventUpdate
        
        if tariff == 'T':
            return [cards.join(tariff, region), cards.sc(tariff, region, td),
                    cards.one(tariff, region, td), cards.two(tariff, region)]
        else:
            return [cards.join(tariff, region), cards.sc(tariff, region),
                    cards.one(tariff, region), cards.two(tariff, region)]
        

    @app.callback(
        Output("agile-stats-today", "data"),
        [Input("tabs", "value"), Input("region-dropdown", "value"), Input("type-radio", "value")],
         prevent_initial_call=True
    )
    def agile_today_stats(tariff, region, td):
        if not region or tariff != 'A' or tariff == "tab-1":
            raise PreventUpdate
        
        return s.today(tariff, region, td)


    @app.callback(
        [Output("price-plot", "figure"), Output("data-table", "data")],
        [Input("tabs", "value"), Input("region-dropdown", "value"), Input("type-radio", "value"),
         Input("date-picker", "start_date"), Input("date-picker", "end_date")],
         prevent_initial_call=True
    )
    def get_price_data(tariff, region, td, start, end):
        if not region or not tariff or tariff == "tab-1":
            raise PreventUpdate
        
        if td in ["Gas", "Electricity"]:
            return g.price(tariff, region, start, end, energy_type=td)
        else:
            return g.price(tariff, region, start, end, direction=td)
    

    @app.callback(
        Output("table-best", "data"),
        [Input("region-dropdown", "value"), Input("type-radio", "value"),
         Input("best-dropdown", "value"), Input("tabs", "value")],
         prevent_initial_call=True
    )
    def get_best_time_agile(region, td, period, tab):
        if not region or period not in range(0,13) or tab != 'A':
            raise PreventUpdate
            
        return s.best_time(td, region, period)
    

    @app.callback(
        [Output("dist-plot", "figure"), Output("dist-table", "data")],
        [Input("tabs", "value"), Input("region-dropdown", "value"), Input("type-radio", "value"),
         Input("date-picker", "start_date"), Input("date-picker", "end_date")],
         prevent_initial_call=True
    )
    def get_dist_data(tariff, region, td, start, end):
        if not region or tariff == "tab-1" or tariff not in ['A', 'T']:
            raise PreventUpdate
            
        if tariff == 'A':
            return g.dist(tariff, region, start, end, direction=td)
        else:
            return g.dist(tariff, region, start, end, energy_type=td)
        

    @app.callback(
        Output("box-plot", "figure"),
        [Input("tabs", "value"), Input("region-dropdown", "value"),
         Input("type-radio", "value")],
         prevent_initial_call=True
    )
    def get_box_data(tariff, region, td):
        if not region or tariff == "tab-1" or tariff not in ['A', 'T']:
            raise PreventUpdate
            
        if tariff == 'A':
            return g.box_6m(tariff, region, direction=td)
        else:
            return g.box_6m(tariff, region, energy_type=td)
        
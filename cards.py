from const import *
from sql_utils import sql_utils as sql
import dash_bootstrap_components as dbc
from dash import html
from dt_utils import dt_utils as dt
from style import *

class cards:
    # standing charge card
    def sc(tariff, region, energy_type="E"):
        card = dbc.Card(
            dbc.CardBody(
                [
                    html.H6("Standing Charge", className="card-title"),
                    html.H5(str(sql.query(f"SELECT cost FROM StandingCharges WHERE tariff = '{tariff}' AND \
                                          region_code = '{region}' AND type = '{energy_type[0]}'")['cost'][0]) + "p",
                                          className="card-subtitle"),
                ]
            ),
            style=card_style,
        )

        return card

    def one(tariff, region, energy_type="E"):
        if energy_type[0] == "E":
            table = "ElectricityImport"
        else:
            table = "GasImport"

        card = dbc.Card(
            dbc.CardBody(
                [
                    html.H6("Current Import", className="card-title"),
                    html.H5(str(sql.query(f"SELECT unit_rate FROM {table} WHERE tariff = '{tariff}' AND \
                                          region_code = '{region}' AND date = '{dt.get_period(tariff)}'")['unit_rate'][0]) +
                                          "p", className="card-subtitle"),
                ]
            ),
            style=card_style
        )

        return card

    def two(tariff, region):  
        if tariff == "T":
            title = "Current Gas Cost"
            contents = str(sql.query(f"SELECT unit_rate FROM GasImport WHERE tariff = '{tariff}' \
                                     AND region_code = '{region}' AND date = '{dt.get_period(tariff)}'")['unit_rate'][0]) + "p"
        elif tariff in ['G', 'I', 'C']:
            title = "Fixed SEG Export"
            contents = "4.1p"
        else:
            title = "Current Export"
            contents = str(sql.query(f"SELECT unit_rate FROM ElectricityExport WHERE tariff = '{tariff}' AND \
                                     region_code = '{region}' AND date = '{dt.get_period(tariff)}'")['unit_rate'][0]) + "p"

        card = dbc.Card(
            dbc.CardBody(
                [
                    html.H6(title, className="card-title"),
                    html.H5(contents, className="card-subtitle"),
                ]
            ),
            style=card_style
        )

        return card
    
    def join(tariff, region):
        join_card = dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H6("Join Octopus", className="card-title"),
                        html.H6("Get £50 credit"),
                        html.P(
                            "Join Octopus with the code light-beach-323 or click the button "
                            "for £50 account credit.",
                        style={'font-size':'13px'}),                        
                        dbc.Button("Join Now", color="primary", href="https://share.octopus.energy/light-beach-323", style={'font-size':'13px'}),
                    ]
                ),
            ],
            style=card_style,
        )
        return join_card

from const import *
from sql_utils import sql_utils as sql
import dash_bootstrap_components as dbc
from dash import html
from dt_utils import dt_utils as dt

class cards:
    # standing charge card
    def sc(tariff, region, energy_type="E"):
        card = dbc.Card(
            dbc.CardBody(
                [
                    html.H3("Standing Charge", className="card-title"),
                    html.H2(str(sql.query(f"SELECT cost FROM StandingCharges WHERE tariff = '{tariff}' AND region_code = '{region}' AND type = '{energy_type[0]}'")['cost'][0]) + "p", className="card-subtitle"),
                ]
            ),
            style=card_style,
            className="w-75 mb-3",
            color="secondary", inverse=True, outline=False
        )

        return card

    def one(tariff, region, energy_type):
        if energy_type[0] == "E":
            table = "ElectricityImport"
        else:
            table = "GasImport"

        card = dbc.Card(
            dbc.CardBody(
                [
                    html.H3("Current Import", className="card-title"),
                    html.H2(str(sql.query(f"SELECT unit_rate FROM {table} WHERE tariff = '{tariff}' AND region_code = '{region}' AND date = '{dt.get_period(tariff)}'")['unit_rate'][0]) + "p", className="card-subtitle"),
                ]
            ),
            style=card_style,
            className="w-75 mb-3",
        )

        return card

    def two(tariff, region):  
        if tariff == "T":
            title = "Current Gas Cost"
            contents = str(sql.query(f"SELECT unit_rate FROM GasImport WHERE tariff = '{tariff}' AND region_code = '{region}' AND date = '{dt.get_period(tariff)}'")['unit_rate'][0]) + "p"
        elif tariff == "G" or tariff == "I":
            title = "Fixed SEG Export"
            contents = "4.1p"
        else:
            title = "Current Export"
            contents = str(sql.query(f"SELECT unit_rate FROM ElectricityExport WHERE tariff = '{tariff}' AND region_code = '{region}' AND date = '{dt.get_period(tariff)}'")['unit_rate'][0]) + "p"

        card = dbc.Card(
            dbc.CardBody(
                [
                    html.H3(title, className="card-title"),
                    html.H2(contents, className="card-subtitle"),
                ]
            ),
            style=card_style,
            className="w-75 mb-3",
        )

        return card

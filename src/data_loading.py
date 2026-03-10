"""
Functions for loading and cleaning the project datasets.
"""

import geopandas as gpd
import pandas as pd


def load_volcanoes(path="data/volcano_list.csv"):
    """
    Load and clean the volcanic eruption dataset.

    Arguments:
        path (str): path to the volcano CSV

    Returns:
        pd.DataFrame: eruptions with Year, Name, Latitude, Longitude, VEI columns
    """
    df = pd.read_csv(path, encoding="utf-8", encoding_errors="replace")
    df.columns = df.columns.str.strip().str.lstrip("\ufeff")
    # Drop rows without coordinates or year
    df = df.dropna(subset=["Year", "Latitude", "Longitude"])
    df["Year"] = df["Year"].astype(int)
    return df.reset_index(drop=True)


def load_crises(path="data/CrisisConsequencesData_NavigatingPolycrisis_2023.03.csv"):
    """
    Load and clean the Seshat Crisis Consequences dataset.

    Arguments:
        path (str): path to the crisis CSV

    Returns:
        pd.DataFrame: crisis cases with polity info and outcome columns
    """
    df = pd.read_csv(path, encoding="utf-8", encoding_errors="replace")
    df.columns = df.columns.str.strip().str.lstrip("\ufeff")
    # Drop rows missing polity name or dates
    df = df.dropna(subset=["Polity.Name", "Polity.Date.From", "Polity.Date.To"])
    df["Polity.Date.From"] = df["Polity.Date.From"].astype(int)
    df["Polity.Date.To"] = df["Polity.Date.To"].astype(int)
    return df.reset_index(drop=True)


def load_egypt_transitions(path="data/EgyptPT Data.csv"):
    """
    Load and clean the Egyptian power transitions dataset.

    Arguments:
        path (str): path to the Egypt PT CSV

    Returns:
        pd.DataFrame: one row per ruler transition with metadata
    """
    df = pd.read_csv(path, encoding="utf-8-sig")
    df.columns = df.columns.str.strip()
    # Keep only rows with a valid transition year; "U*" values become NaN
    df["End.reign.Transition"] = pd.to_numeric(
        df["End.reign.Transition"], errors="coerce"
    )
    df = df.dropna(subset=["End.reign.Transition"])
    df["End.reign.Transition"] = df["End.reign.Transition"].astype(int)
    return df.reset_index(drop=True)


def load_cliopatria(path="data/cliopatria_polities_only.geojson"):
    """
    Load the Cliopatria polity geometries.

    Arguments:
        path (str): path to the GeoJSON file

    Returns:
        gpd.GeoDataFrame: polities with Name, FromYear, ToYear, geometry
    """
    gdf = gpd.read_file(path)
    gdf["FromYear"] = gdf["FromYear"].astype(int)
    gdf["ToYear"] = gdf["ToYear"].astype(int)
    return gdf

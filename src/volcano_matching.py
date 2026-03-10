"""
Functions to find the nearest volcanic eruption for a given event and time window.
"""

import numpy as np
import pandas as pd
from pyproj import Geod

# WGS84 ellipsoid for geodetic distance calculations
_GEOD = Geod(ellps="WGS84")


def geodetic_distance_km(lon1, lat1, lon2, lat2):
    """
    Compute geodetic distance in km between two points on the WGS84 ellipsoid.

    Arguments:
        lon1 (float): longitude of point 1
        lat1 (float): latitude of point 1
        lon2 (float): longitude of point 2
        lat2 (float): latitude of point 2

    Returns:
        float: distance in kilometres
    """
    _, _, dist_m = _GEOD.inv(lon1, lat1, lon2, lat2)
    return dist_m / 1000.0


def nearest_eruption(event_year, event_lon, event_lat, volcanoes_df, window_years):
    """
    Find the closest volcanic eruption (by distance) that occurred within
    a time window before the event year.

    Arguments:
        event_year (int): year of the crisis or transition
        event_lon (float): longitude of the polity centroid
        event_lat (float): latitude of the polity centroid
        volcanoes_df (pd.DataFrame): eruptions with Year, Latitude, Longitude
        window_years (int): how many years before the event to look back

    Returns:
        dict: {distance_km, volcano_name, volcano_year, vei} or None if no match
    """
    if pd.isna(event_lon) or pd.isna(event_lat):
        return None

    candidates = volcanoes_df[
        (volcanoes_df["Year"] >= event_year - window_years)
        & (volcanoes_df["Year"] <= event_year)
    ]

    if candidates.empty:
        return None

    distances = candidates.apply(
        lambda row: geodetic_distance_km(
            event_lon, event_lat, row["Longitude"], row["Latitude"]
        ),
        axis=1,
    )

    idx = distances.idxmin()
    return {
        "distance_km": distances[idx],
        "volcano_name": candidates.loc[idx, "Name"],
        "volcano_year": candidates.loc[idx, "Year"],
        "vei": candidates.loc[idx, "VEI"],
    }


def add_volcano_distances(df, year_col, lon_col, lat_col, volcanoes_df, windows):
    """
    For each row in df, compute the distance to the nearest eruption for each
    time window and add the results as new columns.

    Arguments:
        df (pd.DataFrame): events with year and centroid coordinates
        year_col (str): column with event year
        lon_col (str): column with polity longitude
        lat_col (str): column with polity latitude
        volcanoes_df (pd.DataFrame): volcanic eruptions
        windows (list[int]): time windows in years to try (e.g. [25, 50, 100])

    Returns:
        pd.DataFrame: df with added columns for each window:
                      'dist_km_{w}yr', 'nearest_volcano_{w}yr',
                      'volcano_year_{w}yr', 'vei_{w}yr'
    """
    df = df.copy()
    for window in windows:
        results = df.apply(
            lambda row: nearest_eruption(
                row[year_col],
                row[lon_col],
                row[lat_col],
                volcanoes_df,
                window,
            ),
            axis=1,
        )
        df[f"dist_km_{window}yr"] = results.apply(
            lambda r: r["distance_km"] if r else np.nan
        )
        df[f"nearest_volcano_{window}yr"] = results.apply(
            lambda r: r["volcano_name"] if r else None
        )
        df[f"volcano_year_{window}yr"] = results.apply(
            lambda r: r["volcano_year"] if r else np.nan
        )
        df[f"vei_{window}yr"] = results.apply(lambda r: r["vei"] if r else np.nan)
    return df

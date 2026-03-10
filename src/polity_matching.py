"""
Fuzzy name matching between crisis/transition polity names and Cliopatria geometries.
"""

import geopandas as gpd
import pandas as pd
from thefuzz import process


def get_centroid_lookup(cliopatria_gdf):
    """
    Build a lookup from Cliopatria polity name to representative centroid (lon, lat).

    Centroids are computed in an equal-area projection then converted back to
    WGS84. When a polity has multiple time-slice entries, centroids are averaged.

    Arguments:
        cliopatria_gdf (gpd.GeoDataFrame): Cliopatria polities (WGS84)

    Returns:
        dict: {polity_name: (lon, lat)}
    """
    # Compute centroids in equal-area projection to avoid geographic CRS warning
    projected = cliopatria_gdf.to_crs("ESRI:54009")
    centroids_proj = projected.geometry.centroid
    # Convert centroids back to WGS84
    centroids_gdf = gpd.GeoDataFrame(
        {"Name": cliopatria_gdf["Name"].values},
        geometry=centroids_proj,
        crs="ESRI:54009",
    ).to_crs("EPSG:4326")
    centroids_gdf["lon"] = centroids_gdf.geometry.x
    centroids_gdf["lat"] = centroids_gdf.geometry.y

    lookup = (
        centroids_gdf.groupby("Name")[["lon", "lat"]]
        .mean()
        .apply(lambda r: (r["lon"], r["lat"]), axis=1)
        .to_dict()
    )
    return lookup


def fuzzy_match_names(query_names, reference_names, score_cutoff=70):
    """
    Match a list of query names to the best fuzzy match in a reference list.

    Arguments:
        query_names (list[str]): names to match (e.g. from crisis dataset)
        reference_names (list[str]): candidate names (e.g. Cliopatria polity names)
        score_cutoff (int): minimum similarity score (0-100) to accept a match

    Returns:
        dict: {query_name: matched_name or None}
    """
    matches = {}
    for name in query_names:
        result = process.extractOne(name, reference_names, score_cutoff=score_cutoff)
        matches[name] = result[0] if result else None
    return matches


def assign_centroids(df, name_col, cliopatria_gdf, score_cutoff=70):
    """
    Add lon/lat centroid columns to a dataframe by fuzzy-matching polity names
    to Cliopatria geometries.

    Arguments:
        df (pd.DataFrame): input dataframe with a polity name column
        name_col (str): column name containing polity names
        cliopatria_gdf (gpd.GeoDataFrame): Cliopatria polities
        score_cutoff (int): minimum fuzzy match score

    Returns:
        pd.DataFrame: df with added columns 'matched_polity', 'lon', 'lat'
    """
    centroid_lookup = get_centroid_lookup(cliopatria_gdf)
    reference_names = list(centroid_lookup.keys())
    query_names = df[name_col].dropna().unique().tolist()

    name_map = fuzzy_match_names(query_names, reference_names, score_cutoff)

    df = df.copy()
    df["matched_polity"] = df[name_col].map(name_map)
    df["lon"] = df["matched_polity"].map(
        lambda n: centroid_lookup[n][0] if (isinstance(n, str) and n in centroid_lookup) else None
    )
    df["lat"] = df["matched_polity"].map(
        lambda n: centroid_lookup[n][1] if (isinstance(n, str) and n in centroid_lookup) else None
    )
    return df

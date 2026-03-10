"""
Simple statistical analysis of volcano proximity vs. crisis outcomes.
"""

import numpy as np
import pandas as pd
from scipy import stats


OUTCOME_COLS_CRISIS = [
    "decline",
    "collapse",
    "epidemic",
    "downw.mob",
    "extermination",
    "uprising",
    "civil.war",
    "century.plus",
    "fragmentation",
    "conquest",
    "assassin",
    "depose",
]

OUTCOME_COLS_EGYPT = [
    "Overturn",
    "Assassination.Predecessor",
    "Intra.elite",
    "Military.revolt",
    "Popular.uprising",
    "Separatist.rebellion",
    "External.invasion",
    "External.interference",
]


def binarize_outcomes(df, cols):
    """
    Convert outcome columns to binary (1 = present, 0 = absent/unknown).

    Values of 1 or "1" map to 1; everything else (0, "U.susp", "A", NaN) maps to 0.

    Arguments:
        df (pd.DataFrame): dataframe with outcome columns
        cols (list[str]): columns to binarize

    Returns:
        pd.DataFrame: copy of df with binarized columns
    """
    df = df.copy()
    for col in cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).clip(0, 1).astype(int)
    return df


def compute_severity_score(df, outcome_cols):
    """
    Sum binarized outcome columns into a total severity score per row.

    Arguments:
        df (pd.DataFrame): dataframe with binarized outcome columns
        outcome_cols (list[str]): columns to sum

    Returns:
        pd.Series: severity score per row
    """
    cols_present = [c for c in outcome_cols if c in df.columns]
    return df[cols_present].sum(axis=1)


def spearman_distance_vs_outcome(df, dist_col, outcome_col):
    """
    Compute Spearman correlation between distance to nearest eruption and
    a numeric outcome column, dropping NaN rows.

    Arguments:
        df (pd.DataFrame): analysis dataframe
        dist_col (str): column with distance in km
        outcome_col (str): column with outcome variable (numeric)

    Returns:
        dict: {rho, pvalue, n}
    """
    sub = df[[dist_col, outcome_col]].dropna()
    if len(sub) < 5:
        return {"rho": np.nan, "pvalue": np.nan, "n": len(sub)}
    rho, p = stats.spearmanr(sub[dist_col], sub[outcome_col])
    return {"rho": rho, "pvalue": p, "n": len(sub)}


def mannwhitney_near_vs_far(df, dist_col, outcome_col, threshold_km):
    """
    Compare outcome between "near" (distance <= threshold) and "far" groups
    using Mann-Whitney U test.

    Arguments:
        df (pd.DataFrame): analysis dataframe
        dist_col (str): column with distance in km
        outcome_col (str): numeric outcome column
        threshold_km (float): distance cutoff for near/far split

    Returns:
        dict: {u_stat, pvalue, n_near, n_far, median_near, median_far}
    """
    sub = df[[dist_col, outcome_col]].dropna()
    near = sub[sub[dist_col] <= threshold_km][outcome_col]
    far = sub[sub[dist_col] > threshold_km][outcome_col]
    if len(near) < 3 or len(far) < 3:
        return {
            "u_stat": np.nan,
            "pvalue": np.nan,
            "n_near": len(near),
            "n_far": len(far),
            "median_near": np.nan,
            "median_far": np.nan,
        }
    u, p = stats.mannwhitneyu(near, far, alternative="two-sided")
    return {
        "u_stat": u,
        "pvalue": p,
        "n_near": len(near),
        "n_far": len(far),
        "median_near": near.median(),
        "median_far": far.median(),
    }


def run_correlation_table(df, dist_cols, outcome_cols):
    """
    Build a summary table of Spearman correlations between each distance column
    and each outcome column.

    Arguments:
        df (pd.DataFrame): analysis dataframe
        dist_cols (list[str]): distance columns (one per time window)
        outcome_cols (list[str]): outcome columns to test

    Returns:
        pd.DataFrame: table with columns [dist_col, outcome_col, rho, pvalue, n]
    """
    rows = []
    for dist_col in dist_cols:
        if dist_col not in df.columns:
            continue
        for outcome_col in outcome_cols:
            if outcome_col not in df.columns:
                continue
            result = spearman_distance_vs_outcome(df, dist_col, outcome_col)
            rows.append(
                {
                    "time_window": dist_col,
                    "outcome": outcome_col,
                    "rho": result["rho"],
                    "pvalue": result["pvalue"],
                    "n": result["n"],
                }
            )
    return pd.DataFrame(rows)

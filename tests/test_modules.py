"""
Basic tests for the analysis modules.
"""

import numpy as np
import pandas as pd
import pytest

from src.analysis import binarize_outcomes, compute_severity_score, run_correlation_table
from src.polity_matching import fuzzy_match_names
from src.volcano_matching import geodetic_distance_km, nearest_eruption


class TestGeodeticDistance:
    def test_same_point_is_zero(self):
        assert geodetic_distance_km(10.0, 50.0, 10.0, 50.0) == pytest.approx(0.0, abs=1)

    def test_known_distance(self):
        # London (~51.5N, 0W) to Paris (~48.9N, 2.3E): ~340 km
        dist = geodetic_distance_km(0.0, 51.5, 2.3, 48.9)
        assert 300 < dist < 400


class TestNearestEruption:
    def make_volcanoes(self):
        return pd.DataFrame(
            {
                "Year": [-200, -100, -50],
                "Name": ["VolcA", "VolcB", "VolcC"],
                "Latitude": [40.0, 40.0, 40.0],
                "Longitude": [10.0, 100.0, 10.5],
                "VEI": [6, 7, 5],
            }
        )

    def test_finds_nearest_within_window(self):
        v = self.make_volcanoes()
        result = nearest_eruption(0, 10.0, 40.0, v, window_years=60)
        assert result is not None
        assert result["volcano_name"] == "VolcC"

    def test_returns_none_outside_window(self):
        v = self.make_volcanoes()
        result = nearest_eruption(0, 10.0, 40.0, v, window_years=10)
        assert result is None

    def test_returns_none_for_missing_coords(self):
        v = self.make_volcanoes()
        result = nearest_eruption(0, np.nan, 40.0, v, window_years=100)
        assert result is None


class TestBinarizeOutcomes:
    def test_numeric_one_stays_one(self):
        df = pd.DataFrame({"col": [1, 0, "U.susp", None]})
        result = binarize_outcomes(df, ["col"])
        assert list(result["col"]) == [1, 0, 0, 0]

    def test_severity_score(self):
        df = pd.DataFrame({"a": [1, 0], "b": [1, 1], "c": [0, 1]})
        scores = compute_severity_score(df, ["a", "b", "c"])
        assert list(scores) == [2, 2]


class TestFuzzyMatch:
    def test_exact_match(self):
        result = fuzzy_match_names(["Rome"], ["Rome", "Athens", "Carthage"])
        assert result["Rome"] == "Rome"

    def test_no_match_below_cutoff(self):
        result = fuzzy_match_names(["XYZ123"], ["Rome", "Athens"], score_cutoff=70)
        assert result["XYZ123"] is None

    def test_partial_match(self):
        result = fuzzy_match_names(["Roman Empire"], ["Roman Empire", "Byzantine"])
        assert result["Roman Empire"] == "Roman Empire"


class TestCorrelationTable:
    def test_table_shape(self):
        df = pd.DataFrame(
            {
                "dist_50yr": [100, 200, 300, 400, 500],
                "outcome_a": [1, 0, 1, 0, 1],
            }
        )
        table = run_correlation_table(df, ["dist_50yr"], ["outcome_a"])
        assert len(table) == 1
        assert "rho" in table.columns
        assert "pvalue" in table.columns

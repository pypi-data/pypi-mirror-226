import osmnx as ox
from shapely.geometry import LineString, Point
import geopandas as gpd
import numpy as np
import keplergl
import random
import pandas as pd

import unittest
import pytest

from ..src.route_generator import *


# Search query for a geographic area
query = "City of Westminster"
# Get the walking network for the query location
G = ox.graph.graph_from_place(query, network_type="walk", simplify=True)
# Project the graph to WGS84
Gp = ox.project_graph(G, to_crs="4326")


class TestUniqueRoutes(unittest.TestCase):
    def test_(self):
        # To make two randomised routes
        two_routes = generate_routes(
                                    Gp,
                                    time_from="2015-02-26 21:42:53",
                                    time_until=None,
                                    time_strategy="fixed",
                                    route_strategy="many-many",
                                    origin_destination_coords=None,
                                    total_routes=2,
                                    walk_speed=1.4,
                                    frequency="1s",
                                    )
        # Unique number of route ids should equal 2
        self.assertEqual(two_routes['id'].nunique(), 2, "incorrect number of unique ids")


# Test case 1: Check if the generated DataFrame has the correct structure
def test_generated_dataframe_structure():
    routes_df = generate_routes(
        Gp,
        time_from="2020-02-26 20:42:53",
        time_until="2020-02-26 21:42:53",
        time_strategy="random",
        route_strategy="one-many",
        origin_destination_coords=[51.499127, -0.153522],
        total_routes=3,
        walk_speed=1.4,
        frequency="1s",
    )
    
    assert isinstance(routes_df, pd.DataFrame)
    assert "time" in routes_df.columns
    assert "geometry" in routes_df.columns
    assert "id" in routes_df.columns

# Test case 2: Check if the number of generated routes is correct
def test_number_of_generated_routes():
    routes_df = generate_routes(
        Gp,
        time_from="2020-02-26 20:42:53",
        time_until="2020-02-26 21:42:53",
        time_strategy="random",
        route_strategy="one-many",
        origin_destination_coords=[51.499127, -0.153522],
        total_routes=3,
        walk_speed=1.4,
        frequency="1s",
    )
    
    assert len(routes_df["id"].unique()) == 3

# Test case 3: Check if all generated routes have valid timestamps
def test_generated_routes_timestamps():
    routes_df = generate_routes(
        Gp,
        time_from="2020-02-26 20:42:53",
        time_until="2020-02-26 21:42:53",
        time_strategy="random",
        route_strategy="one-many",
        origin_destination_coords=[51.499127, -0.153522],
        total_routes=3,
        walk_speed=1.4,
        frequency="1s",
    )
    
    assert routes_df["time"].dtype == "datetime64[ns]"

# Test case 4: Check if generated routes have valid Shapely geometries (Points)
def test_generated_routes_geometry():
    routes_df = generate_routes(
        Gp,
        time_from="2020-02-26 20:42:53",
        time_until="2020-02-26 21:42:53",
        time_strategy="random",
        route_strategy="one-many",
        origin_destination_coords=[51.499127, -0.153522],
        total_routes=3,
        walk_speed=1.4,
        frequency="1s",
    )
    
    assert all(isinstance(geometry, Point) for geometry in routes_df["geometry"])

# Test case 5: Check if the specified time_from and time_until constraints are respected
def test_generated_routes_time_constraints():
    routes_df = generate_routes(
        Gp,
        time_from="2020-02-26 20:42:53",
        time_until="2020-02-26 21:42:53",
        time_strategy="random",
        route_strategy="one-many",
        origin_destination_coords=[51.499127, -0.153522],
        total_routes=3,
        walk_speed=1.4,
        frequency="1s",
    )
    
    earliest_timestamp_per_user = routes_df.groupby('id')['time'].min()

    assert earliest_timestamp_per_user.min() >= pd.Timestamp("2020-02-26 20:42:53")
    assert earliest_timestamp_per_user.max() <= pd.Timestamp("2020-02-26 21:42:53")

if __name__ == "__main__":
    pytest.main()

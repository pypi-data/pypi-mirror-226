# movingpeople

**movingpeople** is a Python package that allows you to generate synthetic data of travel routes in a graph network. It provides a convenient and efficient way to create datasets of travel routes, which are time-stamped based on travel speed. Whether you are working on transportation analysis, urban planning, or simulating human movement patterns, :movingpeople: is a powerful tool to generate realistic and customizable travel data.

## Key Features

* Synthetic Data Generation: With **movingpeople**, you can generate synthetic travel data by simulating movement on the graph network. The package incorporates various parameters such as travel speed, time intervals, and start/end points to create diverse and customizable travel routes.

* Timestamped Routes: Each generated travel route is timestamped according to the travel speed. This enables you to analyze temporal aspects of movement, such as traffic patterns, congestion, or time-based simulations.

* Customizable Parameters: **movingpeople** provides a range of parameters that can be customized to fit your specific use case. You can control aspects such as the number of routes to generate, the distribution of travel speeds, the duration of routes, and more.

## Installation

To install **movingpeople**, you can use pip, the Python package installer. Open a terminal or command prompt and run the following command:

```python
pip install movingpeople
```



### A quick example

Here's a basic example to get you started with **movingpeople**:
```python
from movingpeople import visualise_route, generate_routes
import osmnx as ox

# Search query for a geographic area
query = "City of Westminster"
# Get the walking network for the query location
G = ox.graph.graph_from_place(query, network_type="walk", simplify=True)
# Project the graph to WGS84
Gp = ox.project_graph(G, to_crs="4326")

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

```

In the example above, we first create a ``Graph`` object to define the transportation network. We then generate two routes which have the same start time however randomised origins and destinations.

## Conclusion

**movingpeople** is a versatile Python package for generating synthetic travel route data on graph networks. It offers a range of features and customizable parameters to create realistic and timestamped routes. Whether you are conducting transportation analysis, urban planning, or simulating human movement patterns, :movingpeople: can help you generate valuable datasets for research and analysis. Start using :movingpeople: today and unlock insights into the dynamics of movement in various contexts.


This project is under active development.

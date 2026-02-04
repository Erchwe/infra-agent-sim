# graph.py

import networkx as nx


def build_service_graph(services: dict):
    """
    Node: service agent
    Edge: dependency (A depends on B)
    """
    G = nx.DiGraph()

    for service_id, service in services.items():
        G.add_node(service_id)

        for dep in service.dependencies:
            G.add_edge(dep, service_id)

    return G

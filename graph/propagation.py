# propagation.py

def propagate_failure(graph, failure_scores):
    propagated = {}

    for node in graph.nodes:
        inbound = graph.predecessors(node)
        propagated[node] = sum(failure_scores.get(src, 0) for src in inbound)

    return propagated

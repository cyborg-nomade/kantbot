"""The concrete graph must satisfy the already accepted read-only contract."""

from kantbot.interfaces import ProvenanceView
from kantbot.provenance import ProvenanceGraph


def cognitive_view(graph: ProvenanceGraph) -> ProvenanceView:
    return graph

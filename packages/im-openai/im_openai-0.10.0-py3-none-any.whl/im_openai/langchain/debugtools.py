from typing import Dict
from uuid import UUID


def find_leaves(parents: Dict[UUID, UUID]) -> set[UUID]:
    return set(child for child in parents.keys() if child not in parents.values())


def dump_node(parents: Dict[UUID, UUID], node: UUID, suffix: str = ""):
    if node not in parents:
        print(f"{node}{suffix}")
    else:
        parent = parents[node]
        dump_node(parents, parent, f" -> {node}{suffix}")


def dump_tree(parents: Dict[UUID, UUID]):
    for leaf in find_leaves(parents):
        dump_node(parents, leaf)

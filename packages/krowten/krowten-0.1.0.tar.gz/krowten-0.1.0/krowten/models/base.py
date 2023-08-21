from abc import ABC, abstractmethod
from typing import Any


class Node:
    _parent = None

    def __int__(self, label: str | None = None, value: Any = None):
        self._label = label
        self._value = value
        self._parent = None

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent_node):
        self._parent = parent_node

    @property
    def label(self) -> str:
        return self._label

    @property
    def value(self):
        return self._value

    def __str__(self):
        return f"<Node: {self.label}>: {self.value}"


class Edge:
    def __init__(self, start: Node, end: Node, bi_directional: bool = True):
        self._start_node = start
        self._end_node = end
        self._bi_d = bi_directional

    @property
    def start_node(self):
        return self._start_node

    @property
    def end_node(self):
        return self._end_node

    @property
    def bi_directional(self):
        return self._bi_d


class Base(ABC):
    @property
    def nodes(self):
        raise NotImplementedError

    @property
    def edges(self):
        raise NotImplementedError

    @abstractmethod
    def add_node(self, node: Node, neighbours: list[Node] | None = None):
        raise NotImplementedError

    @abstractmethod
    def remove_node(self, node: Node):
        raise NotImplementedError

    @abstractmethod
    def add_edge(self, edge: Edge):
        raise NotImplementedError

    @abstractmethod
    def remove_edge(self, edge: Edge):
        raise NotImplementedError

    @abstractmethod
    def get_adjacency_view(self):
        raise NotImplementedError

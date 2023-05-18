import datetime
import json
from dataclasses import dataclass

import peewee as pw
from playhouse.sqlite_ext import JSONField
from persistent.models.BaseModel import BaseModel


class BipartiteGraph(BaseModel):
    bigraph_id = pw.AutoField()
    number_of_items = pw.IntegerField()
    number_of_players = pw.IntegerField()
    number_of_edges = pw.IntegerField()
    fractional_k = pw.DoubleField(null=True)
    integral_k = pw.IntegerField(null=True)
    fractional_solution_time = pw.DoubleField(null=True)
    integral_solution_time = pw.DoubleField(null=True)
    items = JSONField()
    item_sets = JSONField()
    players = JSONField(null=True)
    edges = JSONField(null=True)
    fractional_values = JSONField(null=True)
    integral_values = JSONField(null=True)
    creation_date = pw.DateTimeField(default=datetime.datetime.now)

    def get_items(self) -> list['BipartiteGraph.Item']:
        items: list[BipartiteGraph.Item] = list()
        for item in self.items:
            items.append(BipartiteGraph.Item(**item))

        return sorted(items, key=lambda x: x.index)

    def get_players(self) -> list['BipartiteGraph.Player']:
        pass

    def get_item_set(self) -> list['BipartiteGraph.ItemSet']:
        pass

    def get_edges(self) -> list['BipartiteGraph.Edge']:
        pass

    class Meta:
        table_name = 'bipartite_graph'

    @dataclass
    class Item:
        node: int
        value: float

    @dataclass
    class Player:
        node: str

    @dataclass
    class ItemSet:
        start: int
        end: int

    @dataclass
    class Edge:
        from_node: str
        to_node: str

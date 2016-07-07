"""
MATCH (a:b {c: 'd'}) RETURN a.b -> [find(Node, Identifier('a'), props]
"""


class Runnable:
    def run(self):
        raise NotImplementedError


class Operation(Runnable):
    def __init__(self, method, *args):
        """A wrapper for executor"""
        self.method = method
        self.args = args

    def run(self):
        self.method(*self.args)


class QueryPlan:
    def __init__(self, operations):
        self.operations = operations


class LogicalQueryPlan(QueryPlan):
    def __init__(self, query):
        """

        Args:
            query (Query):
        """
        pass


class PhysicalQueryPlan(QueryPlan):
    def __init__(self, logical_query):
        """"""
        pass

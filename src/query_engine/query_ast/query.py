from src.lib.utils import ensure_tuple


class SubQuery:
    """Docstring for QueryModel. """

    def __init__(self, commands):
        """
        Args:
            commands (List[Cluase]):
        """
        self._clauses = ensure_tuple(commands)

    @property
    def clauses(self):
        return self._clauses

    def __repr__(self):
        return str(self._clauses)

    def __eq__(self, other):
        return self._clauses == other.clauses


class Query:
    """Docstring for Query. """

    def __init__(self, queries):
        """
        Defines a whole query.

        Args:
            queries (List[SubQuery]):
        """
        self._queries = ensure_tuple(queries)

    def __repr__(self):
        return str(self._queries)

    def __eq__(self, other):
        return self._queries == other._queries

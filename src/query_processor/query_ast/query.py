from src.lib.utils import ensure_tuple
from src.lib.utils import collect_identifiers


class SubQuery:
    """Docstring for QueryModel. """

    def __init__(self, clauses):
        """
        Args:
            clauses (List[Cluase]):
            identifiers (List[Identifiers]): Keeps sub query identifiers for
                faster lookup
        """
        self._clauses = ensure_tuple(clauses)

    def get_identifiers(self):
        return collect_identifiers(self._clauses)

    @property
    def clauses(self):
        return self._clauses

    def __repr__(self):
        return str(self._clauses)

    def __eq__(self, other):
        return self._clauses == other.clauses


class Query:
    """The root of all evil."""

    def __init__(self, queries):
        """
        Defines a whole query.

        Keeps identifiers list for faster lookup.
        Args:
            queries (List[SubQuery]):
        """
        self._queries = ensure_tuple(queries)
        self.identifiers_map = Query.get_identifiers_map(queries)

    @staticmethod
    def get_identifiers_map(sub_queries):
        """
        Collects Identifiers from the sub-queries and generates a name-dict for
            objects (same name may be present in multiple identifiers)
        Args:
            sub_queries (List[SubQuery]):
        Returns:
            dict:
        """
        name_to_identifiers = {}
        # collect identifiers lists from the subqueries
        identifiers = [sub_query.get_identifiers() for
                       sub_query in
                       sub_queries]
        identifiers = set().union(*identifiers)

        # now populate the map
        for identifier in identifiers:
            name = identifier.name
            if name_to_identifiers.get(name):
                name_to_identifiers[name].add(identifier)
            else:
                name_to_identifiers[name] = {identifier}
        return name_to_identifiers

    @property
    def sub_queries(self):
        return self._queries

    def __repr__(self):
        return str(self._queries)

    def __eq__(self, other):
        return self._queries == other._queries

class Command:

    """ Defines a basic command for the db (MATCH, WHERE, ...) """

    def __init__(self, clause, expression):
        """TODO: to be defined1.

        Args:
            clause (Clause): TODO
            expression (Expression): TODO


        """
        self._clause = clause
        self._expression = expression
        
 
class SubQuery:

    """Docstring for QueryModel. """

    def __init__(self, commands):
        """TODO: to be defined1.

        Args:
            commands (List[Command]):
        """
        self._commands = commands
               

class Query:

    """Docstring for Query. """

    def __init__(self, queries):
        """
        Defines a whole query.

        Args:
            queries (List[SubQuery]):
        """
        self._queries = queries
 

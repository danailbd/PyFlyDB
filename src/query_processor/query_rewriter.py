from query_processor.query_ast.plan import QueryPlan

class DummyStorageManager:
    def find_node(self, identifier=None, *properties):
        pass

    def find_edge(self, identifier=None, *properties):
        pass

clause_to_method = {

}




class QueryRewriter:

    def __init__(self, storage_manager=None):
        self.storage_manager = storage_manager

    def rewrite(self, query):
        """

        Args:
            query (Query):

            find -> populate -> find for each -> ...

        Returns:
            QueryPlan:
        """
        # TODO
        # identifiers -> to single instance

        for sub_query in query.sub_queries():
            sub_query

        return query



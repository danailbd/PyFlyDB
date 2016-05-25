class QueryEngine:
    
    def __init__(self, storage_api):
        self.storage_api = storage_api

    def execute_query(self, query):
    """
    Executes a passed query. Follows the steps:
    - Parse query -> QueryModel
    - Optimize query
    - execute the query using the storage_api
    query - String
    """
        query_model = QueryParser.parse(query)
        query_model = QueryOptimizer.optimize(query_model)

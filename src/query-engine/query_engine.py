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
        query = QueryParser.parse(query)
        query = QueryOptimizer.optimize(query_model)
        self.__execute_query()


    def __execute_command(command, *args):
        # use commands dict
        pass
    command = op[0]
            subcommands = op[1:]
            QueryEngine.__execute_command(op, *subcommands)



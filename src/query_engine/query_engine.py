from src.query_engine.query_parser import QueryParser

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
        #TODO query = QueryOptimizer.optimize(query_model)
        self.__execute_query()

    @staticmethod
    def __apply_post_processors():
        '''Return, sort, ...'''
        pass



    def __execute_command(command, *args):
        # use commands dict
        pass


command = op[0]
subcommands = op[1:]
QueryEngine.__execute_command(op, *subcommands)
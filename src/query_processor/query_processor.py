from src.query_processor.query_parser import QueryParser
import asyncio


class QueryProcessor:
    def __init__(self, plan_executor):
        self.executor = plan_executor

    async def process(self, query):
        """
        Executes a passed query. Follows the steps:
        - Parse query -> QueryModel
        - Query rewrite
        - Optimize query
        - execute the query using the storage_api
        Args:
            query (str):
        """
        query = QueryParser.parse_query(query)
        plan = QueryProcessor.query_rewrite(query)

        # TODO query = QueryOptimizer.optimize(query)

        # plan executor
        self.executor.execute(plan)


    @staticmethod
    def query_rewrite(query):
        # TODO
        return  query



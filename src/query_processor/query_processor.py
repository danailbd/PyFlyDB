from query_processor.plan_executor import PlanExecutor
from query_processor.query_rewriter import QueryRewriter
from src.query_processor.query_parser import QueryParser


class QueryProcessor:
    def __init__(self, process_manager, storage_manager):
        self.query_rewriter = QueryRewriter()#storage_manager)
        self.plan_executor = PlanExecutor(execution_scheduler=process_manager)

    async def process(self, raw_query):
        """
        Executes a passed query. Follows the steps:
        - Parse query -> QueryModel
        - Query rewrite
        - Optimize query
        - execute the query using the storage_api
        Args:
            query (str):
        """
        parsed_query = QueryParser.parse_query(raw_query)
        query_plan = self.query_rewriter.rewrite(parsed_query)

        # TODO query = QueryOptimizer.optimize(query)

        # plan executor
        self.plan_executor.execute(query_plan)

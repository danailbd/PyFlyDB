

class PlanExecutor:

    def __init__(self, storage_manager, execution_scheduler):
        self.storage_manager = storage_manager
        self.scheduler = execution_scheduler


    @staticmethod
    def _post_processors():
        '''Return, sort, ...'''
        pass

    async def execute(query, *args):
        # TODO
        """
        Registers operation to the scheduler and waits for it's
            result
        Args:
            query (Query):
            *args:

        Returns:

        """
        name_to_identifiers_map = query.identifiers

        def populate_post_queries(queries, population_data):
            """
            Applies data from results of a query. (populates identifiers)
            N.B. query param is altered

            TODO optimize -- collect needed fields for the result and search only
                those in the db
            Args:
                queries (Query):
                population_data (dict):
            Returns:
                None: It updates the input object
            """
            def update_identifier_data(query, name, value):
                if query.get_identifiers_map().get(key):
                    query.get_identifiers_map()[key]

            for key, value in population_data.iteritems():
                for query in queries:
                    update_identifier_data(query, key, value)
                    query.get_identifiers_map()




        async def execute_sub_query(sub_query):
            """
            Args:
                sub_query:

            Returns:
                dict: Identifier -> List[Node|Edge|...]
            """
            return {}

        sub_queries = query.queries
        cur_query = query.queries[0]
        for idx in range(1, len(sub_queries)):
            results = await execute_sub_query(cur_query)
            # populate following queries (as they might share an identifier)
            populate_post_queries(sub_queries[idx:], results)
            cur_query = sub_queries[idx]


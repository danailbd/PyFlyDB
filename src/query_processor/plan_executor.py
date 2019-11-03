
class PlanExecutor:

    def __init__(self, storage_manager, execution_scheduler):
        self.storage_manager = storage_manager
        self.scheduler = execution_scheduler


    @staticmethod
    def _post_processors():
        '''Return, sort, ...'''
        pass

    def execute(self, query_plan, *args):
        # TODO
        """
        Registers operation to the scheduler and waits for it's
            result
        Args:
            query_plan (QueryPlan):
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

        # TODO execute atomically  ??
        for operation in query_plan.operations:
            future = self.scheduler.submit(operation)

            # on future ready:
            # - populate results
            # - execute next
            # -- rework operation (as op may be split)
            result = future.result()
            populate_post_queries()



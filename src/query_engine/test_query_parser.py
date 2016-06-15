from unittest import TestCase
from src.query_engine.query_parser import *

from src.query_engine.query_ast import *
from src.query_engine.query_ast.models import *
from src.query_engine.query_ast.clauses import *
from src.query_engine.query_ast.expression import *


# TODO [0] test string, [1] result object

class TestQueryParser(TestCase):
    def test_list_split(self):
        self.assertEquals(split_list('a1 b c d', ['a1']),
                          [['a1', 'b c d']])

        self.assertEquals(split_list('a1 b a2 d', ['a1', 'a2']),
                          [['a1', 'b'], ['a2', 'd']])

        self.assertEquals(split_list('a1 b a1 d', ['a1']),
                          [['a1', 'b'], ['a1', 'd']])

        self.assertEquals(split_list('a1 b a1 d', ['a1', 'a2']),
                          [['a1', 'b'], ['a1', 'd']])

        self.assertEquals(split_list('a1 b a2 d a1 b', ['a1', 'a2']),
                          [['a1', 'b'], ['a2', 'd'], ['a1', 'b']])

    def setUp(self):
        self.parser = QueryParser()

    #
    # Test Main Method
    #
    def test_compound(self):
        COMPOUND_TEST_BIG = [(
            'MATCH (person:Person)-[:IS_FRIEND_OF]->(friend),'
            '(friend)-[:LIKES]->(restaurant:Restaurant),'
            '(restaurant)-[:LOCATED_IN]->(loc:Location),'
            '(restaurant)-[:SERVES]->(type:Cuisine)'

            'WHERE person.name = \'Philip\''
            'AND loc.location = \'New York\''
            'AND type.cuisine = \'Sushi\''

            'RETURN restaurant.name, count(*) AS occurrence'
            'ORDER BY occurrence DESC'
            'LIMIT 5'
        )
            # TODO Translate
        ]

        COMPOUND_TEST = [(
            'MATCH (neo:Database {name:"Neo4j"})\n'
            'MATCH (anna:Person {name:"Anna"})\n'
            'CREATE (anna)-[:FRIEND]->(:Person:Expert '
            '{name:"Amanda"})-[:WORKED_WITH]->(neo);'
        ),
            query.Query([
                query.SubQuery([
                    Match(GraphPatternExpression([Node(labels=Label('Database'),
                                                       identifier=Identifier(
                                                           'neo'),
                                                       properties=[
                                                           Property('name',
                                                                    'Neo4j')])])),
                ]),
                query.SubQuery([
                    Match(GraphPatternExpression([Node(labels=Label('Person'),
                                                       identifier=Identifier(
                                                           'anna'),
                                                       properties=[
                                                           Property('name',
                                                                    'Anna')])])),
                ]),
                query.SubQuery([
                    Create(GraphPatternExpression([Edge(label='FRIEND',
                                                        directed=True,
                                                        node_in=Node(
                                                            identifier=Identifier(
                                                                'anna')),
                                                        node_out=Node(
                                                            labels=(
                                                                Label('Person'),
                                                                Label(
                                                                    'Expert')),
                                                            properties=
                                                            Property('name',
                                                                     'Amanda'))),
                                                   Edge(label='WORKED_WITH',
                                                        directed=True,
                                                        node_out=Node(
                                                            identifier=Identifier(
                                                                'neo')),
                                                        node_in=Node(
                                                            labels=(
                                                                Label('Person'),
                                                                Label(
                                                                    'Expert')),
                                                            properties=
                                                            Property('name',
                                                                     'Amanda')))]))
                ])
            ])
        ]
        self.assertEqual(self.parser.parse_query(COMPOUND_TEST[0]),
                         COMPOUND_TEST[1])

    def test_operator_expressions(self):
        pass

    def test_graph_expressions(self):
        SIMPLE_TEST_MATCH_EDGE = [(
            'MATCH (you {name:"You"})-[:FRIEND]->(yourFriends)'
            'RETURN you, yourFriends'
        ),
            query.Query([
                query.SubQuery([
                    Match(GraphPatternExpression([Edge(label='FRIEND',
                                                       directed=True,
                                                       node_in=
                                                       Node(
                                                           identifier=Identifier(
                                                               'you'),
                                                           properties=
                                                           Property('name',
                                                                    'You')),
                                                       node_out=Node(
                                                           labels=Label(
                                                               'yourFriends'),
                                                           properties=
                                                           Property('name',
                                                                    'Amanda')))])),
                    Return(['you', 'yourFriends'])
                ])
            ])
        ]

        SIMPLE_TEST_CREATE_NODE = [(
            'CREATE (you:Person {name:"You"})'
            'RETURN you'
        ),
            query.Query([
                query.SubQuery([
                    Create(GraphPatternExpression([
                        Node(
                            identifier=Identifier('you'),
                            labels=Label('Person'),
                            properties=
                            Property('name',
                                     'You'))
                    ]))
                ])
            ])

        ]

        TEST_MORE_EDGES = [(
            'MATCH (user)-[:PURCHASED]->(product)<-[:PURCHASED]-()-[:PURCHASED]->(otherProduct)'
            'RETURN user.name'
        ),
            (
                query.Query([
                    query.SubQuery([Match(
                        GraphPatternExpression([Edge(label='PURCHASED',
                                                     directed=True,
                                                     node_in=Node(
                                                         identifier=Identifier(
                                                             'user')),
                                                     node_out=Node(
                                                         identifier=Identifier(
                                                             'product'))),
                                                Edge(label='PURCHASED',
                                                     directed=True,
                                                     node_out=Node(
                                                         identifier=Identifier(
                                                             'product')),
                                                     node_in=Node()),
                                                Edge(label='PURCHASED',
                                                     directed=True,
                                                     node_out=Node(
                                                         identifier=Identifier(
                                                             'otherProduct')),
                                                     node_in=Node())
                                                ])),
                        Return('user.name')
                    ])])
            )]

        # TODO Where

        self.assertEqual(self.parser.parse_query(SIMPLE_TEST_CREATE_NODE[0]),
                         SIMPLE_TEST_CREATE_NODE[1])
        self.assertEqual(self.parser.parse_query(SIMPLE_TEST_MATCH_EDGE[0]),
                         SIMPLE_TEST_MATCH_EDGE[1])
        self.assertEqual(self.parser.parse_query(TEST_MORE_EDGES[0]),
                         TEST_MORE_EDGES[1])


def test_exceptions(self):
    pass

from unittest import TestCase
from src.query_engine.query_parser import *

from src.query_engine.query_ast import *
from src.query_engine.query_ast.models import *
from src.query_engine.query_ast.clauses import *
from src.query_engine.query_ast.expression import *


# TODO [0] test string, [1] result object


class TestQueryParser(TestCase):
    def test_parse_graph_expression(self):
        # test with ,
        # test with 1 node
        # test with edge (directed or none)
        # test with node and edge
        # test with more edges
        ## self.assertRaises(InvalidGraphExpressionError,
        ##                   parse_graph_expression, ['()-[]'])
        ## self.assertRaises(EmptyGraphPatternExpressionError,
        ##                   parse_graph_expression, ['()-[]-()'])

        self.assertEquals(parse_graph_expression(['(a)']),
                          GraphPatternExpression((SimpleGraphPatternExpression(
                              (Node(identifier=Identifier('a')))))))
        self.assertEquals(parse_graph_expression(['(a)-[]-(b)']),
                          GraphPatternExpression(
                              (SimpleGraphPatternExpression((Edge(
                                  directed=False,
                                  node_out=Node(identifier=Identifier('b')),
                                  node_in=Node(identifier=Identifier('a'))))))))
        self.assertEquals(parse_graph_expression(['(a)-[:b]-(b)']),
                          GraphPatternExpression(
                              (SimpleGraphPatternExpression((Edge(
                                  label=Label('b'),
                                  directed=False,
                                  node_out=Node(identifier=Identifier('b')),
                                  node_in=Node(identifier=Identifier('a'))))))))
        self.assertEquals(parse_graph_expression(['(a)<-[]-(b)']),
                          GraphPatternExpression(
                              (SimpleGraphPatternExpression((Edge(
                                  directed=True,
                                  node_out=Node(identifier=Identifier('a')),
                                  node_in=Node(identifier=Identifier('b'))))))))

        self.assertEquals(parse_graph_expression(['(a)<-[:b]-()-[:c]->(d)']),
                          GraphPatternExpression((SimpleGraphPatternExpression((
                              Edge(label=Label('b'),
                                   directed=True,
                                   node_out=Node(identifier=Identifier('a')),
                                   node_in=Node()),
                              Edge(label=Label('c'),
                                   directed=True,
                                   node_out=Node(identifier=Identifier('d')),
                                   node_in=Node())
                          )))))

        self.assertEquals(parse_graph_expression(['(a)<-[]-(b)',
                                                  '(c)']),
                          GraphPatternExpression((
                              SimpleGraphPatternExpression((Edge(
                                  directed=True,
                                  node_out=Node(identifier=Identifier('a')),
                                  node_in=Node(identifier=Identifier('b'))))),
                              SimpleGraphPatternExpression(
                                  (Node(identifier=Identifier('c')))))))

    def test_get_properties(self):
        self.assertEquals(get_properties(':lab {a: 1}'),
                          (Property('a', 1),),
                          'Normal, spaced, int')
        self.assertEquals(get_properties(':lab {a: 1.2}'),
                          (Property('a', 1.2),),
                          'Normal, spaced, float')
        self.assertEquals(get_properties(':lab {a: "b"} '),
                          (Property('a', 'b'),),
                          'Normal spaced str')
        self.assertEquals(get_properties(' {a: "b"} '),
                          (Property('a', 'b'),),
                          'Normal; only props')
        self.assertEquals(get_properties(' {a:"b"} '),
                          (Property('a', 'b'),),
                          'Normal; no space')

        self.assertEquals(get_properties(' {a:"b", b:"c"} '),
                          (Property('a', 'b'), Property('b', 'c')),
                          'Multi prop')
        self.assertEquals(get_properties(' {a:"b", b:"c",c:1} '),
                          (Property('a', 'b'), Property('b', 'c'),
                           Property('c', 1)),
                          'Multi prop')
        self.assertEquals(get_properties('a:label '), ())

        self.assertEquals(get_properties(' {a: c.b, b: a.b.d} '),
                          (Property('a', Identifier(name='c', fields=('b',))),
                           Property('b',
                                    Identifier(name='a', fields=('b', 'd')))),
                          'Variable properties')
        self.assertEquals(get_properties(' {a: c.b, b:"c"} '),
                          (Property('a', Identifier(name='c', fields=('b',))),
                           Property('b', 'c')),
                          'Variable properties')
        self.assertEquals(get_properties(' {a: c.b.d.df, b:"c"} '),
                          (Property('a', Identifier(name='c',
                                                    fields=('b', 'd', 'df'))),
                           Property('b', 'c')),
                          'Variable properties more')
        # TODO test EXCEPTIONS

    def test_get_labels(self):
        self.assertEquals(get_labels('a:lab {a: 1}'),
                          (Label('lab'),))
        self.assertEquals(get_labels('a:lab:lab1 {a: 1}'),
                          (Label('lab'), Label('lab1')))
        self.assertEquals(get_labels(':lab:lab1 {a: 1}'),
                          (Label('lab'), Label('lab1')))
        self.assertEquals(get_labels(':lab:lab1'),
                          (Label('lab'), Label('lab1')))
        self.assertEquals(get_labels(':lab:lab1:lab3'),
                          (Label('lab'), Label('lab1'), Label('lab3')))
        self.assertEquals(get_labels('a {}'),
                          ())

        self.assertRaises(InvalidLabelsCountError, get_labels, 'a:b:c',
                          multi=False),
        self.assertEquals(get_labels('a:b', multi=False),
                          Label('b')),
        self.assertIs(get_labels('', multi=False),
                      None),
        self.assertEquals(get_labels('', multi=True),
                          ())

        # TODO test EXCEPTIONS

    def test_get_identifier(self):
        self.assertEquals(get_identifier('a'), Identifier('a'))
        self.assertEquals(get_identifier('a.b'), Identifier(name='a',
                                                            fields=('b',)))
        self.assertEquals(get_identifier('a.bc.cf'),
                          Identifier(name='a', fields=('bc', 'cf')))
        self.assertEquals(get_identifier('a:b '), Identifier('a'))
        self.assertEquals(get_identifier('a.b:b '), Identifier('a', ('b',)))
        self.assertIs(get_identifier(':b'), None)

    def test_parse_edge(self):
        n1 = Node(identifier='a')
        n2 = Node(identifier='b')
        # self.assertRaises(InvalidEdgeLabelError,
        #                   parse_edge, '[]')
        self.assertEquals(parse_edge('-[a]-', n1, n2),
                          Edge(identifier=Identifier('a'),
                               node_in=n1, node_out=n2))
        self.assertEquals(parse_edge('-[a {a: 1}]-', n1, n2),
                          Edge(identifier=Identifier('a'),
                               properties=(Property('a', 1),),
                               node_in=n1, node_out=n2)),
        self.assertEquals(parse_edge('-[a:b {a: 1}]-', n1, n2),
                          Edge(identifier=Identifier('a'),
                               label=Label('b'),
                               node_in=n1, node_out=n2,
                               properties=(Property('a', 1),)))
        self.assertEquals(parse_edge('-[:b {a: 1}]-', n1, n2),
                          Edge(label=Label('b'),
                               node_in=n1, node_out=n2,
                               properties=(Property('a', 1),)))
        self.assertEquals(parse_edge('-[]-', n1, n2),
                          Edge(node_in=n1, node_out=n2))
        # Check direction
        self.assertEquals(parse_edge('-[:b {a: 1}]->', n1, n2),
                          Edge(label=Label('b'),
                               node_in=n1, node_out=n2,
                               directed=True,
                               properties=(Property('a', 1),)))
        self.assertEquals(parse_edge('<-[:b {a: 1}]-', n1, n2),
                          Edge(label=Label('b'),
                               node_in=n2, node_out=n1,
                               directed=True,
                               properties=(Property('a', 1),)))

    ##   self.assertRaises(InvalidEdgeError, parse_edge, '-[]-', n1, n2)

    def test_parse_node(self):
        # TODO clean up tests
        self.assertEquals(parse_node('()'),
                          Node(),
                          'Just a node')

        self.assertEquals(parse_node('(id:lab1)'),
                          Node(identifier=Identifier('id'),
                               labels=Label('lab1')),
                          'Id and label')

        #
        self.assertEquals(parse_node('(id)'),
                          Node(identifier=Identifier('id')),
                          'Just id')

        self.assertEquals(parse_node('(id {a: 1})'),
                          Node(identifier=Identifier('id'),
                               properties=(Property('a', 1),)),
                          'Id and props')

        self.assertEquals(parse_node('(id:lab {a: 1})'),
                          Node(identifier=Identifier('id'),
                               labels=Label('lab'),
                               properties=(Property('a', 1),)),
                          'Id and props')

        self.assertEquals(parse_node('(:lab {a: 1})'),
                          Node(labels=Label('lab'),
                               properties=(Property('a', 1),)),
                          'Label and prop')

        self.assertEquals(parse_node('(:lab:lab1:lab2 {a: 1})'),
                          Node(labels=(Label('lab'), Label('lab1'),
                                       Label('lab2')),
                               properties=(Property('a', 1),)),
                          'Many Labels and prop')

        self.assertEquals(parse_node('(:lab:lab1:lab2)'),
                          Node(labels=(Label('lab'), Label('lab1'),
                                       Label('lab2'))),
                          'Many Labels')

        # PROPERTIES

        self.assertEquals(parse_node('({a: 1})'),
                          Node(properties=(Property('a', 1),)),
                          'Spaced prop'),

        self.assertEquals(parse_node('({a:1})'),
                          Node(properties=(Property('a', 1),)),
                          'No Spaced prop'),

        self.assertEquals(parse_node('({a:1.12})'),
                          Node(properties=(Property('a', 1.12),)),
                          'Float prop'),

        self.assertEquals(parse_node('({a:"abc"})'),
                          Node(properties=(Property('a', "abc"),)),
                          'Prop with string')

        self.assertEquals(parse_node('({a:"abc"})'),
                          Node(properties=(Property('a', 'abc'))),
                          'Prop with string')

        self.assertEquals(parse_node('({a:"abc", b: 1})'),
                          Node(properties=(Property('a', 'abc'),
                                           Property('b', 1))),
                          'Mixed properties')
        #
        # TODO raise Tests
        #

    def test_list_split(self):
        self.assertEquals(split_list('a1 b c d', ['a1']),
                          ['a1', 'b c d'])

        self.assertEquals(split_list('a1 b a2 d', ['a1', 'a2']),
                          ['a1', 'b', 'a2', 'd'])

        self.assertEquals(split_list('a1 b a1 d', ['a1']),
                          ['a1', 'b', 'a1', 'd'])

        self.assertEquals(split_list('a1 b a1 d', ['a1', 'a2']),
                          ['a1', 'b', 'a1', 'd'])

        self.assertEquals(split_list('a1 b a2 d a1 b', ['a1', 'a2']),
                          ['a1', 'b', 'a2', 'd', 'a1', 'b'])

        # Special conditions
        self.assertEquals(split_list('Aa1 Ba a2 d aA1 b', ['aa1', 'a2']),
                          ['aa1', 'Ba', 'a2', 'd', 'aa1', 'b'])

        self.assertEquals(split_list('Aa Baa aA baab', ['aa']),
                          ['aa', 'Baa', 'aa', 'baab'])

    def test_parse_id_expression(self):
        self.fail()

    def setUp(self):
        self.parser = QueryParser()

    # lib
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
                    Match(GraphPatternExpression([SimpleGraphPatternExpression(
                        [Node(labels=Label('Database'),
                              identifier=Identifier(
                                  'neo'),
                              properties=[
                                  Property('name',
                                           'Neo4j')])])])),
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

        # TODO test Expressions with ','hj

    def test_operator_expressions(self):
        self.fail()

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
                    Create(GraphPatternExpression(
                        (SimpleGraphPatternExpression((
                            Node(identifier=Identifier('you'),
                                 labels=Label('Person'),
                                 properties=Property('name', 'You'))
                        ), ),)
                    )),
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
        self.fail()

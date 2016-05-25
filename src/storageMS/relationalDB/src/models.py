from sqlalchemy import Integer, String, ForeignKey, create_engine, Table
from sqlalchemy import Column
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

labels_table = Table('labels', Base.metadata,
                     Column('node_id', Integer, ForeignKey('node.node_id')),
                     Column('label_id', Integer, ForeignKey('label.label_id')))


class Node(Base):
    __tablename__ = 'node'

    node_id = Column(Integer, primary_key=True)
    node_name = Column(String(50))
    properties = relationship("NodeProperty")
    labels = relationship("Label", secondary=labels_table)

    def add_neighbors(self, relationship_type, node):
        Edge(self, node, relationship_type)
        return self

    def higher_neighbors(self, labels=None):
        if not labels:
            labels = self.labels
        return [x.higher_node for x in self.lower_edges if x.labels in labels]

    def lower_neighbors(self, labels=None):
        if not labels:
            labels = self.labels
        return [x.lower_node for x in self.lower_edges if x.label in labels]


class Edge(Base):
    __tablename__ = 'edge'

    edge_id = Column(Integer, primary_key=True)
    label = Column(String)
    child_id = Column(Integer, ForeignKey('node.node_id'))
    parent_id = Column(Integer, ForeignKey('node.node_id'))
    properties = relationship("EdgeProperty")

    lower_node = relationship(Node,
                              primaryjoin=child_id == Node.node_id,
                              backref='lower_edges')

    higher_node = relationship(Node,
                               primaryjoin=parent_id == Node.node_id,
                               backref='higher_edges')

    def __init__(self, n1, n2, label):
        self.higher_node = n1
        self.lower_node = n2
        self.label = label


class EdgeProperty(Base):
    __tablename__ = 'edgeproperty'

    property_id = Column(Integer, primary_key=True)
    key = Column(String(50))
    value = Column(String(50))

    node_id = Column(Integer, ForeignKey('edge.edge_id'))

    def __repr__(self):
        return "{}: {}".format(self.key, self.value)


class NodeProperty(Base):
    __tablename__ = 'nodeproperty'

    property_id = Column(Integer, primary_key=True)
    key = Column(String(50))
    value = Column(String(50))

    node_id = Column(Integer, ForeignKey('node.node_id'))

    def __repr__(self):
        return "{}: {}".format(self.key, self.value)


class Label(Base):
    __tablename__ = 'label'

    label_id = Column(Integer, primary_key=True)
    name = Column(String(50))

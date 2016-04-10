"""

-{}->  // relation syntax
<-{}-

//Rel - relation
(node_1:LABEL) - {Rel} -> (node_2) [ <-{RelI}-() ][-{RelJ}->()] - {Rel2} -> (node_N),
[(node_1) -{Rel3}-> (node_N) [ <-{RelI}-() ] [-{RelJ}->()] ..
// каквото ти позволява въображението :D

WHERE
    node_k.property1 = valuek
    node_j.property2 = valuej          // за всякакви естенствени k,j,i
    ...                                // в разумни граници :D
    Rel_i.propertyi = valuei
    ...

RETURN {node_i.property_i | i = m .. n}

Въпроси

1. Някакъв смислен начин да се репрезентира информацията при RETRUN-а
2. Как да се парсва израза
    -node-овете, и дадените към тях данни да се записват в някаква структура
    подобна на недетерминиран автомат по възможност по която да match-ваме
    части от графа по време на обхождането.
3. -трябва да има някакво умно мачване на node-ове така че да няма изпуснати
   резултати


BFS -> follow existing relations -> if match rememer



"""


class Vertice:
    def __init__(self, unique_id, name, label, properties):
        self.unique_id = unique_id
        self.name = name
        self.label = label
        self.properties = properties


def get_neighbouring_nodes(vertice, **kwargs):
    """
    recieves a vertice and some optional key word arguments
    list of *relationship* types,
    list of *properties*
    list of *labels* a name
    and a *groupby* variable
    which represents the key by which returned nodes should be grouped
    by default - the key is relationship
    """
    pass


def get_nodes(**kwargs):
    """
    recieves a list of *properties*
    list of *labels*
    list of *names*
    and a *groupby* variable
    which represents the key by which returned nodes should be grouped
    by default - the key is relationship
        """
    pass


def get_edges():
    pass


def add_node():
    pass


def add_edge():
    pass


def delete_node():
    pass


def delete_edge():
    pass

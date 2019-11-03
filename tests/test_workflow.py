test_queries = (
    ('MATCH (p:Person { name:"Tom Hanks" })'
     'CREATE (m:Movie { title:"Cloud Atlas",released:2012 })'
     'CREATE (p)-[r:ACTED_IN { roles: [\'Zachry\']}]->(m)'
     'RETURN p,r,m'),
)



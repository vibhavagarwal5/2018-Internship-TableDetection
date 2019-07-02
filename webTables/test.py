import networkx 


G = networkx.Graph()
if(G.nodes == []):
    print("G.nodes == []")

if(list(G.nodes) == []):
    print("list(G.nodes) == []")

if(networkx.is_empty(G)):
    print("networkx.is_empty(G)")

G.add_node(0)
print("node added")
print("-"*30)
if(G.nodes == []):
    print("G.nodes == []")

if(networkx.is_empty(G)):
    print("networkx.is_empty(G)")

if(list(G.nodes) == []):
    print("list(G.nodes) == []")
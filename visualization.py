import networkx as nx
from pyvis.network import Network

# basic
# g = Network(notebook=False)
# nxg = nx.random_tree(20)
# g.from_nx(nxg)
# g.show("example.html")

# layout
# g = Network(notebook=False)
# g.add_nodes([1,2,3],
#             value=[10, 100, 400],
#             title=["I am node 1", "node 2 here", "and im node 3"],
#             x=[21.4, 21.4, 21.4], y=[100.2, 223.54, 32.1],
#             label=["NODE 1", "NODE 2", "NODE 3"],
#             color=["#00ff1e", "#162347", "#dd4b39"])
# g.show("example.html")

# larger
# import pandas as pd
#
# got_net = Network(notebook=False, height="750px", width="100%", bgcolor="#222222", font_color="white")
#
# # set the physics layout of the network
# got_net.barnes_hut()
# got_data = pd.read_csv("https://www.macalester.edu/~abeverid/data/stormofswords.csv")
#
# sources = got_data['Source']
# targets = got_data['Target']
# weights = got_data['Weight']
#
# edge_data = zip(sources, targets, weights)
#
# for e in edge_data:
#     src = e[0]
#     dst = e[1]
#     w = e[2]
#
#     got_net.add_node(src, src, title=src)
#     got_net.add_node(dst, dst, title=dst)
#     got_net.add_edge(src, dst, value=w)
#
# neighbor_map = got_net.get_adj_list()
#
# # add neighbor data to node hover data
# for node in got_net.nodes:
#     node["title"] += " Neighbors:<br>" + "<br>".join(neighbor_map[node["id"]])
#     node["value"] = len(neighbor_map[node["id"]]) # this value attrribute for the node affects node size
#
# got_net.show("example.html")

#
nx_graph = nx.cycle_graph(10)
nx_graph.nodes[1]['title'] = 'Number 1'
nx_graph.nodes[1]['group'] = 1
nx_graph.nodes[3]['title'] = 'I belong to a different group!'
nx_graph.nodes[3]['group'] = 10
nx_graph.add_node(20, size=20, title='couple', group=2)
nx_graph.add_node(21, size=15, title='couple', group=2)
nx_graph.add_edge(20, 21, weight=5)
nx_graph.add_node(25, size=25, label='lonely', title='lonely node', group=3)

nt = Network(notebook=False, height="750px", width="100%")

nt.from_nx(nx_graph)
nt.show("nx.html")
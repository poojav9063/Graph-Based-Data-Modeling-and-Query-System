from graph.build_graph import build_graph

G = build_graph()

print("Total Nodes:", len(G.nodes))
print("Total Edges:", len(G.edges))

# Print sample nodes
for i, node in enumerate(G.nodes(data=True)):
    print(node)
    if i > 5:
        break

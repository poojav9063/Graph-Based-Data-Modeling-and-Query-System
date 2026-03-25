from graph.build_graph import build_graph
from query.query_executor import trace_invoice, find_missing_journals

G = build_graph()

print("\n--- TRACE INVOICE ---")
print(trace_invoice(G, "INV1"))

print("\n--- MISSING JOURNALS ---")
print(find_missing_journals(G)[:5])

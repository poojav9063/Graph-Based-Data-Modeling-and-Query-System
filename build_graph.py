import pandas as pd
import networkx as nx

def build_graph():
    G = nx.DiGraph()

    # Load data
    customers = pd.read_csv("data/business_partners.csv")
    billing = pd.read_csv("data/billing_document_headers.csv")
    items = pd.read_csv("data/billing_document_items.csv")
    journal = pd.read_csv("data/journal_entry_items_accounts_receivable.csv")

    # ----------------------
    # ADD NODES
    # ----------------------

    # Customers
    for _, row in customers.iterrows():
        G.add_node(
            f"customer_{row['business_partner']}",
            type="Customer",
            name=row["name"]
        )

    # Invoices
    for _, row in billing.iterrows():
        G.add_node(
            f"invoice_{row['billing_document']}",
            type="Invoice",
            amount=row.get("amount", 0)
        )

    # Items
    for _, row in items.iterrows():
        G.add_node(
            f"item_{row['billing_document']}_{row['item']}",
            type="Item",
            material=row["material"]
        )

    # Journal Entries
    for _, row in journal.iterrows():
        G.add_node(
            f"journal_{row['accounting_document']}",
            type="Journal"
        )

    # ----------------------
    # ADD EDGES
    # ----------------------

    # Customer → Invoice
    for _, row in billing.iterrows():
        G.add_edge(
            f"customer_{row['sold_to_party']}",
            f"invoice_{row['billing_document']}",
            relation="HAS_INVOICE"
        )

    # Invoice → Item
    for _, row in items.iterrows():
        G.add_edge(
            f"invoice_{row['billing_document']}",
            f"item_{row['billing_document']}_{row['item']}",
            relation="HAS_ITEM"
        )

    # Invoice → Journal
    for _, row in journal.iterrows():
        G.add_edge(
            f"invoice_{row['reference_document']}",
            f"journal_{row['accounting_document']}",
            relation="POSTED_TO"
        )

    return G

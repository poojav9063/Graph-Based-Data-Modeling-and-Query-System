import pandas as pd
import random

# -------------------
# CONFIG
# -------------------
NUM_CUSTOMERS = 10
NUM_INVOICES = 50

# -------------------
# CUSTOMERS
# -------------------
customers = []
for i in range(NUM_CUSTOMERS):
    customers.append({
        "business_partner": f"CUST{i}",
        "name": f"Customer_{i}"
    })

customers_df = pd.DataFrame(customers)

# -------------------
# INVOICES
# -------------------
invoices = []
for i in range(NUM_INVOICES):
    cust = random.choice(customers)
    invoices.append({
        "billing_document": f"INV{i}",
        "sold_to_party": cust["business_partner"],
        "amount": random.randint(1000, 5000)
    })

billing_df = pd.DataFrame(invoices)

# -------------------
# ITEMS
# -------------------
items = []
for inv in invoices:
    num_items = random.randint(1, 3)
    for j in range(num_items):
        items.append({
            "billing_document": inv["billing_document"],
            "item": f"{j}",
            "material": f"PROD{random.randint(1,10)}"
        })

items_df = pd.DataFrame(items)

# -------------------
# JOURNAL ENTRIES
# -------------------
journals = []
for inv in invoices:
    # 80% invoices have journal (realistic)
    if random.random() < 0.8:
        journals.append({
            "accounting_document": f"JRN{inv['billing_document']}",
            "reference_document": inv["billing_document"],
            "amount": inv["amount"]
        })

journal_df = pd.DataFrame(journals)

# -------------------
# SAVE FILES
# -------------------
customers_df.to_csv("business_partners.csv", index=False)
billing_df.to_csv("billing_document_headers.csv", index=False)
items_df.to_csv("billing_document_items.csv", index=False)
journal_df.to_csv("journal_entry_items_accounts_receivable.csv", index=False)

print("✅ Realistic SAP sample data generated!")

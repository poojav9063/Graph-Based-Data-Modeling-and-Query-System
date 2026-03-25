import streamlit as st
from graph.build_graph import build_graph
from query.query_executor import trace_invoice, find_missing_journals
from pyvis.network import Network
import tempfile
from openai import OpenAI
import os
import re

# -------------------------
# LLM SETUP (SAFE)
# -------------------------
client = OpenAI(
    api_key="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",   # ✅ secure
    base_url="https://openrouter.ai/api/v1"
)

# -------------------------
# LLM PARSER
# -------------------------
def llm_parse_query(user_query):
    prompt = f"""
    Convert user query into ONE command ONLY.

    Commands:
    TRACE_INVOICE <invoice_id>
    FIND_MISSING_JOURNALS
    INVALID

    Rules:
    - Output must be EXACT format
    - No explanation

    Examples:
    Find invoice INV1 → TRACE_INVOICE INV1
    Show flow of INV5 → TRACE_INVOICE INV5
    Missing journals → FIND_MISSING_JOURNALS

    Query: {user_query}
    """

    try:
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content.strip()

    except Exception:
        return "ERROR"

# -------------------------
# STREAMLIT UI
# -------------------------
st.set_page_config(layout="wide")
st.title("📊 SAP Order-to-Cash Graph + Chat")

@st.cache_resource
def load_graph():
    return build_graph()

G = load_graph()

col1, col2 = st.columns([3, 1])

# -------------------------
# GRAPH
# -------------------------
with col1:
    st.subheader("📈 Graph View")

    net = Network(height="600px", width="100%", directed=True)

    MAX_NODES = 120
    added_nodes = set()

    for i, (node, data) in enumerate(G.nodes(data=True)):
        if i > MAX_NODES:
            break
        net.add_node(node, label=node, title=str(data))
        added_nodes.add(node)

    for u, v, data in G.edges(data=True):
        if u in added_nodes and v in added_nodes:
            net.add_edge(u, v, label=data.get("relation", ""))

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    net.save_graph(tmp_file.name)

    st.components.v1.html(open(tmp_file.name).read(), height=600)

# -------------------------
# CHAT (SMART HYBRID)
# -------------------------
with col2:
    st.subheader("💬 Chat")

    query = st.text_input("Ask a question")

    if query:
        q = query.lower()

        # -------------------------
        # 🔥 UNIVERSAL INVOICE DETECTION
        # -------------------------
        match = re.search(r"INV\d+", query.upper())
        invoice_id = match.group(0) if match else None

        # -------------------------
        # ⚡ FAST PATH (NO LLM)
        # -------------------------
        if invoice_id:
            result = trace_invoice(G, invoice_id)

            st.success(f"Invoice {invoice_id}")
            st.write("👤 Customer:", result.get("customer"))
            st.write("📦 Items:", result.get("items"))
            st.write("💰 Journals:", result.get("journals"))

        elif any(word in q for word in ["missing", "broken", "incomplete"]):
            result = find_missing_journals(G)

            st.success("Missing journals:")
            st.write(result[:10])

        # -------------------------
        # 🤖 LLM FALLBACK
        # -------------------------
        else:
            with st.spinner("Thinking with LLM... 🤖"):

                parsed = llm_parse_query(query)
                parsed_upper = parsed.upper()

                st.caption(f"LLM Parsed: {parsed}")

                # 🔥 robust parsing
                inv_match = re.search(r"INV\d+", parsed_upper)

                if "TRACE" in parsed_upper and inv_match:
                    invoice_id = inv_match.group(0)
                    result = trace_invoice(G, invoice_id)
                    st.write(result)

                elif "MISSING" in parsed_upper:
                    result = find_missing_journals(G)
                    st.write(result[:10])

                elif "INVALID" in parsed_upper:
                    st.warning("Only dataset-related queries allowed")

                else:
                    st.warning("Could not understand query")

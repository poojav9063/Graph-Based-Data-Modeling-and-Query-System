#  Graph-Based Data Modeling and Query System

##  Overview
This project transforms structured business data (Customers, Invoices, Items, Journals) into a graph-based system and enables natural language querying using an LLM-powered interface.

It helps trace relationships across fragmented datasets and answer business questions interactively.

---
##  Tech Stack

### 🔹 Core

- Python
- 
- Pandas  

### 🔹 Graph & Data Modeling

- NetworkX (graph construction & traversal)  

### 🔹 Visualization

- PyVis (interactive graph rendering)
  
- Streamlit (UI dashboard)  

### 🔹 AI / NLP

- LLM via OpenRouter (Mistral-7B)
   
- OpenAI-compatible API  

### 🔹 System Design

- Hybrid Query Engine (Rule-based + LLM)

  
##  Key Features

-  Graph-based data modeling using NetworkX  
-  Interactive graph visualization using PyVis  
-  Natural language query interface (LLM-powered)  
-  Hybrid query system (rule-based + LLM for speed & flexibility)  
-  Guardrails to restrict queries to dataset domain  
-  Detect incomplete business flows (e.g., missing journal entries)

---

##  Architecture

- **Nodes:** Customers, Invoices, Items, Journals  
- **Edges:** Relationships like HAS_INVOICE, HAS_ITEM, POSTED_TO  
- **Frontend:** Streamlit UI  
- **Backend:** Graph traversal + query execution  
- **LLM Layer:** Converts natural language → structured commands  

---

##  Project Structure

DodgeAI/
│
├── graph/
│ └── build_graph.py
├── query/
│ └── query_executor.py
├── data/
│ ├── dataset.py
│ └── *.csv
├── app.py
├── test_graph.py
└── test_query.py


---

Setup Instructions:

1.Create Environment

bash
python3 -m venv venv
source venv/bin/activate

2.Install Dependencies

pip install pandas networkx streamlit pyvis openai

3.Set API Key

export OPENROUTER_API_KEY="your_api_key"

4.Generate Dataset

python data/dataset.py

5.Run Application

streamlit run app.py

6.Example Queries

Find invoice INV1

What is the flow of INV5?

Which invoices are incomplete?

Show details of INV10

7.Use Cases

Trace end-to-end business transactions

Identify missing or broken workflows

Explore relationships between entities

Query structured data using natural language

8.Key Highlights

Converts tabular ERP data into graph structure

Enables intuitive querying over complex relationships

Combines deterministic logic with LLM flexibility

Provides interactive visualization + chat interface

Output:

<img width="1718" height="567" alt="image" src="https://github.com/user-attachments/assets/24185008-62f5-47fa-a2a8-ac220a1e5515" />

<img width="1670" height="735" alt="image" src="https://github.com/user-attachments/assets/6764e6fe-0da3-4a4d-ac01-b1a68a184995" />



Conclusion

This project demonstrates how structured business data can be transformed into a graph-based system to enable intuitive exploration of complex relationships. By combining graph modeling with a hybrid query approach (rule-based + LLM), the system allows users to interact with data using natural language while ensuring responses remain accurate and data-driven.

The solution highlights the power of graph representations in solving real-world problems such as tracing workflows and identifying incomplete processes, making it a scalable foundation for advanced data analytics systems.


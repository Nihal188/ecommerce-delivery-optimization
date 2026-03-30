import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="E-commerce Delivery Optimization", layout="wide")

st.title("🚚 E-commerce Delivery Optimization System")

st.markdown("""
This app simulates:
- Warehouse to Hub delivery flow
- Route optimization using shortest path
- Vehicle allocation
""")

# -------------------------------
# Sidebar Inputs
# -------------------------------
st.sidebar.header("⚙️ Input Configuration")

num_hubs = st.sidebar.slider("Number of Hubs", 2, 6, 3)

vehicle_capacity = st.sidebar.number_input("Vehicle Capacity (units)", 50, 500, 100)
cost_per_km = st.sidebar.number_input("Cost per km", 1, 20, 5)

# -------------------------------
# Graph Creation
# -------------------------------
G = nx.Graph()

warehouse = "Warehouse"
G.add_node(warehouse)

hubs = [f"Hub_{i}" for i in range(1, num_hubs+1)]

for hub in hubs:
    G.add_node(hub)

# Add distances
import random

edges = []
for hub in hubs:
    distance = random.randint(5, 30)
    G.add_edge(warehouse, hub, weight=distance)
    edges.append((warehouse, hub, distance))

# Inter-hub connections
for i in range(len(hubs)):
    for j in range(i+1, len(hubs)):
        if random.random() > 0.5:
            dist = random.randint(5, 20)
            G.add_edge(hubs[i], hubs[j], weight=dist)
            edges.append((hubs[i], hubs[j], dist))

# -------------------------------
# Demand Input
# -------------------------------
st.subheader("📦 Hub Demand")

demand_data = {}
for hub in hubs:
    demand_data[hub] = st.number_input(f"Demand at {hub}", 10, 300, 50)

# -------------------------------
# Shortest Path Calculation
# -------------------------------
st.subheader("🛣️ Optimized Routes")

routes = {}
total_cost = 0

for hub in hubs:
    path = nx.shortest_path(G, source=warehouse, target=hub, weight='weight')
    distance = nx.shortest_path_length(G, source=warehouse, target=hub, weight='weight')
    
    vehicles_needed = -(-demand_data[hub] // vehicle_capacity)
    cost = distance * cost_per_km * vehicles_needed
    
    routes[hub] = {
        "Path": " → ".join(path),
        "Distance": distance,
        "Vehicles": vehicles_needed,
        "Cost": cost
    }
    
    total_cost += cost

# -------------------------------
# Display Table
# -------------------------------
df = pd.DataFrame(routes).T
st.dataframe(df)

st.success(f"💰 Total Delivery Cost: {total_cost}")

# -------------------------------
# Graph Visualization
# -------------------------------
st.subheader("🗺️ Network Visualization")

pos = nx.spring_layout(G)

plt.figure(figsize=(8,6))
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10)
labels = nx.get_edge_attributes(G,'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

st.pyplot(plt)

# -------------------------------
# Flow Summary
# -------------------------------
st.subheader("📊 Flow Summary")

flow_data = []
for hub in hubs:
    flow_data.append({
        "From": "Warehouse",
        "To": hub,
        "Demand": demand_data[hub],
        "Vehicles": routes[hub]["Vehicles"]
    })

flow_df = pd.DataFrame(flow_data)
st.table(flow_df)

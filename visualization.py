import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

def visualize_decision_tree(scenario, decisions_made):
    """Create and display a visualization of the decision tree and the user's path"""
    if not scenario or not scenario.get("steps"):
        st.warning("No scenario data available for visualization")
        return
    
    # Create a directed graph
    G = nx.DiGraph()
    
    # Add nodes and edges based on scenario steps
    for step in scenario.get("steps", []):
        step_id = step.get("id")
        
        # Skip if no ID
        if not step_id:
            continue
        
        # Add the step as a node
        node_label = step_id.replace("_", " ").title()
        G.add_node(step_id, label=node_label)
        
        # Add edges for decisions
        for decision in step.get("decisions", []):
            next_step = decision.get("next_step")
            if next_step:
                G.add_edge(step_id, next_step, 
                           label=decision.get("text", ""),
                           weight=1.0)
    
    # Create a path through the decisions that were made
    path_edges = []
    current = "start"
    for step in decisions_made:
        path_edges.append((current, step))
        current = step
    
    # Set up the plot
    plt.figure(figsize=(10, 6))
    
    # Create layout
    pos = nx.spring_layout(G, seed=42)
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color="lightblue")
    
    # Draw non-path edges
    all_edges = list(G.edges())
    non_path_edges = [e for e in all_edges if e not in path_edges]
    
    nx.draw_networkx_edges(G, pos, edgelist=non_path_edges, 
                          width=1.0, alpha=0.5, edge_color="gray")
    
    # Draw path edges with different style
    nx.draw_networkx_edges(G, pos, edgelist=path_edges,
                          width=3.0, alpha=1.0, edge_color="blue")
    
    # Draw node labels
    nx.draw_networkx_labels(G, pos, 
                           {n: d.get("label", n) for n, d in G.nodes(data=True)},
                           font_size=10)
    
    # Draw edge labels only for the path
    edge_labels = {(u, v): G[u][v].get("label", "") for u, v in path_edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    
    # Title and styling
    plt.title("Decision Path Through Scenario")
    plt.axis("off")
    
    # Display in Streamlit
    st.pyplot(plt)
    
    # Display biases identified at each step in the path
    if scenario.get("biases"):
        st.markdown("### Biases Along Your Decision Path")
        
        path_steps = ["start"] + decisions_made
        path_biases = []
        
        for bias in scenario.get("biases", []):
            if bias.get("step") in path_steps:
                path_biases.append(bias)
        
        if path_biases:
            bias_df = pd.DataFrame(path_biases)
            st.table(bias_df[["step", "type", "description"]])
        else:
            st.info("No specific biases were identified in your decision path.")

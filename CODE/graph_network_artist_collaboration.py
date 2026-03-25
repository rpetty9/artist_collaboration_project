import pandas as pd
import networkx as nx
from pyvis.network import Network
from pathlib import Path

# Load data
file_path = "assets/artist_collaboration_predictions_by_market.csv"
df = pd.read_csv(file_path)

# Identify market columns
market_cols = [col for col in df.columns if col.startswith("predicted_revenue_")]

# Sort data by predicted streams descending
df_sorted = df.sort_values('predicted_streams', ascending=False)

# Use top 150 rows
top_150 = df_sorted.head(150)

# Create artist scores (total revenue across all collaborations)
artist_score = {}
for _, row in top_150.iterrows():
    rev = row['predicted_revenue_overall']
    for artist in [row["artist_1_name"], row["artist_2_name"]]:
        artist_score[artist] = artist_score.get(artist, 0) + rev

# Calculate min and max revenue for scaling node sizes
min_rev = min(artist_score.values())
max_rev = max(artist_score.values())


# Define a helper function for scaling node sizes
def scale_size(revenue, min_rev, max_rev, min_size=10, max_size=30):
    if max_rev == min_rev:
        return (min_size + max_size) / 2
    return min_size + (revenue - min_rev) / (max_rev - min_rev) * (max_size - min_size)


# Create the graph
G = nx.Graph()


# Function to extract market codes
def get_markets(row):
    """Extract market codes where the artist is present."""
    return [col.split("_")[2] for col in market_cols if row[col] > 2000]


# Add nodes and edges with dynamic node sizes based on revenue
for _, row in top_150.iterrows():
    a1, a2 = row["artist_1_name"], row["artist_2_name"]
    m1 = ",".join(get_markets(row))
    m2 = ",".join(get_markets(row))

    # Add artist 1 node with dynamic size
    if a1 not in G:
        G.add_node(a1,
                   title=f"Artist: {a1}\nEstimated Revenue: ${artist_score[a1]:,.0f}\nMarkets: {m1}",
                   color="#B3A369",
                   font="black",
                   size=scale_size(artist_score[a1], min_rev, max_rev),
                   revenue=artist_score[a1],
                   markets=m1)
    # Add artist 2 node with dynamic size
    if a2 not in G:
        G.add_node(a2,
                   title=f"Artist: {a2}\nEstimated Revenue: ${artist_score[a2]:,.0f}\nMarkets: {m2}",
                   color="#B3A369",
                   font="black",
                   size=scale_size(artist_score[a2], min_rev, max_rev),
                   revenue=artist_score[a2],
                   markets=m2)
    # Add edge with revenue attribute
    G.add_edge(a1, a2,
               value=row['predicted_streams'],
               color="#001f3f",
               title=f"Collaboration: {a1} & {a2}\nEstimated Revenue: ${row['predicted_revenue_overall']:,.0f}",
               edge_revenue=row['predicted_revenue_overall'])

# Update node titles with edge count
for node in G.nodes():
    G.nodes[node]['title'] += f"\nEdges: {G.degree(node)}"
    G.nodes[node]['edge_count'] = G.degree(node)

# Convert to Pyvis Network
net = Network(height="100%", width="100%", notebook=True, bgcolor="white", font_color="black")
net.from_nx(G)

# Set physics options
net.set_options("""
{
  "physics": {
    "enabled": true,
    "stabilization": {
      "enabled": true,
      "iterations": 50
    },
    "barnesHut": {
      "gravitationalConstant": -500,
      "centralGravity": 0.3,
      "springLength": 200,
      "springConstant": 0.2,
      "damping": 0.95,
      "avoidOverlap": 0.1
    },
    "minVelocity": 0.1
  }
}
""")

# Save the initial graph to HTML
output_file = "artist_collaborations.html"
net.save_graph(output_file)

template_path = Path(__file__).resolve().parent / "assets" / "network_shell_template.html"
custom_filter = template_path.read_text(encoding="utf-8")
custom_filter = custom_filter.replace("__MIN_REV__", str(min_rev)).replace("__MAX_REV__", str(max_rev))
custom_filter = custom_filter.replace("{{", "{").replace("}}", "}")

# Inject custom filter into HTML file
with open(output_file, "r", encoding="utf-8") as file:
    html_content = file.read()

html_content = html_content.replace("<head>", "<head>" + custom_filter)

with open(output_file, "w", encoding="utf-8") as file:
    file.write(html_content)

print(f"Interactive graph saved as {output_file}")

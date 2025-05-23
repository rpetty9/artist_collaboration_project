import pandas as pd
import networkx as nx
from pyvis.network import Network

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

# Custom HTML with Edge Count Slider, Filters, and Node Click Toggle Event,
# Plus background image styling for the network container.

custom_filter = f"""
<!-- Include noUiSlider CSS and JS -->
<link href="https://cdnjs.cloudflare.com/ajax/libs/noUiSlider/15.6.1/nouislider.min.css" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/noUiSlider/15.6.1/nouislider.min.js"></script>

<!-- Custom CSS: Set the background of the network container -->
<style>
  /* Set global font color to match the edge color */
  body, h1, h2, h3, h4, h5, h6, p, label, select, option, span, div, a, button {{
    color: #001f3f !important;
  }}

  html, body {{
    height: 100%;
    margin: 0;
    overflow: hidden; /* Prevent scrolling */
  }}

  #mynetwork {{
    position: fixed;
    background-image: url('assets/global_map.png');
    background-repeat: no-repeat;
    background-position: top left;
    background-size: 300px auto;
    left: 350px; /* Align next to leftPanel */
  }}

  #leftPanel {{
    top: 200px;
  }}
</style>

<!-- Define dynamic scaling variables and function -->
<script>
  // These values come from your Python code
  var minRev = {min_rev};
  var maxRev = {max_rev};
  var minSize = 10;
  var maxSize = 50;

  function scaleSize(revenue) {{
      // Avoid division by zero if all revenues are equal
      if (maxRev === minRev) return (minSize + maxSize) / 2;
      return minSize + ((revenue - minRev) / (maxRev - minRev)) * (maxSize - minSize);
  }}
</script>

<body>

  <div style="display: flex; justify-content: space-between; align-items: center; padding: 25px; 
    border-bottom: 2px solid #ccc; background: linear-gradient(135deg, #f0f0f0, #ffffff); 
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);">
    <!-- Larger clickable music icon -->
    <div id="iconContainer" style="flex: 0.8; text-align: left; cursor: pointer;" onclick="resetPage()">
      <img src="assets/music_icon.png" alt="Music Icon" style="height: 150px; width: auto; vertical-align: middle;" 
        title="Reset to Default">
    </div>

    <div id="titleContainer" style="flex: 2; text-align: center;">
      <h1 style="margin: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 38px; 
        color: #001f3f;">
        <span style="font-weight: 600;">Artist Collaboration Network</span> 
      </h1>
      <p style="margin: 5px 0 0; font-size: 18px; color: #555;">Analyzing artist collaboration opportunities and revenue potential</p>
    </div>

    <div id="controlsContainer" style="flex: 1; text-align: right;">
      <div style="margin-bottom: 10px;">
        <label for="marketFilter" style="font-weight: bold; color: #001f3f;">Market:</label>
        <select id="marketFilter" onchange="filterNodes()" style="padding: 6px 12px; font-size: 14px; 
            border-radius: 5px; border: 1px solid #ccc;">
          <option value="all" selected>All Markets</option>
          <option value="au">Australia</option>
          <option value="br">Brazil</option>
          <option value="ca">Canada</option>
          <option value="de">Denmark</option>
          <option value="fr">France</option>
          <option value="gb">Great Britain</option>
          <option value="jp">Japan</option>
          <option value="us">United States</option>
        </select>
      </div>
      <div style="margin-bottom: 15px;">
        <label for="edgeCount" style="font-weight: bold; color: #001f3f;">Show Top</label>
        <select id="edgeCount" onchange="filterNodes()" style="padding: 6px 12px; font-size: 14px; border-radius: 5px; 
            border: 1px solid #ccc;">
          <option value="50">50</option>
          <option value="75">75</option>
          <option value="100">100</option>
          <option value="125">125</option>
          <option value="150" selected>150</option>
        </select>
        <label style="font-weight: bold; color: #001f3f;">Collaborations</label>
      </div>
      <div style="margin-bottom: 10px;">
        <strong style="color: #001f3f;">Total Collaboration Revenue:</strong>
        <span id="totalRevenue" style="font-size: 16px; font-weight: bold;">Loading...</span>
      </div>
      <div style="margin-bottom: 0px;">
        <strong style="color: #001f3f;">Total Artist Revenue:</strong>
        <span id="totalArtistRevenue" style="font-size: 16px; font-weight: bold;">Loading...</span>
      </div>
    </div>
  </div>

  <!-- Left Side Panel for Top 3 Collaborations -->
  <div id="leftPanel" style="
    width: 350px; 
    height: 100vh; 
    position: fixed; 
    left: 0; 
    top: 205px; 
    background: linear-gradient(135deg, #001f3f, #004080); 
    color: white; 
    padding: 20px; 
    font-family: 'Arial', sans-serif; 
    overflow-y: auto;
    box-shadow: 2px 0 10px rgba(0,0,0,0.2);
    ">
    <h2 style="text-align: center; font-size: 20px; margin-bottom: 15px; color: white !important;">Top 3 Collaborations by Revenue</h2>
    <div id="topCollabs"></div>
    <h2 style="text-align: center; font-size: 20px; margin-top: 30px; margin-bottom: 15px; color: white !important;">Top 3 Artists by Revenue</h2>
    <div id="topArtists"></div>
  </div>

  <!-- Network Visualization -->
  <!-- <div id="mynetwork" style="margin-left: 350px; width: calc(100% - 200px); height: 100vh;"></div> -->
  <div id="mynetwork"></div>

</body>



<script>
// Function to calculate and display the total sum revenue of all collaborations
function calculateTotalRevenue() {{
    const allEdges = network.body.data.edges.get();
    const visibleRevenues = allEdges.map(e => e.edge_revenue).filter(rev => rev !== undefined);

    // Sum up all revenue values
    const totalRevenue = visibleRevenues.reduce((sum, rev) => sum + rev, 0);
    document.getElementById("totalRevenue").innerText = `$${{totalRevenue.toLocaleString(undefined, 
        {{minimumFractionDigits: 2, maximumFractionDigits: 2 }})}}`;
}}

// Function to calculate and display the total sum revenue of all artists
function calculateTotalArtistRevenue() {{
    const allNodes = network.body.data.nodes.get();
    const visibleRevenues = allNodes.map(n => n.revenue).filter(rev => rev !== undefined);

    // Sum up all revenue values
    const totalArtistRevenue = visibleRevenues.reduce((sum, rev) => sum + rev, 0);
    document.getElementById("totalArtistRevenue").innerText = `$${{totalArtistRevenue.toLocaleString(undefined, 
        {{minimumFractionDigits: 2, maximumFractionDigits: 2 }})}}`;
}}

// Filtering function for market and edge count
function filterNodes() {{
    const marketFilter = document.getElementById("marketFilter").value;
    const maxEdges = Number(document.getElementById("edgeCount").value);
    const allEdges = network.body.data.edges.get();
    const allNodes = network.body.data.nodes.get();
    let filteredEdges;

    if (marketFilter === "all") {{
        filteredEdges = allEdges;
        document.getElementById("mynetwork").style.backgroundImage = "url('assets/global_map.png')";
    }} else {{
        filteredEdges = allEdges.filter(e => {{
            const fromNode = network.body.data.nodes.get(e.from);
            const toNode = network.body.data.nodes.get(e.to);
            const fromMarkets = fromNode.markets ? fromNode.markets.split(",").map(m => m.trim()) : [];
            const toMarkets = toNode.markets ? toNode.markets.split(",").map(m => m.trim()) : [];
            return fromMarkets.includes(marketFilter) || toMarkets.includes(marketFilter);
        }});
        document.getElementById("mynetwork").style.backgroundImage = `url('assets/${{marketFilter}}_map.png')`;
    }}

    filteredEdges = filteredEdges.slice(0, maxEdges);
    const visibleNodeIDs = new Set(filteredEdges.flatMap(e => [e.from, e.to]));

    allNodes.forEach(n => {{
        network.body.data.nodes.update({{ id: n.id, hidden: !visibleNodeIDs.has(n.id) }});
    }});

    allEdges.forEach(e => {{
        network.body.data.edges.update({{ id: e.id, hidden: !filteredEdges.includes(e) }});
    }});

    const visibleRevenues = filteredEdges.map(e => e.edge_revenue).filter(rev => rev !== undefined);

    // Sum up all collaboration revenue values
    const totalRevenue = visibleRevenues.reduce((sum, rev) => sum + rev, 0);
    document.getElementById("totalRevenue").innerText = `$${{totalRevenue.toLocaleString(undefined, {{minimumFractionDigits: 2, maximumFractionDigits: 2 }})}}`;

    const visibleNodes = allNodes.filter(node => visibleNodeIDs.has(node.id));
    const visibleArtistRevenues = visibleNodes.map(n => n.revenue).filter(rev => rev !== undefined);

    // Sum up all artist revenue values
    const totalArtistRevenue = visibleArtistRevenues.reduce((sum, rev) => sum + rev, 0);
    document.getElementById("totalArtistRevenue").innerText = `$${{totalArtistRevenue.toLocaleString(undefined, {{minimumFractionDigits: 2, maximumFractionDigits: 2 }})}}`;

    updateLeftPanel();
}}

function resetPage() {{
  // Reset filters to their default values
  document.getElementById('marketFilter').value = 'all';
  document.getElementById('edgeCount').value = '150';
  document.getElementById('totalRevenue').textContent = 'Loading...';

  // Clear the selected node
  window.selectedNode = null;

  // Restore original colors and sizes for all nodes using stored sizes
  network.body.data.nodes.get().forEach(node => {{
    network.body.data.nodes.update({{
      id: node.id,
      color: window.originalColors[node.id],
      size: window.originalSizes[node.id]
    }});
  }});

  // Reset the graph to the initial state
  filterNodes();

  // Zoom out to the desired view (e.g., window.initialScale * 0.6)
  network.moveTo({{
    position: window.initialView,
    scale: window.initialScale * 0.6,
    animation: {{ duration: 500, easingFunction: "easeInOutQuad" }}
  }});
}}

// Add a DFS function for full component traversal
function dfs(node, visited, network) {{
    if (visited.has(node)) return;
    visited.add(node);
    const connectedNodes = network.getConnectedNodes(node);
    connectedNodes.forEach(n => dfs(n, visited, network));
}}

window.addEventListener("load", function () {{
    window.selectedNode = null;
    window.originalColors = {{}};
    window.originalSizes = {{}};
    // Store original colors and sizes (using dynamic sizes from revenue)
    network.body.data.nodes.get().forEach(node => {{
        window.originalColors[node.id] = node.color;
        window.originalSizes[node.id] = node.size;
    }});

    // Store the initial view position and scale
    window.initialView = network.getViewPosition();
    window.initialScale = network.getScale();

    // Immediately calculate the revenue range on load
    calculateTotalRevenue();
    calculateTotalArtistRevenue();

    network.on("click", function (params) {{
        if (params.nodes.length > 0) {{
            const clickedNode = params.nodes[0];
            if (window.selectedNode === clickedNode) {{
                // If clicking the same node again, reset the graph and restore the initial view
                window.selectedNode = null;

                // Restore initial view with desired zoom (e.g., window.initialScale * 0.6)
                network.moveTo({{
                  position: window.initialView,
                  scale: window.initialScale * 0.6,
                  animation: {{ duration: 500, easingFunction: "easeInOutQuad" }}
                }});

                // Restore original colors and sizes using stored values
                network.body.data.nodes.get().forEach(node => {{
                    network.body.data.nodes.update({{
                        id: node.id,
                        color: window.originalColors[node.id],
                        size: window.originalSizes[node.id]
                    }});
                }});
                filterNodes();
            }} else {{
                // Highlight the full interconnected chain
                window.selectedNode = clickedNode;
                const visited = new Set();
                const queue = [clickedNode];
                // Breadth-First Search (BFS) to find the entire chain
                while (queue.length > 0) {{
                    const current = queue.shift();
                    if (!visited.has(current)) {{
                        visited.add(current);
                        const neighbors = network.getConnectedNodes(current);
                        queue.push(...neighbors);
                    }}
                }}
                // Display all interconnected nodes
                const visibleNodes = [...visited];
                const allNodes = network.body.data.nodes.get();
                const allEdges = network.body.data.edges.get();
                allNodes.forEach(n => {{
                    network.body.data.nodes.update({{
                        id: n.id,
                        hidden: !visibleNodes.includes(n.id),
                        color: n.id === clickedNode ? "green" : window.originalColors[n.id],
                        size: n.id === clickedNode ? window.originalSizes[n.id] + 5 : window.originalSizes[n.id]
                    }});
                }});
                allEdges.forEach(e => {{
                    const showEdge = visibleNodes.includes(e.from) && visibleNodes.includes(e.to);
                    network.body.data.edges.update({{ id: e.id, hidden: !showEdge }});
                }});
                // Zoom in on the clicked node
                const nodePosition = network.getPositions([clickedNode])[clickedNode];
                network.moveTo({{
                    position: nodePosition,
                    scale: 1.2,
                    animation: {{ duration: 500, easingFunction: "easeInOutQuad" }}
                }});
            }}
        }} else {{
            // Reset the view when clicking outside nodes
            window.selectedNode = null;

            // Restore initial view
            network.moveTo({{
              position: window.initialView,
              scale: window.initialScale,
              animation: {{ duration: 500, easingFunction: "easeInOutQuad" }}
            }});

            // Restore original colors and sizes using stored values
            network.body.data.nodes.get().forEach(node => {{
                network.body.data.nodes.update({{
                    id: node.id,
                    color: window.originalColors[node.id],
                    size: window.originalSizes[node.id]
                }});
            }});
            filterNodes();
        }}
    }});
}});

  // Function to update the Top 3 Collaborations Panel
  function updateLeftPanel() {{
    const marketFilter = document.getElementById("marketFilter").value;
    const allNodes = network.body.data.nodes.get();
    const allEdges = network.body.data.edges.get();

    if (marketFilter === "all") {{
        filteredEdges = allEdges;
    }} else {{
        filteredEdges = allEdges.filter(e => {{
            const fromNode = network.body.data.nodes.get(e.from);
            const toNode = network.body.data.nodes.get(e.to);
            const fromMarkets = fromNode.markets ? fromNode.markets.split(",").map(m => m.trim()) : [];
            const toMarkets = toNode.markets ? toNode.markets.split(",").map(m => m.trim()) : [];
            return fromMarkets.includes(marketFilter) || toMarkets.includes(marketFilter);
        }});
    }}

    // Sort edges and nodes by estimated revenue (descending)
    const sortedEdges = filteredEdges.sort((a, b) => (b.edge_revenue || 0) - (a.edge_revenue || 0)).slice(0, 3);
    const visibleNodeIDs = new Set(filteredEdges.flatMap(e => [e.from, e.to]));
    const sortedNodes = allNodes.filter(node => visibleNodeIDs.has(node.id))
        .sort((a, b) => (b.revenue || 0) - (a.revenue || 0))
        .slice(0, 3);

    // Get the container div
    const topCollabsDiv = document.getElementById("topCollabs");
    topCollabsDiv.innerHTML = ""; // Clear previous content

    // Loop through top 3 collaborations and create HTML elements
    sortedEdges.forEach((edge, index) => {{
      const fromNode = network.body.data.nodes.get(edge.from);
      const toNode = network.body.data.nodes.get(edge.to);
      const revenueFormatted = edge.edge_revenue.toLocaleString("en-US", {{minimumFractionDigits: 2, maximumFractionDigits: 2}});

      const collabHTML = `
        <div style="background: rgba(255,255,255,0.6); border-radius: 10px; padding: 10px; margin-bottom: 10px;">
          <h3 style="font-size: 18px; margin: 2px 0;">#${{index + 1}}: ${{fromNode.label}} & ${{toNode.label}}</h3>
          <p style="font-size: 16px; margin: 2px 0;">Revenue: <strong>$${{revenueFormatted}}</strong></p>
        </div>
      `;

      topCollabsDiv.innerHTML += collabHTML;
    }});

    // Get the container div
    const topArtistsDiv = document.getElementById("topArtists");
    topArtistsDiv.innerHTML = ""; // Clear previous content

    // Loop through top 3 collaborations and create HTML elements
    sortedNodes.forEach((node, index) => {{
      const artistName = node.label;
      const revenueFormatted = node.revenue.toLocaleString("en-US", {{minimumFractionDigits: 2, maximumFractionDigits: 2}});

      const topArtistsHTML = `
        <div style="background: rgba(255,255,255,0.6); border-radius: 10px; padding: 10px; margin-bottom: 10px;">
          <h3 style="font-size: 18px; margin: 2px 0;">#${{index + 1}}: ${{artistName}}</h3>
          <p style="font-size: 16px; margin: 2px 0;">Revenue: <strong>$${{revenueFormatted}}</strong></p>
        </div>
      `;

      topArtistsDiv.innerHTML += topArtistsHTML;
    }});
  }}

  // Call the function when the page loads
  window.addEventListener("load", updateLeftPanel);

  // Call the function whenever filtering occurs
  network.on("afterDrawing", updateLeftPanel);

</script>
"""

# Inject custom filter into HTML file
with open(output_file, "r", encoding="utf-8") as file:
    html_content = file.read()

html_content = html_content.replace("<head>", "<head>" + custom_filter)

with open(output_file, "w", encoding="utf-8") as file:
    file.write(html_content)

print(f"Interactive graph saved as {output_file}")

import subprocess
import sys
import os
import time
import webbrowser

# Relative paths to the visualization scripts
graph_script = os.path.join("..", "graph_network_artist_collaboration.py")
map_script = os.path.join("..", "choropleth_map_artist_collaboration.py")
graph_output = os.path.join("..", "artist_collaborations.html")

# Runs the "graph_network_artist_collaboration.py"
if os.path.exists(graph_script):
    print("Running Graph Network script...")
    subprocess.run(["python", graph_script], check=True)
else:
    print("Graph script not found at:", graph_script)

    sys.exit(1)

# Opens the "artist_collaborations.html"
if os.path.exists(graph_output):
    print("Opening artist_collaborations.html...")
    webbrowser.open(f"file://{os.path.abspath(graph_output)}")
    time.sleep(2)
else:
    print("Graph output not found at:", graph_output)

# Runs the "choropleth_map_artist_collaboration.py"
if os.path.exists(map_script):
    print("Launching Dash choropleth app...")
    subprocess.Popen(["python", map_script])
    time.sleep(5)  # Wait for Dash to start
    webbrowser.open("http://127.0.0.1:8050")
else:
    print("Choropleth map script not found at:", map_script)
    sys.exit(1)

print("\nVisualizations are now running!")

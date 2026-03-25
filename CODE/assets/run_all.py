import subprocess
import sys
import os
import time
import webbrowser

assets_dir = os.path.dirname(os.path.abspath(__file__))
code_dir = os.path.abspath(os.path.join(assets_dir, ".."))

# Relative paths to the visualization scripts
graph_script = os.path.join(code_dir, "graph_network_artist_collaboration.py")
map_script = os.path.join(code_dir, "choropleth_map_artist_collaboration.py")
graph_output = os.path.join(code_dir, "artist_collaborations.html")
predictions_csv = os.path.join(assets_dir, "artist_collaboration_predictions_by_market.csv")
reconstruct_script = os.path.join(assets_dir, "reconstruct_predictions_from_html.py")


def ensure_predictions_csv():
    if os.path.exists(predictions_csv):
        return

    if not os.path.exists(reconstruct_script):
        print("Prediction CSV is missing and no recovery script was found.")
        sys.exit(1)

    print("Prediction CSV missing. Reconstructing it from artist_collaborations.html...")
    subprocess.run(["python", reconstruct_script], check=True, cwd=assets_dir)


ensure_predictions_csv()

# Runs the "graph_network_artist_collaboration.py"
if os.path.exists(graph_script):
    print("Running Graph Network script...")
    subprocess.run(["python", graph_script], check=True, cwd=code_dir)
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
    subprocess.Popen(["python", map_script], cwd=code_dir)
    time.sleep(5)  # Wait for Dash to start
    webbrowser.open("http://127.0.0.1:8050")
else:
    print("Choropleth map script not found at:", map_script)
    sys.exit(1)

print("\nVisualizations are now running!")

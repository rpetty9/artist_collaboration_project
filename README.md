<table>
  <tr>
    <td><img src="CODE/assets/music_icon.png" alt="Music Icon" width="50"></td>
    <td>Artist Collaboration Network</td>
  </tr>
</table>

LIVE DEMO
---------
- Main network visualization: https://rpetty9.github.io/artist_collaboration_project/CODE/artist_collaborations.html
- Market map visualization: https://rpetty9.github.io/artist_collaboration_project/CODE/artist_collaboration_map.html




✨ DESCRIPTION
-----------
This project provides an interactive visualization tool to help music professionals explore potential artist collaborations and market opportunities. It combines network graphs and choropleth maps to visualize predicted revenue across global markets based on past song success, artist features, and market-level chart data.

The tool consists of:
- **`graph_network_artist_collaboration.py`**  
  A network graph visualization showing artists as nodes and their potential collaborations as edges, weighted by predicted revenue.

- **`choropleth_map_artist_collaboration.py`**  
  A choropleth map displaying total revenue potential by country.

- **`generate_collab_predictions.py`**  
  A preprocessing script that analyzes Spotify artist, song, and chart data to generate collaboration predictions.

- **`setup_env.sh`** and **`run_all.py`**  
  A fully automated setup and execution flow that creates a Python virtual environment, installs all dependencies, and launches both visualizations.

Our project is designed to help users discover insights such of high-potential collaborations between connected artists


📥 INSTALLATION
------------
⚠️ **Python Requirement**- Make sure Python **3.10** is installed on your system before running the setup script.  

To set up the project:

1. **Download and unzip the project folder `team043final`**

2. **Open a terminal and navigate into the project’s `assets` folder**
   ```bash
   cd path/to/unzipped/folder/CODE/assets
   ```

3. **Run the setup script, it will create a virtual environment and install dependencies for you**

   ```bash
   bash setup_env.sh
   ```
   (Dependencies installed by bash script: pandas, plotly, dash, networkx, pyvis, numpy, scikit-learn)

5. **Activate the virtual environment**
   ```bash
   source venv/bin/activate
   ```

6. **At this point, you should have all the core files organized in the following structure:**
```
team043final/
└── CODE/
    ├── choropleth_map_artist_collaboration.py              # Choropleth Dash app
    ├── graph_network_artist_collaboration.py               # Pyvis graph visualization
    └── assets/
        ├── setup_env.sh                                    # Environment setup script
        ├── venv/                                           # (Created after running setup_env.sh)
        ├── artist_collaboration_predictions_by_market.csv  # Precomputed prediction data
        ├── run_all.py                                      # Launches both visualizations
        ├── generate_collab_predictions.py                  # Generates prediction CSV
        └── data/
```

🚀 EXECUTION
---------
Once the environment is set up, run the project with:

```bash
python run_all.py
```

This script will:
- Generate artist collaboration predictions
- Create the interactive Pyvis network graph (`artist_collaborations.html`)
- Launch the Dash choropleth map at `http://127.0.0.1:8050`
- Open both in your default web browser automatically

STATIC GITHUB PAGES VERSION
---------
This repository also includes a static, browser-only version that can be hosted with GitHub Pages.

Files:
- `index.html` - landing page for the public site
- `CODE/artist_collaborations.html` - interactive network graph
- `CODE/artist_collaboration_map.html` - static choropleth dashboard

To rebuild the static site assets locally:

```bash
cd CODE/assets
python build_static_site.py
```

If the original prediction CSV is missing, the build script will reconstruct a usable replacement from the saved `artist_collaborations.html` graph artifact.

To activate the environment in future sessions run:
```bash
source venv/bin/activate
```
To exit the virtual environment run:
```
deactivate
```

🎥 DEMO VIDEO
---------------------
- 📺 https://youtu.be/V3jEN4EqOS8


📈 GENERATING COLLABORATION PREDICTIONS (OPTIONAL)
---------------------
This script `generate_collab_predictions.py` generates artist collaboration predictions and exports them as a CSV file.

**Step 1: File Setup**

With the given data files, make sure your working directory looks like this:

```
Your_Project_Folder/
├── generate_collab_predictions.py
├── data/
│   ├── artist_data/
│   │   └── Artists/
│   │       └── spotify_artists_info_complete.csv
│   ├── hit_songs/
│   │   └── Hit Songs/
│   │       └── spotify_hits_dataset_complete.csv
│   └── charts/
│       └── Charts/
│           ├── us/
│           ├── gb/
│           ├── jp/
│           └── ... (all other country folders and year subfolders)
```
**Step 2: How to Run the Script**

<table>
  <thead>
    <tr>
      <th>🍎 macOS</th>
      <th>🐧 Linux</th>
    </tr>
  </thead>
  <tr>
    <td>
      <p>Open Terminal.</p>
      <p>Navigate to the folder where the script is located:</p>
      <pre><code>cd /Users/yourname/Desktop/team043final/CODE/assets</code></pre>
      <p>Run the script:</p>
      <pre><code>python3 generate_collab_predictions.py</code></pre>
    </td>
    <td>
      <p>Open Terminal.</p>
      <p>Navigate to the folder where the script is located:</p>
      <pre><code>cd /home/yourname/team043final/CODE/assets</code></pre>
      <p>Run the script:</p>
      <pre><code>python3 generate_collab_predictions.py</code></pre>
    </td>
  </tr>
</table>

**Script Output**

<p>After successful execution, a file named <code>artist_collaboration_predictions_by_market.csv</code> will be created inside the <code>assets/</code> folder.</p>


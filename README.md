<table>
  <tr>
    <td><img src="https://github.gatech.edu/thackler3/dva-project/blob/master/CODE/assets/music_icon.png" alt="Music Icon" width="50"></td>
    <td>Artist Collaboration Network</td>
  </tr>
</table>




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

4. **Activate the virtual environment**
   ```bash
   source venv/bin/activate
   ```

5. **At this point, you should have all the core files organized in the following structure:**
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
Once the environment is set up and data is in place, run the project with:

```bash
python run_all.py
```

This script will:
- Generate artist collaboration predictions
- Create the interactive Pyvis network graph (`artist_collaborations.html`)
- Launch the Dash choropleth map at `http://127.0.0.1:8050`
- Open both in your default web browser automatically

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
- 📺 https://youtu.be/uzwC4YNMi48


📈 GENERATING COLLABORATION PREDICTIONS (OPTIONAL)
---------------------
This script generates artist collaboration predictions and exports them as a CSV file.

If you'd like to generate your own `artist_collaboration_predictions_by_market.csv`, you can run the following script:

```bash
assets/generate_collab_predictions.py
```

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


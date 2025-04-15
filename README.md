<img src="https://github.gatech.edu/thackler3/dva-project/blob/master/CODE/assets/music_icon.png" alt="Music Icon" width="40"/> Artist Collaboration Network
 DESCRIPTION
-----------
This project provides an interactive visualization tool to help music professionals explore potential artist collaborations and market opportunities. It combines network graphs and choropleth maps to visualize predicted revenue across global markets based on past song success, artist features, and market-level chart data.

The tool consists of:
- A network graph showing artists as nodes and their potential collaborations as edges, weighted by predicted revenue.  
- A choropleth map showing total revenue potential by country.  
- A preprocessing script that builds these predictions from real Spotify datasets.  
- A fully automated setup and execution flow that creates a Python virtual environment, installs all dependencies, and launches both visualizations.

Our project is designed to help users discover insights such of high-potential collaborations between connected artists

📥 INSTALLATION
------------
To set up the project:

1. **Download and unzip the project folder**

2. **Open a terminal and navigate into the project’s `CODE/` folder**
   ```bash
   cd path/to/unzipped/folder/CODE
   ```

3. **Run the setup script to create a virtual environment and install dependencies**
   ```bash
   bash setup_env.sh
   ```

4. **Activate the virtual environment**
   ```bash
   source venv/bin/activate
   ```

5. 📂 **Ensure you have all the required data files in the following structure**
   ```
   assets/data/
     ├──
     ├── 
     └── 
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

To activate the environment in future sessions:
```bash
source venv/bin/activate
```

🎥 DEMO VIDEO
---------------------
📺 https://youtu.be/uzwC4YNMi48

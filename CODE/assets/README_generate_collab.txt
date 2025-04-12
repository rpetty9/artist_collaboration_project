README: How to Run generate_collab_predictions.py

This script generates artist collaboration predictions and exports them as a CSV file.

Step 1: File Setup
With the given data files, make sure your working directory looks like this:


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


Step 2: How to Run the Script

For Windows:
Open the folder where generate_collab_predictions.py is saved. Hold Shift, right-click in an empty area, and select "Open PowerShell window here" or "Open Command Prompt here".

Run:

python generate_collab_predictions.py

For Mac:
Open Terminal.

Navigate to your project folder using cd, like:

cd /Users/yourname/Desktop/Your_Project_Folder

Run:

python3 generate_collab_predictions.py

For Linux:
Open Terminal.

Navigate to the folder:

cd /home/yourname/Your_Project_Folder

Run:

python3 generate_collab_predictions.py

Script Output
After successful execution, a file named 'artist_collaboration_predictions_by_market.csv' will be created in your project folder.
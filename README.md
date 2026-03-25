<table>
  <tr>
    <td><img src="CODE/assets/music_icon.png" alt="Music Icon" width="56"></td>
    <td><h1 style="margin:0;">Artist Collaboration Network</h1></td>
  </tr>
</table>

Interactive music-market visualization project exploring potential artist collaborations and estimated revenue opportunity across global markets.

## Live Demo
- Main network visualization: https://rpetty9.github.io/artist_collaboration_project/CODE/artist_collaborations.html
- Market map visualization: https://rpetty9.github.io/artist_collaboration_project/CODE/artist_collaboration_map.html

## Project Overview
This project began as a data visualization class project focused on discovering high-potential artist collaborations. It combines:

- a network graph that shows artists as nodes and predicted collaborations as revenue-weighted edges
- a market map that shows where projected collaboration revenue is concentrated across countries
- a preprocessing pipeline that was originally designed to generate collaboration predictions from Spotify artist, song, and chart data

The current repository also includes a polished static demo path so the project can be explored directly on GitHub Pages without running a Python server.

## Visualizations
### Network Graph
[`CODE/artist_collaborations.html`](CODE/artist_collaborations.html)

The network view highlights:
- top collaboration opportunities
- top artists by visible revenue
- market-based filtering
- click-to-focus cluster exploration for a selected artist

### Market Map
[`CODE/artist_collaboration_map.html`](CODE/artist_collaboration_map.html)

The map view highlights:
- artist-level revenue totals
- top collaboration cards
- searchable artist selection
- country-level revenue distribution

## Repo Structure
```text
artist_collaboration_project/
├── index.html
├── CODE/
│   ├── artist_collaborations.html
│   ├── artist_collaboration_map.html
│   ├── graph_network_artist_collaboration.py
│   ├── choropleth_map_artist_collaboration.py
│   ├── lib/
│   └── assets/
│       ├── artist_collaboration_predictions_by_market.csv
│       ├── build_static_site.py
│       ├── generate_collab_predictions.py
│       ├── generate_static_choropleth.py
│       ├── reconstruct_predictions_from_html.py
│       ├── run_all.py
│       └── network_shell_template.html
```

## Local Preview
To rebuild the static pages locally:

```bash
cd CODE/assets
python build_static_site.py
```

To preview them in a browser:

```bash
cd ..
cd ..
python -m http.server 8000
```

Then open:
- `http://localhost:8000/CODE/artist_collaborations.html`
- `http://localhost:8000/CODE/artist_collaboration_map.html`

## Python App Workflow
The original Python workflow is still included.

Run from [`CODE/assets`](CODE/assets):

```bash
python run_all.py
```

This will:
- ensure a prediction CSV exists
- generate the network graph HTML
- launch the Dash choropleth app locally

## Data Notes
The original class-project data files were not preserved in this repo. To keep the project runnable, the current static demo uses a reconstructed predictions CSV derived from the saved network graph artifact.

That means:
- the project is fully demoable and explorable
- the static outputs are suitable for presentation and portfolio use
- the reconstructed CSV is not guaranteed to be identical to the original raw model output

If the prediction CSV is missing, the recovery/build scripts can regenerate a usable version from the preserved graph HTML.

## Original Prediction Pipeline
[`CODE/assets/generate_collab_predictions.py`](CODE/assets/generate_collab_predictions.py)

The original script expects a data layout like:

```text
data/
├── artist_data/
│   └── Artists/
│       └── spotify_artists_info_complete.csv
├── hit_songs/
│   └── Hit Songs/
│       └── spotify_hits_dataset_complete.csv
└── charts/
    └── Charts/
        ├── us/
        ├── gb/
        ├── jp/
        └── ...
```

If those raw datasets are recovered in the future, the original model-generation path can be revisited.

## Demo Video
- https://youtu.be/V3jEN4EqOS8

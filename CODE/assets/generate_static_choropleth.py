import json
from pathlib import Path

import pandas as pd


COUNTRY_MAPPING = {
    "predicted_revenue_us": "United States",
    "predicted_revenue_jp": "Japan",
    "predicted_revenue_fr": "France",
    "predicted_revenue_gb": "Great Britain",
    "predicted_revenue_ca": "Canada",
    "predicted_revenue_br": "Brazil",
    "predicted_revenue_de": "Denmark",
    "predicted_revenue_au": "Australia",
}


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Artist Collaboration Earnings by Market</title>
  <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
  <style>
    :root {{
      --navy: #003057;
      --gold: #b3a369;
      --paper: #f3f1eb;
      --ink: #1f2b38;
      --panel: rgba(255, 255, 255, 0.88);
      --line: rgba(0, 48, 87, 0.16);
    }}

    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      font-family: Georgia, "Times New Roman", serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(179, 163, 105, 0.24), transparent 32%),
        linear-gradient(135deg, #f8f5ef 0%, #eef3f8 100%);
      min-height: 100vh;
    }}

    .page {{
      max-width: 1400px;
      margin: 0 auto;
      padding: 32px 20px 40px;
    }}

    .hero {{
      display: grid;
      grid-template-columns: 96px 1fr auto;
      gap: 18px;
      align-items: center;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 24px;
      box-shadow: 0 18px 50px rgba(0, 48, 87, 0.1);
      padding: 22px 24px;
      backdrop-filter: blur(10px);
    }}

    .hero img {{
      width: 96px;
      height: 96px;
      object-fit: contain;
    }}

    .eyebrow {{
      margin: 0 0 6px;
      text-transform: uppercase;
      letter-spacing: 0.16em;
      font-size: 12px;
      color: var(--gold);
      font-weight: 700;
    }}

    .hero h1 {{
      margin: 0;
      font-size: clamp(28px, 4vw, 44px);
      line-height: 1.05;
      color: var(--navy);
    }}

    .hero p {{
      margin: 8px 0 0;
      max-width: 760px;
      font-size: 17px;
      line-height: 1.5;
    }}

    .hero a {{
      justify-self: end;
      text-decoration: none;
      color: white;
      background: var(--navy);
      border-radius: 999px;
      padding: 12px 18px;
      font-weight: 700;
      box-shadow: 0 10px 20px rgba(0, 48, 87, 0.18);
    }}

    .dashboard {{
      display: grid;
      grid-template-columns: minmax(0, 2fr) minmax(320px, 1fr);
      gap: 24px;
      margin-top: 24px;
    }}

    .panel {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 24px;
      box-shadow: 0 18px 50px rgba(0, 48, 87, 0.08);
      backdrop-filter: blur(10px);
    }}

    .map-panel {{
      padding: 24px;
    }}

    .controls {{
      display: grid;
      grid-template-columns: 1fr 260px;
      gap: 16px;
      align-items: end;
      margin-bottom: 18px;
    }}

    .metric-strip {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
    }}

    .metric {{
      padding: 16px 18px;
      border-radius: 18px;
      background: linear-gradient(135deg, rgba(0, 48, 87, 0.95), rgba(24, 83, 128, 0.9));
      color: white;
    }}

    .metric-label {{
      font-size: 12px;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      opacity: 0.78;
    }}

    .metric-value {{
      margin-top: 6px;
      font-size: clamp(20px, 2.4vw, 30px);
      font-weight: 700;
    }}

    .select-wrap label {{
      display: block;
      margin-bottom: 8px;
      font-size: 12px;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--navy);
      font-weight: 700;
    }}

    .select-wrap select {{
      width: 100%;
      border-radius: 16px;
      border: 1px solid var(--line);
      padding: 14px 16px;
      font-size: 16px;
      background: white;
      color: var(--ink);
    }}

    #map {{
      height: 680px;
    }}

    .sidebar {{
      padding: 24px;
    }}

    .sidebar h2 {{
      margin: 0 0 10px;
      color: var(--navy);
      font-size: 22px;
    }}

    .sidebar p {{
      margin: 0 0 18px;
      color: rgba(31, 43, 56, 0.78);
      line-height: 1.5;
    }}

    .collab-list {{
      display: grid;
      gap: 12px;
      max-height: 760px;
      overflow: auto;
      padding-right: 4px;
    }}

    .collab-card {{
      padding: 14px 16px;
      border-radius: 18px;
      background: linear-gradient(180deg, rgba(255, 255, 255, 0.92), rgba(244, 247, 250, 0.92));
      border: 1px solid rgba(0, 48, 87, 0.1);
    }}

    .collab-title {{
      margin: 0;
      font-size: 17px;
      color: var(--navy);
      font-weight: 700;
    }}

    .collab-value {{
      margin: 6px 0 0;
      font-size: 15px;
      color: rgba(31, 43, 56, 0.82);
    }}

    @media (max-width: 980px) {{
      .hero {{
        grid-template-columns: 72px 1fr;
      }}

      .hero a {{
        justify-self: start;
      }}

      .dashboard {{
        grid-template-columns: 1fr;
      }}

      .controls {{
        grid-template-columns: 1fr;
      }}

      #map {{
        height: 520px;
      }}
    }}
  </style>
</head>
<body>
  <div class="page">
    <section class="hero">
      <img src="assets/music_icon.png" alt="Music icon">
      <div>
        <p class="eyebrow">Static Demo</p>
        <h1>Artist Collaboration Earnings by Market</h1>
        <p>Explore the recovered collaboration dataset by artist, compare market-level revenue opportunity, and see the strongest predicted pairings without needing a live Python server.</p>
      </div>
      <a href="artist_collaborations.html">Open Network Graph</a>
    </section>

    <section class="dashboard">
      <div class="panel map-panel">
        <div class="controls">
          <div class="metric-strip">
            <div class="metric">
              <div class="metric-label">Selected Artist Revenue</div>
              <div id="totalRevenue" class="metric-value">$0</div>
            </div>
            <div class="metric">
              <div class="metric-label">Tracked Collaborations</div>
              <div id="collabCount" class="metric-value">0</div>
            </div>
          </div>
          <div class="select-wrap">
            <label for="artistSelect">Choose Artist</label>
            <select id="artistSelect"></select>
          </div>
        </div>
        <div id="map"></div>
      </div>

      <aside class="panel sidebar">
        <h2>Top 10 Potential Collaborations</h2>
        <p>The list updates with the selected artist and shows the highest reconstructed market-level revenue totals from the preserved project output.</p>
        <div id="collaborationList" class="collab-list"></div>
      </aside>
    </section>
  </div>

  <script>
    const dashboardData = {dashboard_data};
    const artistOrder = {artist_order};
    const selectEl = document.getElementById("artistSelect");
    const totalRevenueEl = document.getElementById("totalRevenue");
    const collabCountEl = document.getElementById("collabCount");
    const collabListEl = document.getElementById("collaborationList");

    function currency(value) {{
      return new Intl.NumberFormat("en-US", {{
        style: "currency",
        currency: "USD",
        maximumFractionDigits: 2
      }}).format(value);
    }}

    function buildOptions() {{
      artistOrder.forEach((artist) => {{
        const option = document.createElement("option");
        option.value = artist;
        option.textContent = artist;
        selectEl.appendChild(option);
      }});
    }}

    function renderCollaborations(rows) {{
      collabListEl.innerHTML = "";
      rows.forEach((row) => {{
        const card = document.createElement("article");
        card.className = "collab-card";

        const title = document.createElement("p");
        title.className = "collab-title";
        title.textContent = row.pair;

        const value = document.createElement("p");
        value.className = "collab-value";
        value.textContent = `Revenue: ${{currency(row.revenue)}}`;

        card.appendChild(title);
        card.appendChild(value);
        collabListEl.appendChild(card);
      }});
    }}

    function renderMap(artist) {{
      const view = dashboardData[artist];
      totalRevenueEl.textContent = currency(view.total_revenue);
      collabCountEl.textContent = String(view.collaboration_count);
      renderCollaborations(view.top_collaborations);

      const data = [{{
        type: "choropleth",
        locationmode: "country names",
        locations: view.countries,
        z: view.revenues,
        text: view.countries,
        customdata: view.collaborations,
        colorscale: [
          [0, "#F0F4F8"],
          [1, "#003057"]
        ],
        marker: {{
          line: {{
            color: "rgba(255,255,255,0.65)",
            width: 0.7
          }}
        }},
        colorbar: {{
          title: "Revenue"
        }},
        hovertemplate: "<b>%{{text}}</b><br>Revenue: $%{{z:,.2f}}<br>Collaborations: %{{customdata}}<extra></extra>"
      }}];

      const layout = {{
        margin: {{l: 0, r: 0, t: 0, b: 0}},
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        geo: {{
          projection: {{type: "natural earth"}},
          showframe: false,
          showcoastlines: false,
          bgcolor: "rgba(0,0,0,0)"
        }}
      }};

      Plotly.react("map", data, layout, {{responsive: true, displayModeBar: false}});
    }}

    buildOptions();
    selectEl.value = artistOrder[0];
    renderMap(selectEl.value);
    selectEl.addEventListener("change", () => renderMap(selectEl.value));
  </script>
</body>
</html>
"""


def main() -> None:
    assets_dir = Path(__file__).resolve().parent
    code_dir = assets_dir.parent
    csv_path = assets_dir / "artist_collaboration_predictions_by_market.csv"
    output_path = code_dir / "artist_collaboration_map.html"

    df = pd.read_csv(csv_path)
    market_cols = list(COUNTRY_MAPPING.keys())
    melted_df = df.melt(
        id_vars=["artist_1_name", "artist_2_name"],
        value_vars=market_cols,
        var_name="market",
        value_name="revenue",
    )
    melted_df["country"] = melted_df["market"].map(COUNTRY_MAPPING)

    total_artist_1 = melted_df.groupby("artist_1_name")["revenue"].sum()
    total_artist_2 = melted_df.groupby("artist_2_name")["revenue"].sum()
    total_revenue = total_artist_1.add(total_artist_2, fill_value=0)
    artist_order = total_revenue.sort_values(ascending=False).index.tolist()

    dashboard_data = {}

    for artist in artist_order:
        filtered_df = melted_df[
            (melted_df["artist_1_name"] == artist) | (melted_df["artist_2_name"] == artist)
        ].copy()

        collab_count = filtered_df.groupby("country").size().reset_index(name="collaborations")
        revenue_by_country = filtered_df.groupby("country", as_index=False)["revenue"].sum()
        merged_df = revenue_by_country.merge(collab_count, on="country", how="left")

        top_collaborations = (
            filtered_df.groupby(["artist_1_name", "artist_2_name"], as_index=False)["revenue"]
            .sum()
            .sort_values(by="revenue", ascending=False)
            .head(10)
        )

        dashboard_data[artist] = {
            "countries": merged_df["country"].tolist(),
            "revenues": [round(value, 2) for value in merged_df["revenue"].tolist()],
            "collaborations": merged_df["collaborations"].astype(int).tolist(),
            "total_revenue": round(filtered_df["revenue"].sum(), 2),
            "collaboration_count": int(
                filtered_df[["artist_1_name", "artist_2_name"]].drop_duplicates().shape[0]
            ),
            "top_collaborations": [
                {
                    "pair": f"{row.artist_1_name} & {row.artist_2_name}",
                    "revenue": round(row.revenue, 2),
                }
                for row in top_collaborations.itertuples(index=False)
            ],
        }

    html = HTML_TEMPLATE.format(
        dashboard_data=json.dumps(dashboard_data, ensure_ascii=False),
        artist_order=json.dumps(artist_order, ensure_ascii=False),
    )
    output_path.write_text(html, encoding="utf-8")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()

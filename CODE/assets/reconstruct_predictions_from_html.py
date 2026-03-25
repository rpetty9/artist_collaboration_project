import json
import re
from pathlib import Path

import pandas as pd


MARKET_CODES = ["au", "br", "ca", "de", "fr", "gb", "jp", "us"]


def extract_dataset_block(html_text: str, dataset_name: str) -> list[dict]:
    pattern = rf"{dataset_name}\s*=\s*new vis\.DataSet\((\[.*?\])\);"
    match = re.search(pattern, html_text, re.DOTALL)
    if not match:
        raise ValueError(f"Could not find {dataset_name} dataset in HTML")
    return json.loads(match.group(1))


def choose_edge_markets(node_lookup: dict[str, dict], artist_1: str, artist_2: str) -> list[str]:
    markets_1 = set(node_lookup.get(artist_1, {}).get("markets", "").split(","))
    markets_2 = set(node_lookup.get(artist_2, {}).get("markets", "").split(","))

    clean_1 = {market.strip() for market in markets_1 if market.strip() and market.strip() != "overall"}
    clean_2 = {market.strip() for market in markets_2 if market.strip() and market.strip() != "overall"}

    shared = sorted(clean_1 & clean_2)
    if shared:
        return [market for market in MARKET_CODES if market in shared]

    combined = sorted(clean_1 | clean_2)
    if combined:
        return [market for market in MARKET_CODES if market in combined]

    return MARKET_CODES.copy()


def allocate_market_revenue(total_revenue: float, markets: list[str]) -> dict[str, float]:
    if not markets:
        markets = MARKET_CODES.copy()

    split_value = total_revenue / len(markets)
    allocations = {f"predicted_revenue_{market}": 0.0 for market in MARKET_CODES}
    for market in markets:
        allocations[f"predicted_revenue_{market}"] = split_value
    return allocations


def main() -> None:
    assets_dir = Path(__file__).resolve().parent
    code_dir = assets_dir.parent
    html_path = code_dir / "artist_collaborations.html"
    output_path = assets_dir / "artist_collaboration_predictions_by_market.csv"

    html_text = html_path.read_text(encoding="utf-8")
    nodes = extract_dataset_block(html_text, "nodes")
    edges = extract_dataset_block(html_text, "edges")

    node_lookup = {node["id"]: node for node in nodes}
    reconstructed_rows = []

    for edge in edges:
        artist_1 = edge["from"]
        artist_2 = edge["to"]
        predicted_streams = float(edge.get("value", 0.0))
        predicted_revenue_overall = float(edge.get("edge_revenue", 0.0))

        markets = choose_edge_markets(node_lookup, artist_1, artist_2)
        row = {
            "artist_1_name": artist_1,
            "artist_2_name": artist_2,
            "predicted_streams": predicted_streams,
            "predicted_streams_overall": predicted_streams,
            "predicted_revenue_overall": predicted_revenue_overall,
        }

        revenue_allocations = allocate_market_revenue(predicted_revenue_overall, markets)
        stream_allocations = {
            key.replace("predicted_revenue_", "predicted_streams_"): value / 0.004
            for key, value in revenue_allocations.items()
        }

        row.update(revenue_allocations)
        row.update(stream_allocations)
        reconstructed_rows.append(row)

    df = pd.DataFrame(reconstructed_rows)
    df = df.sort_values("predicted_streams", ascending=False).reset_index(drop=True)
    df.to_csv(output_path, index=False)

    total_edges = len(df)
    total_revenue = df["predicted_revenue_overall"].sum()
    print(f"Reconstructed {total_edges} collaboration rows")
    print(f"Wrote {output_path}")
    print(f"Total overall revenue: ${total_revenue:,.2f}")


if __name__ == "__main__":
    main()

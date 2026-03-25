import os
import subprocess
import sys
from pathlib import Path


def run_step(label: str, command: list[str], cwd: Path) -> None:
    print(f"{label}...")
    subprocess.run(command, check=True, cwd=str(cwd))


def main() -> None:
    assets_dir = Path(__file__).resolve().parent
    code_dir = assets_dir.parent

    predictions_csv = assets_dir / "artist_collaboration_predictions_by_market.csv"
    if not predictions_csv.exists():
        run_step(
            "Reconstructing predictions CSV from saved graph HTML",
            [sys.executable, "reconstruct_predictions_from_html.py"],
            assets_dir,
        )

    run_step(
        "Generating network graph HTML",
        [sys.executable, "graph_network_artist_collaboration.py"],
        code_dir,
    )
    run_step(
        "Generating static choropleth HTML",
        [sys.executable, "generate_static_choropleth.py"],
        assets_dir,
    )
    print("Static site build complete.")


if __name__ == "__main__":
    main()

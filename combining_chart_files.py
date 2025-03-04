import os
import pandas as pd

folder_path = r"C:\Users\rjpet\Desktop\Spotify Project\Updated Files\Charts\all_chart_files"
all_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

combined_df = []

for file in all_files:
    file_path = os.path.join(folder_path, file)

    try:
        df = pd.read_csv(file_path, sep="\t", engine="python", encoding="utf-8")

        # Extract country_code (everything before the first "-")
        country_code = file.split("-")[0]

        # Extract date_range (everything after "features-" and before ".csv")
        date_range = file.split("features-")[-1].replace(".csv", "")

        df["country_code"] = country_code
        df["date_range"] = date_range

        combined_df.append(df)
    except Exception as e:
        print(f"Error reading {file}: {e}")

# Merge all DataFrames
final_df = pd.concat(combined_df, ignore_index=True)

# Save combined file
output_path = os.path.join(folder_path, "charts.csv")
final_df.to_csv(output_path, sep="\t", index=False)

print(f"Combined file saved to: {output_path}")

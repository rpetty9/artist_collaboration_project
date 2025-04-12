import pandas as pd
import numpy as np
from ast import literal_eval
from itertools import combinations
import os
import glob
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# --- File paths ---
songs_path = "data/hit_songs/Hit Songs/spotify_hits_dataset_complete.csv"
artists_path = "data/artist_data/Artists/spotify_artists_info_complete.csv"
charts_folder = "data/charts/Charts"

# --- Load datasets ---
songs_df = pd.read_csv(songs_path, delimiter="\t")
artists_df = pd.read_csv(artists_path, sep="\t")
chart_files = glob.glob(os.path.join(charts_folder, "*", "*", "*.csv"))

charts_data = []

for file in chart_files:
    try:
        filename = os.path.basename(file)
        country_code = filename.split("-")[0]

        date_part = filename.split("-weekly_with_features-")[1].replace(".csv", "")
        start_date_str, end_date_str = date_part.split("--")

        start_date = pd.to_datetime(start_date_str)
        end_date = pd.to_datetime(end_date_str)
        year = start_date.year
        month = start_date.month
        iso_week = start_date.isocalendar()[1]

        df = pd.read_csv(file, sep="\t", quotechar='"')

        df["market"] = country_code
        df["start_date"] = start_date
        df["end_date"] = end_date
        df["year"] = year
        df["month"] = month
        df["iso_week"] = iso_week

        charts_data.append(df)

    except Exception as e:
        print(f"Error loading {file}: {e}")

charts_df = pd.concat(charts_data, ignore_index=True)

# --- Preprocessing: explode artist info ---
songs_df["artist_id"] = songs_df["artist_id"].apply(literal_eval)
songs_df = songs_df.explode("artist_id")

# Merge charts with song-artist pairs to get artist_id per charted song
charts_with_artists_df = charts_df.merge(
    songs_df[["song_id", "artist_id"]],
    on="song_id",
    how="left"
)

# Build artist-market dictionary
artist_market_dict = charts_with_artists_df.groupby("artist_id")["market"].agg(set).to_dict()

# Generate all unique artist pairs
artist_ids = artists_df["artist_id"].unique()
artist_pairs = list(combinations(artist_ids, 2))

# Create DataFrame for artist pairs
artist_pairs_df = pd.DataFrame(artist_pairs, columns=["artist_1_id", "artist_2_id"])

# Attach artist_1 names
artist_pairs_df = artist_pairs_df.merge(
    artists_df[["artist_id", "name"]],
    left_on="artist_1_id",
    right_on="artist_id"
).rename(columns={"name": "artist_1_name"}).drop(columns=["artist_id"])

# Attach artist_2 names
artist_pairs_df = artist_pairs_df.merge(
    artists_df[["artist_id", "name"]],
    left_on="artist_2_id",
    right_on="artist_id"
).rename(columns={"name": "artist_2_name"}).drop(columns=["artist_id"])

# Parse the genres column from string to list
artists_df["genres"] = artists_df["genres"].apply(literal_eval)

# Create helper dictionaries
artist_genre_dict = artists_df.set_index("artist_id")["genres"].to_dict()
artist_popularity_dict = artists_df.set_index("artist_id")["popularity"].to_dict()

# Define filtering function
def filter_artist_pairs(row):
    pop_1 = artist_popularity_dict.get(row["artist_1_id"], 0)
    pop_2 = artist_popularity_dict.get(row["artist_2_id"], 0)
    if abs(pop_1 - pop_2) > 30:
        return False

    genres_1 = set(artist_genre_dict.get(row["artist_1_id"], []))
    genres_2 = set(artist_genre_dict.get(row["artist_2_id"], []))
    if len(genres_1 & genres_2) == 0:
        return False

    markets_1 = artist_market_dict.get(row["artist_1_id"], set())
    markets_2 = artist_market_dict.get(row["artist_2_id"], set())
    if not markets_1 and not markets_2:
        return False

    return True

# Apply filter
filtered_artist_pairs_df = artist_pairs_df[artist_pairs_df.apply(filter_artist_pairs, axis=1)].copy()

# Define function to calculate Jaccard similarity
def jaccard_similarity(row):
    genres_1 = set(artist_genre_dict.get(row["artist_1_id"], []))
    genres_2 = set(artist_genre_dict.get(row["artist_2_id"], []))
    intersection = len(genres_1 & genres_2)
    union = len(genres_1 | genres_2)
    return intersection / union if union != 0 else 0

# Apply to DataFrame
filtered_artist_pairs_df["genre_similarity"] = filtered_artist_pairs_df.apply(jaccard_similarity, axis=1)

# Merge audio features into charts_with_artists_df
audio_features = ["danceability", "energy", "valence", "tempo"]

charts_with_audio = charts_with_artists_df.merge(
    songs_df[["song_id", "artist_id"] + audio_features + ["popularity"]],
    on=["song_id", "artist_id"],
    how="left"
)

# Select top 3 songs per artist by popularity
top_songs_per_artist = charts_with_audio.sort_values(by=["artist_id", "popularity"], ascending=[True, False])
top_songs_per_artist = top_songs_per_artist.groupby("artist_id").head(3)

# Average audio features per artist
artist_feature_avgs = top_songs_per_artist.groupby("artist_id")[audio_features].mean(numeric_only=True).reset_index()

# Merge for artist_1
filtered_artist_pairs_df = filtered_artist_pairs_df.merge(
    artist_feature_avgs,
    left_on="artist_1_id",
    right_on="artist_id",
    how="left"
).rename(columns={
    "danceability": "danceability_1",
    "energy": "energy_1",
    "valence": "valence_1",
    "tempo": "tempo_1"
}).drop(columns=["artist_id"])

# Merge for artist_2
filtered_artist_pairs_df = filtered_artist_pairs_df.merge(
    artist_feature_avgs,
    left_on="artist_2_id",
    right_on="artist_id",
    how="left"
).rename(columns={
    "danceability": "danceability_2",
    "energy": "energy_2",
    "valence": "valence_2",
    "tempo": "tempo_2"
}).drop(columns=["artist_id"])

# Average audio features per pair
def safe_average(a, b):
    if pd.isna(a) and pd.isna(b):
        return np.nan
    elif pd.isna(a):
        return b
    elif pd.isna(b):
        return a
    else:
        return (a + b) / 2

for feature in ["danceability", "energy", "valence", "tempo"]:
    filtered_artist_pairs_df[f"{feature}_avg"] = filtered_artist_pairs_df.apply(
        lambda row: safe_average(row[f"{feature}_1"], row[f"{feature}_2"]), axis=1
    )

# Drop rows with missing averages
filtered_artist_pairs_df.dropna(
    subset=["danceability_avg", "energy_avg", "valence_avg", "tempo_avg"],
    inplace=True
)

# Use charts_with_artists_df which has streams + audio features
training_df = charts_with_artists_df.merge(
    songs_df[["song_id", "danceability", "energy", "valence", "tempo"]],
    on="song_id",
    how="left"
)

# Filter rows with non-null streams and features
training_df = training_df.dropna(subset=["streams", "danceability", "energy", "valence", "tempo"])

# Define X and y
X_train = training_df[["danceability", "energy", "valence", "tempo"]]
y_train = training_df["streams"]

# Train the model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Predict streams for artist collaborations

# Rename columns to match training feature names
X_predict = filtered_artist_pairs_df[["danceability_avg", "energy_avg", "valence_avg", "tempo_avg"]].copy()
X_predict.columns = ["danceability", "energy", "valence", "tempo"]

# Predict and assign
filtered_artist_pairs_df["predicted_streams"] = rf_model.predict(X_predict)

# Create average audio feature profile for each market

# Merge charts data with songs data to get audio features
charts_with_audio = charts_with_artists_df.merge(
    songs_df[["song_id", "danceability", "energy", "valence", "tempo"]],
    on="song_id",
    how="left"
)

# Drop rows with missing audio features
charts_with_audio = charts_with_audio.dropna(subset=["danceability", "energy", "valence", "tempo"])

# Group by market and compute mean audio features
market_audio_profiles = charts_with_audio.groupby("market")[["danceability", "energy", "valence", "tempo"]].mean().reset_index()

# Normalize features and compute cosine similarity (rescaled to avoid negatives)

# Define the features
feature_cols_market = ["danceability", "energy", "valence", "tempo"]
feature_cols_pair = ["danceability_avg", "energy_avg", "valence_avg", "tempo_avg"]

# ✅ Drop 'global' market from audio profiles
market_audio_profiles_filtered = market_audio_profiles[market_audio_profiles["market"] != "global"].copy()

# Scale market features
market_features = market_audio_profiles_filtered[feature_cols_market].copy()
scaler = StandardScaler()
market_scaled = scaler.fit_transform(market_features)

# Prepare and scale artist pair features
pair_features = filtered_artist_pairs_df[feature_cols_pair].copy()
pair_features.columns = feature_cols_market  # Rename to match scaler training
pair_scaled = scaler.transform(pair_features)

# Compute raw cosine similarities
raw_similarity_matrix = cosine_similarity(pair_scaled, market_scaled)

# Rescale cosine similarities to [0, 1]
rescaled_similarities = (raw_similarity_matrix + 1) / 2

# Normalize so each row sums to 1
normalized_similarities = rescaled_similarities / rescaled_similarities.sum(axis=1, keepdims=True)

# Save to a DataFrame for inspection
market_similarity_weights_df = pd.DataFrame(normalized_similarities, columns=market_audio_profiles_filtered["market"].tolist())

# Allocate predicted streams to markets using sonic similarity

# Pull markets in same order as market_audio_profiles
market_list = market_audio_profiles_filtered["market"].tolist()

rows = []

for i, row in filtered_artist_pairs_df.iterrows():
    predicted_streams = row["predicted_streams"]
    similarities = normalized_similarities[i]

    row_dict = row.to_dict()
    row_dict["predicted_streams_overall"] = predicted_streams
    row_dict["predicted_revenue_overall"] = predicted_streams * 0.004  # 👈 Insert here

    for j, market in enumerate(market_list):
        weight = similarities[j]
        market_streams = predicted_streams * weight
        market_revenue = market_streams * 0.004

        row_dict[f"predicted_streams_{market}"] = market_streams
        row_dict[f"predicted_revenue_{market}"] = market_revenue

    rows.append(row_dict)

# Create final output DataFrame
final_df = pd.DataFrame(rows)

# Optional: drop global streams and revenue if present
final_df = final_df.drop(columns=[col for col in final_df.columns if col.endswith("_global")], errors="ignore")

# Step: Export final output to CSV
final_df.to_csv("artist_collaboration_predictions_by_market.csv", index=False)
print("Final output written to artist_collaboration_predictions_by_market.csv")
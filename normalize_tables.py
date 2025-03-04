import os
import pandas as pd
from ast import literal_eval

def load_csv(filename):
    path = r"C:\Users\rjpet\Desktop\Spotify Project\Updated Files\All staging files"
    # Specify tab-delimited files
    return pd.read_csv(os.path.join(path, filename), delimiter='\t')

def process_data():
    # Load files
    artist_df = load_csv("artist.csv")
    artist_network_df = load_csv("artist_network.csv")
    charts_df = load_csv("charts.csv")
    genre_mapping_df = load_csv("genre_mapping.csv")
    genre_network_df = load_csv("genre_network.csv")
    songs_df = load_csv("songs.csv")
    
    print("Starting processing data...")
    
    # Normalize artist-genre relationship
    artist_genre_list = []
    for _, row in artist_df.iterrows():
        artist_id = row['artist_id']
        genres = literal_eval(row['genres']) if isinstance(row['genres'], str) else []
        
        # Skip empty genres
        if genres:
            for genre in genres:
                artist_genre_list.append({'artist_id': artist_id, 'genre': genre})
    
    # Create the DataFrame for artist-genre
    artist_genre_df = pd.DataFrame(artist_genre_list)
    
    # Normalize song-artist relationship (assuming a list in 'songs.csv')
    song_artist_list = []
    for _, row in songs_df.iterrows():
        song_id = row['song_id']
        artists = literal_eval(row['artist_id']) if isinstance(row['artist_id'], str) else []
        for artist in artists:
            song_artist_list.append({'song_id': song_id, 'artist_id': artist})
    song_artist_df = pd.DataFrame(song_artist_list)
    
    # Apply genre mapping
    artist_genre_df = artist_genre_df.merge(genre_mapping_df, left_on='genre', right_on='original_genre', how='left')
    artist_genre_df['mapped_genre'].fillna(artist_genre_df['genre'], inplace=True)
    artist_genre_df = artist_genre_df[['artist_id', 'mapped_genre']].rename(columns={'mapped_genre': 'genre'})
    
    # Normalize artist_network: Artist 1, Artist 2, and count
    artist_network_list = []
    for _, row in artist_network_df.iterrows():
        artist_1 = row['artist_1']
        artist_2 = row['artist_2']
        count = row['count']
        song_ids = literal_eval(row['song_ids']) if isinstance(row['song_ids'], str) else []
        for song_id in song_ids:
            artist_network_list.append({
                'artist_1': artist_1, 'artist_2': artist_2, 'count': count, 'song_id': song_id
            })
    artist_network_expanded_df = pd.DataFrame(artist_network_list)
    
    # Create country dimension table
    country_data = {
        'country_code': ['au', 'br', 'de', 'fr', 'ca', 'gb', 'jp', 'us', 'global'],
        'country_name': ['Australia', 'Brazil', 'Denmark', 'France', 'Canada', 'Great Britain', 'Japan', 'United States', 'Global']
    }
    country_df = pd.DataFrame(country_data)

    # Split the date_range into start_of_week and end_of_week
    charts_df[['start_of_week', 'end_of_week']] = charts_df['date_range'].str.split('--', expand=True)
    charts_df.drop(columns=['date_range'], inplace=True)

    # Save the normalized tables
    output_path = r"C:\Users\rjpet\Desktop\Spotify Project\Updated Files\Normalized Tables"
    os.makedirs(output_path, exist_ok=True)
    
    print(f"Files will be saved to: {output_path}")
    
    # Save all processed DataFrames, including artist.csv
    artist_df.to_csv(os.path.join(output_path, "artist.csv"), index=False)  # Save artist table
    artist_genre_df.to_csv(os.path.join(output_path, "artist_genre.csv"), index=False)
    song_artist_df.to_csv(os.path.join(output_path, "song_artist.csv"), index=False)
    genre_network_df.to_csv(os.path.join(output_path, "genre_network.csv"), index=False)
    artist_network_expanded_df.to_csv(os.path.join(output_path, "artist_network.csv"), index=False)
    charts_df.to_csv(os.path.join(output_path, "charts.csv"), index=False)
    genre_mapping_df.to_csv(os.path.join(output_path, "genre_mapping.csv"), index=False)
    songs_df.to_csv(os.path.join(output_path, "songs.csv"), index=False)  # Saving songs.csv
    country_df.to_csv(os.path.join(output_path, "country.csv"), index=False)  # Save country dimension
    
    print("All files saved successfully.")

# Call the process_data function
print("Calling process_data()...")
process_data()

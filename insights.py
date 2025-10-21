import pandas as pd
import numpy as np
import os  

CSV_PATH = "streaming_history_cleaned.csv"

df = pd.read_csv(CSV_PATH, low_memory=False)

# Identify columns
ms_col = [c for c in df.columns if 'ms_played' in c][0]
track_col = [c for c in df.columns if 'track_name' in c][0]
artist_col = [c for c in df.columns if 'artist_name' in c][0]

# Convert ms_played to numeric
df[ms_col] = pd.to_numeric(df[ms_col], errors='coerce')
df = df.dropna(subset=[ms_col])

# Create a song key
df['song_key'] = df[artist_col].str.strip() + " - " + df[track_col].str.strip()

# Total ms, minutes, hours
song_time = df.groupby('song_key')[ms_col].sum().rename('total_ms_played').reset_index()
song_time['total_minutes_played'] = song_time['total_ms_played'] / 60000
song_time['total_hours_played'] = song_time['total_minutes_played'] / 60

# Count plays
song_count = df.groupby('song_key').size().rename('play_count').reset_index()

# Merge stats
song_stats = song_time.merge(song_count, on='song_key').sort_values('total_ms_played', ascending=False)
song_stats.index = np.arange(1, len(song_stats)+1)

# Top 20
top20_time = song_stats.head(20)

os.makedirs("outputs", exist_ok=True)
song_stats.to_csv("outputs/song_stats.csv", index=False)
top20_time.to_csv("outputs/top20_by_time.csv", index=False)

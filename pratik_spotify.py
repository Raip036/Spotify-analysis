import pandas as pd 
import json 
import os

folder_path = "/Users/pratikrai/Documents/CS/data_projects/Spotify_project/pratik_history"
# List all JSON files in the folder
files = [f for f in os.listdir(folder_path) if f.endswith('.json')]

dfs = []
for file in files:
    file_path = os.path.join(folder_path, file)
    with open(file_path, 'r') as f:
        data = json.load(f)
        temp_df = pd.DataFrame(data)
        dfs.append(temp_df)

df = pd.concat(dfs, ignore_index=True)

print(df.head())
print(f"Loaded {len(df)} rows from {len(files)} files")

df.to_csv("/Users/pratikrai/Documents/CS/data_projects/Spotify_project/spotify_streaming_history.csv", index=False)

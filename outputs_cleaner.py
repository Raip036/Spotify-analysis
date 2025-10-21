import pandas as pd
import csv
import os

# === 1. Path to your input CSV ===
INPUT_CSV = "/Users/pratikrai/Documents/CS/data_projects/Spotify_project/outputs/song_stats.csv"   # change this to your file name
OUTPUT_CSV = "song_stats_cleaned.csv"

# === 2. Load data safely ===
print("🔹 Loading CSV...")
df = pd.read_csv(INPUT_CSV, engine="python", on_bad_lines="skip")

print(f"✅ Loaded {len(df)} rows and {len(df.columns)} columns")

# === 3. Clean text columns ===
# Detect columns that are likely to be text
text_cols = df.select_dtypes(include=["object"]).columns

print(f"🧼 Cleaning text columns: {', '.join(text_cols)}")

for col in text_cols:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(r'[\n\r]', ' ', regex=True)  # remove newlines
        .str.replace('"', '""')                   # escape quotes
        .str.strip()                              # trim spaces
    )

# === 4. Optional: drop fully empty rows ===
df.dropna(how="all", inplace=True)

# === 5. Save as fully quoted CSV (PostgreSQL-safe) ===
print("💾 Saving clean CSV...")
df.to_csv(
    OUTPUT_CSV,
    index=False,
    quoting=csv.QUOTE_ALL,  # ensures all text is wrapped in quotes
    escapechar='\\'
)

print(f"✅ Done! Clean file saved as: {os.path.abspath(OUTPUT_CSV)}")
print("You can now safely import this into PostgreSQL using:")
print(f"COPY your_table FROM '{os.path.abspath(OUTPUT_CSV)}' WITH (FORMAT csv, HEADER true, QUOTE '\"', ESCAPE '\"');")

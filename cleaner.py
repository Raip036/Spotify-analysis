import pandas as pd

df = pd.read_csv("spotify_streaming_history.csv")

df['ts'] = pd.to_datetime(df['ts'], utc=True)

# sort
df = df.sort_values(by='ts').reset_index(drop=True)

# drop rows with missing timestamps
df = df.dropna(subset=['ts'])

df['ts_local'] = df['ts'].dt.tz_convert('Europe/London')

df['date'] = df['ts_local'].dt.date
df['hour'] = df['ts_local'].dt.hour
df['day_of_week'] = df['ts_local'].dt.day_name()

df.drop(columns=['episode_name','episode_show_name','spotify_episode_uri','audiobook_title','audiobook_uri','audiobook_chapter_uri','audiobook_chapter_title','reason_start','reason_end','shuffle','skipped','offline','offline_timestamp','incognito_mode'], inplace=True)

df.to_csv("streaming_history_cleaned.csv", index=False)

print(df.head())
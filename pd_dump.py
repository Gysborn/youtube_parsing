import pandas as pd

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 500)

df = pd.read_json('data/UCrWWcscvUWaqdQJLQQGO6BA.json')
df = df.sort_values(by='likes', ascending=False)
print(df[['likes', 'author', 'video_id', 'text']])

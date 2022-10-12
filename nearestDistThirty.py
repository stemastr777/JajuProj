data = pd.read_json('resultDistAll.json', orient='records').rename(columns={'destination' : 'dst_city','distance(km)' : 'distance'})
res_df = pd.DataFrame(columns=data.columns)

for i in set(data["src_city"].unique()):
    top_30 = data.loc[data["src_city"] == i].sort_values(by='distance').iloc[:30]
    res_df = pd.concat([res_df, top_30], ignore_index=True)

res_df.to_json('resultDistThirty.json', orient='records')
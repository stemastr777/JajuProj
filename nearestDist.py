import pandas as pd
from math import radians, cos, sin, asin, sqrt

# Use Haversine formula
def srcDistance(LaA, LaB, LoA, LoB):
    LoA = radians(LoA)  
    LoB = radians(LoB)  
    LaA= radians(LaA)  
    LaB = radians(LaB)

    dist_lo = LoB - LoA 
    dist_la = LaB - LaA 

    P = sin(dist_la / 2)**2 + cos(LaA) * cos(LaB) * sin(dist_lo / 2)**2  
    Q = 2 * asin(sqrt(P)) 
    earth_rad = 6371
    return(Q * earth_rad) 

# Get the desired data
data = pd.read_csv("daftar-nama-daerah.csv")
used_data = data.drop(['serial','status','parent_nid','type'], axis=1)
used_data = used_data.loc[data["type"] == 2].drop_duplicates(subset="name").reset_index()

# Make SQL statement string
string = []
for p in range(len(used_data)):
    for s in range(len(used_data)):
        if s == p:
            continue
        res = srcDistance(
                used_data.iloc[p,3], 
                used_data.iloc[s,3],
                used_data.iloc[p,4],
                used_data.iloc[s,4]
            )
        string.append(
            "({index}, {source_id}, {dest_id}, {distance})".format( index=len(string), 
                                                                    source_id=used_data["nid"].iloc[p],
                                                                    dest_id=used_data["nid"].iloc[s],
                                                                    distance = "%.2f" % (res)
                                                                )
            )
initialize = "INSERT INTO distance.test2 (`index`,source_id,dest_id,distance) VALUES\n "
result = initialize + ",\n".join(string)
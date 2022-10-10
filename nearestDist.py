import pandas as pd
from math import radians, cos, sin, asin, sqrt


# Latitude and Longitude Converter
def latLongConverter(latlong):
    splitting = latlong[i].split(' ')
    splitting_number = list(map(lambda x: int(x.rstrip(x[-1])), splitting[:2]))
    wind_direction = splitting[2]
    res = splitting_number[0] + (splitting_number[1] / 60)
    if wind_direction == "LS" or wind_direction == "BB":
        res *= -1
    return(round(res,2))


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
raw_data = pd.read_csv("coordinate.csv")
used_data = data.drop_duplicates(subset="city").drop("province", axis=1)
copy_data = used_data.copy()


# Convert latLong
i = 0
for la,lo in zip(used_data["latitude"], used_data["longitude"]):
    copy_data["latitude"].iloc[i] = latLongConverter(la)
    copy_data["longitude"].iloc[i] = latLongConverter(lo)
    i += 1


# Make distance dataframe
new_df = pd.DataFrame(columns=["src_city","destination","distance(km)"])

for p in range(len(copy_data)):
    for s in range(len(copy_data)):
        if s == p:
            continue
        res_dist = srcDistance(
                copy_data.iloc[p,1], 
                copy_data.iloc[s,1],
                copy_data.iloc[p,2],
                copy_data.iloc[s,2]
        )
        new_df.loc[len(new_df)] = [copy_data["city"].iloc[p], copy_data["city"].iloc[s], res_dist]
 

# Make JSON statement string
new_df.to_json('resultDist.json', orient="records")
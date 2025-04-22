import json
from itertools import zip_longest

# Open and read the JSON file
with open('94660.json', 'rb') as file:
    # data = json.load(file)
    data = json.load(file)
    pass

# with open('strings.json') as json_data:
#     d = json.loads(json_data)
#     json_data.close()
#     pprint(d)

# Print the data
# print(data["RouteInfo"]['Name'])
print(len(data["geometry"]))
print(len(data["video_points"]))


por=[ (i['distance'],j['distance']) if j else (i['distance'],0) for i,j in zip_longest(data["geometry"],data["video_points"])]
for i in por:
    # print(i,i[0]-i[1])
    pass


# print(data["geometry"][-1])
# print(data["video_points"][-1])

GP=[i['distance'] for i in data["geometry"]]
VP=[i['distance'] for i in data["video_points"]]

dif=[i for i in GP if i not in VP]

print(dif)
print(len(dif))



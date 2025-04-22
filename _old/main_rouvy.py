#bmystek
from classes import *
import json
import os
import pymsgbox



def make_files(video_file,
                main_video_folder,
                main_gpx_folder,
                GC_routes_files):

    data_startu='2024-10-14T10:00:00Z'

    # pobranie danych, usunięcie ostatniego wiersza i utworzenie słownika z pliku json_file

    data_file_path = f'{GC_routes_files}/{video_file}.json'

    with open(data_file_path, 'rb') as file:
        file = file.read().splitlines()[0]
        data_file = json.loads(file)

    # utworzenie obiektu trasy
    trace = Trace(data_file)

    # do usunięcia:
    def test():


        import matplotlib.pyplot as plt
        import numpy as np

        # x=[i['longitude'] for i in data_file['geometry']]
        # y=[i['latitude'] for i in data_file['geometry']]

        # x=[i['distance'] for i in data_file['geometry']]
        # y=[i['altitude'] for i in data_file['geometry']]

        # x=[i['time'] for i in data_file['video_points']]
        # y=[i['distance'] for i in data_file['video_points']]

        # xpoints = np.array(x)
        # ypoints = np.array(y)
        # plt.plot(xpoints, ypoints,'o')

        # ***************************************

        # x=[i.lon for i in trace.geometry_points]
        # y=[i.lat for i in trace.geometry_points]

        # x=[i.distance for i in trace.geometry_points]
        # y=[i.alt for i in trace.geometry_points]

        # x=[i.point_2.lon for i in trace.geometry_points_lines]
        # y=[i.point_2.lat for i in trace.geometry_points_lines]

        # x=[i.point_2.lon for i in trace.geometry_points_lines]
        # y=[i.point_2.lat for i in trace.geometry_points_lines]

        # x=[i.time for i in trace.video_points]
        # y=[i.distance for i in trace.video_points]

        # x=[i.point_1.time for i in trace.video_points_lines]
        # y=[i.point_1.distance for i in trace.video_points_lines]

        # x=[i.lon for i in trace.GC_points]
        # y=[i.lat for i in trace.GC_points]

        # x=[i.distance for i in trace.GC_points]
        # y=[i.alt for i in trace.GC_points]

        x=[i.time for i in trace.GC_points]
        y=[i.slope for i in trace.GC_points]

        xpoints = np.array(x)
        ypoints = np.array(y)
        plt.plot(xpoints, ypoints)

        # plt.show()



        pass

    # utworzenie plików gpx i GC.json

    gpx_file_path = f'{main_gpx_folder}/{video_file}.gpx'

    trace.make_gpx_file(gpx_file_path, data_startu)

    GC_file_path = f'{main_video_folder}/{video_file}.json'

    trace.make_GC_file(GC_file_path, data_startu)


# dane do wprowadzenia:

main_video_folder = 'D:/_Golden Cheetach/_routes'

main_gpx_folder = 'D:/_Golden Cheetach/_gpx'

GC_routes_files = 'C:/Users/Praca/AppData/LocalLow/VirtualTraining/ROUVY/data/routes/route_geometry_cache'


video_file_list = []
GC_file_list = []
GC_routes_list = []

for path,_,files in os.walk(main_video_folder):
    for file in files:
        if file.endswith(".mp4"):
            video_file_list.append(file.split('_')[0])
        elif file.endswith(".json"):
            GC_file_list.append(file.split('_')[0])

for path,_,files in os.walk(GC_routes_files):
    for file in files:
        if file != "_cache.json":
            GC_routes_list.append(file.split('.')[0])


utworzone_pliki= []
brak_danych = []

for video in video_file_list:
    if video in GC_file_list:
        print(video + ' ok')
        continue
    elif video in GC_routes_list:
        make_files(video,
                   main_video_folder,
                   main_gpx_folder,
                   GC_routes_files)
        print(video + ' utworzono plik GC.json')
        utworzone_pliki.append(video)
    else:
        print(f'Brak pliku {video} w katalogu Rouvy')
        brak_danych.append(video)

pymsgbox.alert(text='Utworzone pliki:   {}\nBrak danych:   {}'.format('; '.join(utworzone_pliki),'; '.join(brak_danych)), title='{}'.format('GC'), button='OK')

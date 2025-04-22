import json
import os
import pymsgbox
from bs4 import BeautifulSoup
import requests
import random


#tworzu pliki gpx z wszystkich plików json w katalogu

def main():

    def make_gpx(file_path):

        # pobranie danych z pliku json
        with open(file_path, 'rb') as file:
            data = json.load(file)
            pass

        # dane do wprowadzenia:

        data_startu='2024-12-14T10:00:{:02d}Z'.format(random.randint(0,59))
        print(data_startu)

        #utworzenie instancji punktów

        class gpx_point:
            def __init__(self,lat,lon,dis,alt,vid_time):
                self.lat=lat
                self.lon=lon
                self.dis=dis
                self.alt=alt
                self.vid_time=vid_time
            
            def make_txt(self,time):

                return '''		<trkpt lat="{}" lon="{}"><ele>{}</ele><time>{}</time></trkpt>'''.format(self.lat,self.lon,self.alt,time)
            
        gpx_points=[]

        print(file_path)

        print(len(data['geometry']))

        print(len(data['video_points']))

        for i,j in enumerate(data['geometry']):
            # print(f"{i}: {int(data['video_points'][i+1]['time'])-int(data['video_points'][i]['time'])} {int(data['geometry'][i+1]['distance'])-int(data['geometry'][i]['distance'])} : {int(data['geometry'][i]['distance'])}")
            try:
                gpx_points.append(gpx_point(j['latitude'],
                                        j['longitude'],
                                        j['distance'],
                                        j['altitude'],
                                        data['video_points'][i]['time']
                                        ))
            except:
                print('xxxx')
        pass
        # print(data['RouteInfo']['Name'])
        # print(data['RouteInfo'])


        # pobranie danych ze strony
        # do poprawy - nie działa bo wymagane jest logowanie
                # url = "https://riders.rouvy.com/new-route/{}".format(file_path[-10:-5])
                # response = requests.get(url)
                # html_content = response.content
                # soup = BeautifulSoup(html_content, "html.parser")
                # print(soup.text)

                # elements = soup.find('h1', class_='hero-heading pb-6 text-global-white')
                
                # for element in elements:
                #     route_name = element.find(class_="grid grid-cols-1 lg:grid-cols-2").get_text()
                
                # pass


        # tworzenie pliku gpx

        import datetime

        start_time=datetime.datetime.fromisoformat(data_startu)

        nazwa_pliku_gpx=file_path.rstrip('json')+'gpx'

        plik = open(nazwa_pliku_gpx, 'w')

        route_name="{}".format(file_path[-10:-5])
        print(route_name)

        opening='''<?xml version="1.0" encoding="UTF-8"?>
        <gpx version="1.0">
            <name>{}</name>
            <wpt lat="{}" lon="{}">
                <ele>{}</ele>
                <name>{}</name>
            </wpt>
            <trk><name>{}</name><number>1</number><trkseg>\n'''.format(route_name,
                                                                        gpx_points[0].lat,
                                                                        gpx_points[0].lon,
                                                                        gpx_points[0].alt,
                                                                        route_name,
                                                                        route_name)

        plik.write(opening)

        for i in gpx_points:
            t=start_time+datetime.timedelta(0,float(i.vid_time))
            s=t.strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:-4]
            plik.write(i.make_txt(s)+'\n')

        ending='''	</trkseg></trk>
        </gpx>'''

        plik.write(ending)

        plik.close()

    input_dir = os.getcwd()

    cnt=0
    error_files=''

    for i,_,k in os.walk(input_dir):
        for l in k:
            if l.endswith('.json'):
                    try:
                        file_path='{}\\{}'.format(i,l)
                        make_gpx(file_path)
                        cnt+=1
                    except:
                        error_files+=l.split('''\\''')[-1]+'\n'
                    


    pymsgbox.alert(text=f'Utworzone pliki .gpx :{cnt}szt.\nBłędne pliki:\n'+error_files)

if __name__ == "__main__":
    main()

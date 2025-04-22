class GpxPoint:
    def __init__(self, count, lat, lon, distance, alt, time = 0):
        self.count = count
        self.lat = lat
        self.lon = lon
        self.distance = distance # [m]
        self.alt = alt
        self.time = time

        # dane do plików GC
        self.speed = 0 # [m/s]
        self.slope = 0

    def make_gpx_txt(self,time):

        return '''		<trkpt lat="{}" lon="{}"><ele>{}</ele><time>{}</time></trkpt>'''.format(self.lat,
                                                                                            self.lon,
                                                                                            self.alt,
                                                                                            time)
    def make_GC_txt(self):

        return '''			{} "SECS":{}, "KM":{}, "KPH":{}, "ALT":{}, "LAT":{}, "LON":{}, "SLOPE":{} {},'''.format('{',
                                                                                                                self.time,
                                                                                                                round(self.distance/1000,7),
                                                                                                                round(3.6 * self.speed,4),
                                                                                                                round(self.alt,4),
                                                                                                                round(self.lat,9),
                                                                                                                round(self.lon,9),
                                                                                                                round(self.slope,6),
                                                                                                                '}')


    def make_GC_json_txt(self):
        pass


class VideoPoint:
    def __init__(self, count, distance, time):
        self.count = count
        self.distance = distance
        self.time = time


class GeometryPointsLine:
    def __init__(self, count, point_1, point_2):
        self.count = count
        self.point_1 = point_1
        self.point_2 = point_2
        self.start = point_1.distance
        self.end = point_2.distance
        self.length = point_2.distance - point_1.distance
        self.time = point_2.time - point_1.time
    
    def generate_new_gpx_point(self, time):
        if time == 0: return self.point_1
        # generuje nowy punkt dla zadanego czasu
        # ustalenie proporcji
        proportion = (time - self.point_1.time)/self.time

        new_distance = self.start + (self.length * proportion)
        new_alt = self.point_1.alt + ((self.point_2.alt - self.point_1.alt) * proportion)
        new_lat = self.point_1.lat + ((self.point_2.lat - self.point_1.lat) * proportion)
        new_lon = self.point_1.lon + ((self.point_2.lon - self.point_1.lon) * proportion)

        return GpxPoint(int(time), new_lat, new_lon, new_distance, new_alt, time)


class VideoPointsLine:
    def __init__(self, count, point_1, point_2):
        self.count = count
        self.point_1 = point_1
        self.point_2 = point_2
        self.start = point_1.distance
        self.end = point_2.distance
        self.length = point_2.distance - point_1.distance
        self.time = point_2.time - point_1.time

    def calc_time(self, point):
        tmp =point.count
        a = self.point_1.time
        b= point.distance
        c= self.start
        d = self.length
        e = self.time
        f = self.point_1.time + (((point.distance-self.start)/self.length)*self.time)
        return self.point_1.time + (((point.distance-self.start)/self.length)*self.time)
    

class GCPointsLine:
    def __init__(self, count, point_1, point_2):
        self.count = count
        self.point_1 = point_1
        self.point_2 = point_2
        self.length = point_2.distance - point_1.distance
        self.slope = 100 * (point_2.alt - point_1.alt)/(point_2.distance - point_1.distance)
        self.time = point_2.time - point_1.time
        self.speed = self.length/self.time

        self.point_2.slope = self.slope
        self.point_2.speed = self.speed


class Trace:
    def __init__(self, data_file):
        self.data_file = data_file

        self.geometry_points = []
        self.video_points = []
        self.GC_points = []

        self.geometry_points_lines = []
        self.video_points_lines = []
        self.GC_points_lines = []

        
        
        self.create_geometry_points()
        self.create_video_points()
        self.create_video_points_lines()
        self.set_geometry_points_times()
        self.create_geometry_points_lines()

        self.create_GC_points()
        self.create_GC_points_lines()

    def create_geometry_points(self):
        for count, data_point in enumerate(sorted(self.data_file['geometry'], key=lambda n: n['distance'])):
            self.geometry_points.append(GpxPoint(count,
                                                  data_point['latitude'],
                                                  data_point['longitude'],
                                                  data_point['distance'],
                                                  data_point['altitude']))

    def create_video_points(self):
        for count, data_point in enumerate(sorted(self.data_file['video_points'], key=lambda n: n['distance'])):
            self.video_points.append(VideoPoint(count,
                                                data_point['distance'],
                                                data_point['time']))

    def create_video_points_lines(self):
        count = 0
        for point_1, point_2 in zip(self.video_points, self.video_points[1:]):
            if point_1.time != point_2.time:
                self.video_points_lines.append(
                    VideoPointsLine(count, point_1, point_2))
                count += 1

    def set_geometry_points_times(self):
        for point in self.geometry_points:
            for video_line in self.video_points_lines:
                if video_line.start <= point.distance < video_line.end:
                    vid_time = video_line.calc_time(point)
                    point.time = vid_time
                    break
                vid_time = video_line.calc_time(point)
                point.time = vid_time

    def create_geometry_points_lines(self):
        count = 0
        for point_1, point_2 in zip(self.geometry_points, self.geometry_points[1:]):
            self.geometry_points_lines.append(
                GeometryPointsLine(count, point_1, point_2))
            count += 1

    def create_GC_points(self):
        for time in range(int(self.geometry_points[-1].time)+1):
            for geometry_points_line in self.geometry_points_lines:
                if geometry_points_line.point_1.time <= time < geometry_points_line.point_2.time:
                    self.GC_points.append(geometry_points_line.generate_new_gpx_point(time))
                    break

    def create_GC_points_lines(self):
        count = 0
        for point_1, point_2 in zip(self.GC_points, self.GC_points[1:]):
            self.GC_points_lines.append(
                GCPointsLine(count, point_1, point_2))
            count += 1

    def make_gpx_file(self, gpx_file_path, start_time):
        import datetime
        start_time=datetime.datetime.fromisoformat(start_time)

        file = open(gpx_file_path, 'w')

        opening='''<?xml version="1.0" encoding="UTF-8"?>
        <gpx version="1.0">
            <name>Example gpx</name>
            <wpt lat="{}" lon="{}">
                <ele>{}</ele>
                <name>{}</name>
            </wpt>
            <trk><name>Example gpx</name><number>1</number><trkseg>\n'''.format(self.geometry_points[0].lat,
                                                                                self.geometry_points[0].lon,
                                                                                self.geometry_points[0].alt,
                                                                                gpx_file_path.split('/')[-1])

        file.write(opening)

        for i in self.geometry_points:
            t=start_time+datetime.timedelta(0,float(i.time))
            s=t.strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:-4]
            file.write(i.make_gpx_txt(s)+'\n')

        ending='''	</trkseg></trk>
        </gpx>'''

        file.write(ending)

        file.close()

    def make_GC_file(self, GC_file_path, start_time):
        import datetime
        start_time=datetime.datetime.fromisoformat(start_time)

        file = open(GC_file_path, 'w')

        opening='''{
	"RIDE":{
		"STARTTIME":"2024\\/10\\/14 08:00:00 UTC ",
		"RECINTSECS":1,
		"DEVICETYPE":"unknown ",
		"IDENTIFIER":" ",
		"TAGS":{
			"Athlete":"mgld ",
			"Data":"TDS----AGL----- ",
			"Device":"unknown ",
			"File Format":" ",
			"Filename":"2024_10_14_10_00_00.json ",
			"Month":"pazdziernik ",
			"Source Filename":"78756_2024_10_14_10_00_00.gpx ",
			"Weekday":"pon. ",
			"Year":"2024 "
		},
		"SAMPLES":[\n'''

        file.write(opening)

        for i in self.GC_points[:-1]:
            file.write(i.make_GC_txt()+'\n')

        file.write(self.GC_points[-1].make_GC_txt()[:-1]+'\n')

        ending='''		]
	}
}
'''

        file.write(ending)

        file.close()
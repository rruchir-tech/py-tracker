from xml.dom import minidom
from datetime import datetime

class GeoFenceCheck:

    """
    Read coordinates from a KML file and return them as a list of tuples.
    """
    def read_kml_file(self,file_path):
        coordinates = []
        with open(file_path, 'r') as f:
            content = f.read()
            dom = minidom.parseString(content)
            placemarks = dom.getElementsByTagName('Placemark')
            for placemark in placemarks:
                name = placemark.getElementsByTagName('name')[0].childNodes[0].nodeValue
                polygon = placemark.getElementsByTagName('Polygon')
                if polygon:
                    outer_boundary = polygon[0].getElementsByTagName('outerBoundaryIs')
                    if outer_boundary:
                        coordinates_str = outer_boundary[0].getElementsByTagName('coordinates')[0].childNodes[0].data
                        coordinates_list = coordinates_str.strip().split()
                        for coord in coordinates_list:
                            lon, lat, _ = coord.split(',')
                            coordinates.append((float(lon), float(lat)))
        return (name, coordinates)


    """Using odd-even rule check if the point is on the path, corner, or boundary of the polygon
    Args:
      long -- longitude value.
      lat -- latitude value
      polygon coordinates -- a list of tuples [(x, y), (x, y), ...]
    Returns:
      True if the point is in the path or is a corner or on the boundary"""
    def is_point_inside_polygon(self,long: int, lat: int, polygon_coordinates: list[tuple[int, int]]) -> bool:
        is_inside = False
        for i in range(len(polygon_coordinates)):
            ax, ay = polygon_coordinates[i]
            bx, by = polygon_coordinates[i - 1]
            
            if (long == ax) and (lat == ay):
                # check if point is a corner
                return True
            if (ay > lat) != (by > lat):
                # check if point is between the coordinates
                slope = (long - ax) * (by - ay) - (bx - ax) * (lat - ay)
                if slope == 0:
                    # point is on boundary
                    return True
                if (slope < 0) != (by < ay):
                    is_inside = not is_inside
        return is_inside

    """check if the point is inside the geo fence
    Args:
      config - object with attributes
          long -- longitude value.
          lat -- latitude value
          kml_file_path -- kml file path downloaded from google map
    Returns:
      True if the point is inside the geo fence"""
    def check_point_in_fence(self,config):
        geofence_name, polygon_coordinates = self.read_kml_file(config['kml_file_path'])
        print('[%s] Geo Fence: %s, Coordinates : %s' % (str(datetime.now()), geofence_name, str(polygon_coordinates)))
    
        is_inside = self.is_point_inside_polygon(config['long'], config['lat'], polygon_coordinates)
        if is_inside:
            print(str(config['long']) + "," + str(config['lat']) + " is inside the geo fence.")
        else:
            print(str(config['long']) + "," + str(config['lat']) + " is outside the geo fence.")
        return (geofence_name, is_inside)

   
    

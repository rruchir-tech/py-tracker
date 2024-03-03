from xml.dom import minidom
from shapely.geometry import Point, Polygon

def read_kml(file_path):
    """
    Read coordinates from a KML file and return them as a list of tuples.
    """
    coordinates = []
    with open(file_path, 'r') as f:
        content = f.read()
        dom = minidom.parseString(content)
        placemarks = dom.getElementsByTagName('Placemark')
        for placemark in placemarks:
            polygon = placemark.getElementsByTagName('Polygon')
            if polygon:
                outer_boundary = polygon[0].getElementsByTagName('outerBoundaryIs')
                if outer_boundary:
                    coordinates_str = outer_boundary[0].getElementsByTagName('coordinates')[0].childNodes[0].data
                    coordinates_list = coordinates_str.strip().split()
                    for coord in coordinates_list:
                        lon, lat, _ = coord.split(',')
                        coordinates.append((float(lon), float(lat)))
    return coordinates

def is_inside_polygon(point, polygon_coordinates):
    """
    Check if a point is inside the given polygon.
    """
    polygon = Polygon(polygon_coordinates)
    point = Point(point)
    return polygon.contains(point)

def is_point_in_path(x: int, y: int, poly: list[tuple[int, int]]) -> bool:
    """Determine if the point is on the path, corner, or boundary of the polygon

    Args:
      x -- The x coordinates of point.
      y -- The y coordinates of point.
      poly -- a list of tuples [(x, y), (x, y), ...]

    Returns:
      True if the point is in the path or is a corner or on the boundary"""
    c = False
    for i in range(len(poly)):
        ax, ay = poly[i]
        bx, by = poly[i - 1]
        if (x == ax) and (y == ay):
            # point is a corner
            return True
        if (ay > y) != (by > y):
            slope = (x - ax) * (by - ay) - (bx - ax) * (y - ay)
            if slope == 0:
                # point is on boundary
                return True
            if (slope < 0) != (by < ay):
                c = not c
    return c


if __name__ == "__main__":
    kml_file_path = "/home/avengers/py-tracker/kml_files/Home Fence.kml"
    polygon_coordinates = read_kml(kml_file_path)
    
    print(polygon_coordinates)
    
    x = -121.9017480
    y = 37.7047640
    
    # Test point
    test_point = (x, y)  # Insert the longitude and latitude of your test point here
        
    if is_inside_polygon(test_point, polygon_coordinates):
        print("Test point is inside the polygon.")
    else:
        print("Test point is outside the polygon.")
        
        
    inside = is_point_in_path(x, y, polygon_coordinates)
    
    if inside:
        print("Test point is inside the polygon.")
    else:
        print("Test point is outside the polygon.")

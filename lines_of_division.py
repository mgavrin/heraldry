import math
from device_generator import *
from enum import Enum
constant_definitions =open("constants.py")
exec(constant_definitions.read())

class Orientation(Enum):
    FESSWISE = 0
    PALEWISE = 90
    BENDWISE = 135
    BENDWISE_SINISTER = 45

def alternator(x):
    '''
    Helper function for points alternating opposite sides of a line of division.
    '''
    if x%2 == 0:
        return 1
    return -1

def indented(tinctures, location, orientation,
             num_points = 7, depth_pixels = 30):
    '''
    Returns a Device with exactly one FieldSection, containing an 
      indented line of division.
    Tinctures: a list of exactly two tinctures.
    location: a Rect representing the location of the line of
      division on the screen. If the orientation is per fess or per pale,
      the points will go to the edge of the rect. Otherwise, the depth of
      the points should be determined by depth_pixels.
    Orientation: an Orientation object describing the orientation of the line
      of division.
    Num_points: the number of points of each tincture. For one tincture this
      will include two half-points at the end, counting as one.
    Depth_pixels: the component of the distance from a point of one tincture to
      a point of the other tincture that is perpendicular to the line of
      division. Ignored if orientation is per pale or per fess.
    '''
    size = (kScreenWidth, kScreenHeight)
    surface_0 = pygame.Surface(size, 0, 32)
    surface_0.fill(tinctures[0])
    mask_0 = pygame.Surface(size, 0, 32)
    surface_1 = pygame.Surface(size, 0, 32)
    surface_1.fill(tinctures[1])
    mask_1 = pygame.Surface(size, 0, 32)
    if len(tinctures) != 2:
        print ("A line of division must have two tinctures.")
        return Device("")
    if orientation == Orientation.FESSWISE:
        increment = int(location.width/num_points/2)
        x_points = range(location.left, location.right, increment)
        y_points = [(location.top + (location.height * (i%2)))
                    for i in range(len(x_points))]
        points = [[x_points[i], y_points[i]] for i in range(len(x_points))]
        chief_boundary = [[location.right, location.top]]+ points
        base_boundary = points + [[location.right, location.bottom],
                                  [location.left, location.bottom]]
        
    elif orientation == Orientation.PALEWISE:
        increment = int(location.height/num_points/2)
        y_points = range(location.top, location.bottom, increment)
        x_points = [(location.left + (location.width * (i%2)))
                    for i in range(len(y_points))]
        points = [[x_points[i], y_points[i]] for i in range(len(x_points))]
        chief_boundary = [[location.left, location.top]]+ points
        base_boundary = points + [[location.right, location.bottom],
                                  [location.right, location.top]]
        
    elif (orientation == Orientation.BENDWISE or
          orientation == Orientation.BENDWISE_SINISTER):
        x_increment = int(location.width/num_points)
        y_increment = int(location.height/num_points)
        # stick an extra point above and to the left
        # and one below and to the right
        # for east of connecting the polygons later
        if orientation == Orientation.BENDWISE:
            x_points = range(location.left - x_increment,
                             location.right + x_increment,
                             x_increment)
        else:
            x_points = range(location.right + x_increment,
                             location.left - x_increment,                             
                             -x_increment)
        y_points = range(location.top - y_increment,
                         location.bottom + y_increment,
                         y_increment)
        if len(x_points) > len(y_points):
            x_points = x_points[:len(y_points)]
        if len(y_points) > len(x_points):
            y_points = y_points[:len(x_points)]
        point_depth_x = math.sqrt(depth_pixels**2*location.width**2/
                                  (location.width**2+location.height**2))
        point_depth_y = math.sqrt(depth_pixels**2-point_depth_x**2)
        point_depth_x = int(point_depth_x)
        point_depth_y = int(point_depth_y)
        x_points = [(x_points[i] + point_depth_x*alternator(i))
                    for i in range(len(x_points))]
        if orientation == Orientation.BENDWISE:
            # note the subtraction here
            y_points = [(y_points[i] - point_depth_y*alternator(i))
                        for i in range(len(y_points))]
        else:
            y_points = [(y_points[i] + point_depth_y*alternator(i))
                        for i in range(len(y_points))]
            
        points = [[x_points[i], y_points[i]] for i in range(len(x_points))]
        if (num_points % 2 == 0):
            chief_boundary = points
            base_boundary = points[1:len(points)-1]
        else:
            chief_boundary = points[:len(points)-1]
            base_boundary = points[1:]
        if orientation == Orientation.BENDWISE_SINISTER:
            chief_boundary, base_boundary = base_boundary, chief_boundary
        
    pygame.draw.polygon(mask_0, kGrey, chief_boundary)
    pygame.draw.polygon(mask_1, kGrey, base_boundary)
    return Device("", [FieldSection(surface_0, mask_0),
                       FieldSection(surface_1, mask_1)])
    

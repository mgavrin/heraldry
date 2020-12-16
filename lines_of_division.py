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
        print ("An line of division must have two tinctures.")
        return Device("")
    print("location y boundaries:", location.top, location.bottom)
    if orientation == Orientation.FESSWISE:
        increment = int(location.width/num_points/2)
        x_points = range(location.left, location.right, increment)
        y_points = [(location.top + (location.height * (i%2)))
                    for i in range(len(x_points))]
        points = [[x_points[i], y_points[i]] for i in range(len(x_points))]
        chief_boundary = [[location.right, location.top]]+ points
        base_boundary = points + [[location.right, location.bottom],
                                  [location.left, location.bottom]]
        pygame.draw.polygon(mask_0, kGrey, chief_boundary)
        pygame.draw.polygon(mask_1, kGrey, base_boundary)
        return Device("", [FieldSection(surface_0, mask_0),
                           FieldSection(surface_1, mask_1)])
        
    elif orientation == Orientation.PALEWISE:
        print ("palewise")
    elif orientation == Orientation.BENDWISE:
        print ("bendwise")
    elif orientation == Orientation.BENDWISE_SINISTER:
        print ("bendwise_sinister")

    

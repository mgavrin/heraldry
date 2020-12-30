import math
from device_generator import *
from enum import Enum
constant_definitions =open("constants.py")
exec(constant_definitions.read())

def alternator(x):
    '''
    Helper function for points alternating opposite sides 
      of a line of division.
    '''
    if x%2 == 0:
        return 1
    return -1

def get_longest_line_increments(endpoints, num_points):
    '''
    Takes a list of lines and a number of points and returns the
      x and y intervals between points that will fit num_points
      along the longest line, as a tuple (x, y).
    '''
    x_interval = 0
    y_interval = 0
    greatest_distance = 0
    for line in endpoints:
        x_distance = line[1][0] - line[0][0]
        y_distance = line[1][1] - line[0][1]
        total_distance = math.sqrt(x_distance**2 + y_distance**2)
        if total_distance > greatest_distance:
            x_increment = int(x_distance/num_points)
            y_increment = int(y_distance/num_points)
    return (x_increment, y_increment)
            
        

def indented(tinctures, endpoints, num_points = 8, depth_pixels = 30):
    '''
    Returns a Device with an even number of FieldSections, depicting
      one or more indented lines of division.
    Tinctures: a list of exactly two tinctures.
    Endpoints: a list of lists, each of exactly two lists,
      each of exactly two points: 
      [[[x1a,y1a],[x1b,y1b]],[[x2a,y2a],[x2b,y2b]],...[[xNa,yNa],[xNb,yNb]]].
      These are the endpoints of each indented line.
      Note: It is *the responsibility of the caller* to make sure the lines
      indicated are parallel, sufficiently far apart not to look stupid, etc.
    Num_points: the number of points of each tincture along the longest line.
      For one tincture this will include two half-points at the end,
      counting as one. Fewer points may be displayed if they won't fit.
    Depth_pixels: the component of the distance from a point of one tincture to
      a point of the other tincture that is perpendicular to the line of
      division.
    '''
    # Validation of inputs
    if len(tinctures) != 2:
        print ("Error: A line of division must have two tinctures.")
        return Device("")
    for line in endpoints:
        if len(line) != 2 or len(line[0]) != 2 or len(line[1]) != 2 :
            print("Error: Lines of division must have exactly two endpoints",
                  "of two values each.", "Nonconforming value:", line)
            return Device("")
    # Setup
    size = (kScreenWidth, kScreenHeight)
    surface_0 = pygame.Surface(size, 0, 32)
    surface_0.fill(kAzure)
    #surface_0.fill(tinctures[0])
    mask_0 = pygame.Surface(size, 0, 32)
    surface_1 = pygame.Surface(size, 0, 32)
    surface_1.fill(kVert)
    #surface_1.fill(tinctures[1])
    mask_1 = pygame.Surface(size, 0, 32)
    # The important bit
    (x_increment, y_increment) = get_longest_line_increments(
        endpoints, num_points)
    field_sections = []
    for i in range(len(endpoints)):
        line = endpoints[i]
        print("Line is", line)
        # x and y distances are defined relative to the order
        # the points are passed in, and either or both
        # may be negative.
        x_distance = line[1][0] - line[0][0]
        y_distance = line[1][1] - line[0][1]
        if x_distance == 0 and y_distance == 0:
            print("Warning: line starts and ends at",
                  line[0], ". Skipping.")
            continue
        if ((abs(x_distance) < num_points and x_distance != 0) or
            (abs(y_distance) < num_points and y_distance != 0)):
            print("Warning: extreme slopes will be rounded",
                  "to horizontal or vertical.")
        # stick an extra point above and to the left
        # and one below and to the right
        # for ease of connecting the polygons later
        if x_distance > 0:
            x_points = range(line[0][0] - 2*x_increment,
                             line[1][0] + 2*x_increment,
                             x_increment)
        elif x_distance < 0:
            # You need the negative weirdness or the points
            # will be in the wrong order!
            x_points = range(line[0][0] + 2*x_increment,
                             line[1][0] - 2*x_increment,
                             x_increment)
            print("x_points is", x_points)
        else:
            x_points = [line[0][0]] * (num_points + 4)
        if y_distance > 0:
            y_points = range(line[0][1] - 2*y_increment,
                             line[1][1] + 2*y_increment,
                             y_increment)
            print("y_points is", y_points)
        elif y_distance < 0:
            # You need the negative weirdness or the points
            # will be in the wrong order!
            y_points = range(line[0][1] + 2*y_increment,
                             line[1][1] - 2*y_increment,
                             y_increment)
        else:
            y_points = [line[0][1]] * (num_points + 4)
        if len(x_points) > len(y_points):
            x_points = x_points[:len(y_points)]
        if len(y_points) > len(x_points):
            y_points = y_points[:len(x_points)]
        point_depth_x = math.sqrt(depth_pixels**2 * y_distance**2 /
                                  (y_distance**2 + x_distance**2))
        point_depth_y = math.sqrt(depth_pixels**2-point_depth_x**2)
        point_depth_x = int(point_depth_x)
        point_depth_y = int(point_depth_y)
        x_points = [(x_points[i] + point_depth_x*alternator(i))
                    for i in range(len(x_points))]
        if (x_distance > 0) == (y_distance > 0):
            y_points = [(y_points[i] - point_depth_y*alternator(i))
                        for i in range(len(y_points))]
        else: 
            y_points = [(y_points[i] + point_depth_y*alternator(i))
                        for i in range(len(y_points))]
        points = [[x_points[i], y_points[i]] for i in range(len(x_points))]
        print("Points are",points)
        # TODO take this out
        for point in points:
            pygame.draw.circle(mask_0, kGrey, point, 5)
        if (len(points) % 2 == 0):
            chief_boundary = points[1:]
            base_boundary = points[:len(points)-1]
        else:
            chief_boundary = points[1:len(points)-1]
            base_boundary = points
            
        # Make sure the chief boundary starts out on top
        # for mostly-horizontal lines
        if (x_distance > y_distance and
            chief_boundary[0][1] > base_boundary[0][1]):
            chief_boundary, base_boundary = base_boundary, chief_boundary
        # Make sure the chief boundary starts out on the left
        # for mostly-vertical lines
        if (y_distance > x_distance and
            chief_boundary[0][0] > base_boundary[0][0]):
            chief_boundary, base_boundary = base_boundary, chief_boundary
            
        # reverse direction on multiple stripes (e.g. paly)
        if (i%2 == 1):
            chief_boundary, base_boundary = base_boundary, chief_boundary
        pygame.draw.polygon(mask_0, kGrey, chief_boundary)
        pygame.draw.polygon(mask_1, kGrey, base_boundary)
        field_sections.append(FieldSection(surface_0, mask_0))
        field_sections.append(FieldSection(surface_1, mask_1))
    return Device("", field_sections)

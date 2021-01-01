import math
from device_generator import *
import lines_of_division
from enum import Enum
constant_definitions =open("constants.py")
exec(constant_definitions.read())

def trim_mask(surface, location):
    '''
    Removes everything from the provided surface that falls outside the
      provided rectangle.
    surface: a pygame Surface.
    location: a pygame Rect specifying the area to trim to.
    returns: a new Surface that has been trimmed to be empty outside the
      location Rect.
    '''
    surface.lock()
    new_surface=pygame.Surface(surface.get_size())
    new_surface.lock()
    for x in range(location.left, location.right):
        for y in range(location.top, location.bottom):
            new_surface.set_at((x,y), surface.get_at((x,y)))
    surface.unlock()
    new_surface.unlock()
    return new_surface

def get_plain_field(tincture, location):
    '''
    Returns a FieldSection with a single tincture.
    tincture: the tincture in question, as a tuple of 
      three integers representing RGB values.
    location: a Rect representing the location of the FieldSection on the screen.
     If the plain field should fill the entire shield, the Rect should be 
     Rect(kXMargin, kYMargin, kScreenWidth-2*kXMargin, kShieldBottom-kYMargin).
    '''
    boundary = [[location.left, location.top], [location.left, location.bottom],
                [location.right, location.bottom], [location.right, location.top]]
    size = (kScreenWidth, kScreenHeight)
    surface = pygame.Surface(size, 0, 32)
    surface.fill(tincture)
    mask = pygame.Surface(size, 0, 32)
    pygame.draw.polygon(mask, kGrey, boundary)
    return Device("", [FieldSection(surface, mask)])

def get_paly_boundaries(n, location):
    '''
    Returns a tuple of a list of lists of lists which is the boundary boxes 
      for a paly of n field, and a list of 2-item lists of 2-item lists
      which are the lines of division. 
    n: the number of stripes. Use 2 for per pale.
    location: a Rect representing the location on the screen of the paly portion of the field.
      If the paly field should fill the entire shield, the Rect should be 
      Rect(kXMargin, kYMargin, kScreenWidth-2*kXMargin, kShieldBottom-kYMargin).
    '''
    boundaries = []
    endpoints = []
    for i in range(n):
        left_edge = int(location.left + location.width*i/n)
        right_edge = int(location.left + location.width*(i+1)/n)
        boundaries.append(
            [[left_edge, location.top], [left_edge, location.bottom],
             [right_edge, location.bottom], [right_edge, location.top]])
        if i != 0:
            endpoints.append([[left_edge, location.top],
                              [left_edge, location.bottom]])
    return (boundaries, endpoints)

def get_barry_boundaries(n, location):
    '''
    Returns a list of lists of lists which is the boundary boxes 
      for a barry of n field.
    n: the number of sections. Use 2 for per fess.
    location: a Rect representing the location on the screen of the paly portion of the field.
     If the paly field should fill the entire shield, the Rect should be 
     Rect(kXMargin, kYMargin, kScreenWidth-2*kXMargin, kShieldBottom-kYMargin).
    '''
    boundaries = []
    endpoints = []
    for i in range(n):
        top_edge = int(location.top + location.height*i/n)
        bottom_edge = int(location.top + location.height*(i+1)/n)
        boundaries.append(
            [[location.left, top_edge], [location.right, top_edge],
             [location.right, bottom_edge], [location.left, bottom_edge]])
        if i != 0:
            endpoints.append([[location.left, top_edge],
                              [location.right, top_edge]])
    return (boundaries, endpoints)

def get_bendy_boundaries(n, location):
    '''
    Returns a list of lists of lists which is the boundary boxes 
      for a bendy of n field, and a set of lists of 2-item lists
      which are the endpointsof the lines of division.
    n: the number of sections. Use 2 for per bend.
    location: a Rect representing the location on the screen
      of the bendy portion of the field.
      If the bendy field should fill the entire shield, the Rect should be 
      Rect(kXMargin, kYMargin, kScreenWidth-2*kXMargin, kShieldBottom-kYMargin).
    Note: due to the taper at the bottom of the shield, if the bendy field is on the full
      shield the dexter base stripe(s) may not be visible.
    '''
    boundaries = []
    endpoints = []
    
    # Every stripe goes along either the chief and sinister edges
    # or the dexter and base edges, except the middle
    # stripe if n is odd.

    # The coordinates of the stripe boundary points,
    # going from the corner triangles to the central stripe.
    x_half_interval = int(location.width/n)
    y_half_interval = int(location.height/n)
    chief_points = []
    base_points = []
    dexter_points = []
    sinister_points = []
    counter = 0
    while counter*x_half_interval*2 <= location.width:
        # The +1 and -1 compensate for rounding errors
        base_points.append(location.left + counter*x_half_interval*2 + 1)
        chief_points.append(location.right - counter*x_half_interval*2 - 1)
        sinister_points.append(location.top + counter*y_half_interval*2 + 1)
        dexter_points.append(location.bottom - counter*y_half_interval*2 - 1)
        counter += 1

    # These three blocks need to be in this order
    # so they get blit in the right order with alternating tinctures!
    for i in range(int(n/2)):
        # stripes that touch the chief and dexter edges;
        # widdershins from sinister chief.
        boundaries.append([[chief_points[i], location.top],
                           [chief_points[i+1], location.top],
                           [location.right, sinister_points[i+1]],
                           [location.right, sinister_points[i]]])
        endpoints.append([[chief_points[i+1], location.top],
                          [location.right, sinister_points[i+1]]])
    # make sure to get the middle section if n is odd
    if n%2 == 1:
        boundaries.append([[chief_points[-1], location.top],
                           [location.left, location.top],
                           [location.left, dexter_points[-1]],
                           [base_points[-1], location.bottom],
                           [location.right, location.bottom],
                           [location.right, sinister_points[-1]]])
    for i in range(int(n/2)-1, -1, -1):
        # Stripes that touch the sinister and base edges;
        # deasil from sinister base. Count down i to go from
        # center to corner or the alternating tinctures will be wrong.
        boundaries.append([[base_points[i+1], location.bottom],
                           [base_points[i], location.bottom],
                           [location.left, dexter_points[i]],
                           [location.left, dexter_points[i+1]]])
        endpoints.append([[location.left, dexter_points[i+1]],
                           [base_points[i+1], location.bottom]])
    return (boundaries, endpoints)

def get_bendy_sinister_boundaries(n, location):
    '''
    Returns a list of lists of lists which is the boundary boxes 
      for a bendy sinister of n field.
    n: the number of sections. Use 2 for per bend sinister.
    location: a Rect representing the location on the screen of the 
      bendy sinister portion of the field.
      If the bendy sinister field should fill the entire shield, the Rect should be 
      Rect(kXMargin, kYMargin, kScreenWidth-2*kXMargin, kShieldBottom-kYMargin).
    '''
    boundaries = []
    endpoints = []
    for i in range(n):
        # multiply by 2 because you need a 2x rectangle to get
        # every stripe from top to left. This will produce some
        # boundaries that go outside the location rect, but get_striped_field
        # will trim them later.
        dexter_x = location.left + int(location.width*i*2/n)
        sinister_x = location.left + int(location.width*(i+1)*2/n)
        chief_y = location.top + int(location.height*(i)*2/n)
        base_y = location.top + int(location.height*(i+1)*2/n)
        boundaries.append(
            [[dexter_x, location.top],
             [sinister_x, location.top],
             [location.left, base_y], [location.left, chief_y]])
        if i != 0:
            endpoints.append([[sinister_x, location.top],
                              [location.left, base_y]])
    print("Bendy sinister endpoints:", endpoints)
    return (boundaries, endpoints)

def get_chevronelly_boundaries(n, location):
    '''
    Returns a list of lists of lists which is the boundary boxes 
      for a chevronelly of n field.
    n: the number of sections. Use 2 for per chevron.
    location: a Rect representing the location on the screen of the 
      chevronelly portion of the field.
      If the chevronelly field should fill the entire shield, the Rect should be 
      Rect(kXMargin, kYMargin, kScreenWidth-2*kXMargin, kShieldBottom-kYMargin).
    '''
    boundaries = []
    # change this value for "steeper" or "shallower" chevrons
    steepness = 0.125
    y_offset = int(location.height*steepness)
    # increase height so the pulled-up bit in the middle doesn't leave a gap
    # underneath. get_striped_field will trim off the extra.
    total_height = location.height+y_offset
    for i in range(n):
        boundaries.append([[location.left, int(location.top+total_height*i/n)],
                           [location.centerx, int(location.top+total_height*i/n-y_offset)],
                           [location.right, int(location.top+total_height*i/n)],
                           [location.right, int(location.top+total_height*(i+1)/n)],
                           [location.centerx, int(location.top+total_height*(i+1)/n-y_offset)],
                           [location.left, int(location.top+total_height*(i+1)/n)]])
    return boundaries

def get_chevronelly_inverted_boundaries(n, location):
    '''
    Returns a list of lists of lists which is the boundary boxes 
      for a chevronelly inverted of n field.
    n: the number of sections. Use 2 for per chevron inverted.
    location: a Rect representing the location on the screen of the 
      chevronelly inverted portion of the field.
      If the chevronelly inverted field should fill the entire shield, 
      the Rect should be 
      Rect(kXMargin, kYMargin, kScreenWidth-2*kXMargin, kShieldBottom-kYMargin).
    '''
    boundaries = []
    # change this value for "steeper" or "shallower" chevrons
    steepness = 0.125
    y_offset = int(location.height*steepness)
    # increase height so the pulled-up bit in the middle doesn't leave a gap
    # underneath. get_striped_field will trim off the extra.
    total_height = location.height+y_offset
    for i in range(n):
        boundaries.append([[location.left, int(location.top+total_height*i/n-y_offset)],
                           [location.centerx, int(location.top+total_height*i/n)],
                           [location.right, int(location.top+total_height*i/n-y_offset)],
                           [location.right, int(location.top+total_height*(i+1)/n-y_offset)],
                           [location.centerx, int(location.top+total_height*(i+1)/n)],
                           [location.left, int(location.top+total_height*(i+1)/n-y_offset)]])
    return boundaries

class LineType(Enum):
    PLAIN = 0
    INDENTED = 1

def get_striped_field(num_sections, tinctures, direction, location,
                      line_type = LineType.PLAIN):
    '''
    Returns a Device with a field containing one or more parallel lines of division.
    num_sections: the number of sections.
    tinctures: a list of tincture objects, e.g. [kVert, kArgent], dexter chief zeroth.
    direction: a string indicating direction.
      Must be one of the keys in the dict below.
    location: a Rect representing the location on the screen of the
      striped portion of the field.
      If the striped field should fill the entire shield, the Rect should be 
      Rect(kXMargin, kYMargin, kScreenWidth-2*kXMargin, kShieldBottom-kYMargin).
    line_type: a LineType enum value indicating whether the lines of division
      should be simple or a particular complex type.
    '''
    # The values in this dict are functions.
    directions = {"per pale": get_paly_boundaries, "paly": get_paly_boundaries,
                  "per fess": get_barry_boundaries, "barry": get_barry_boundaries,
                  "per bend": get_bendy_boundaries, "bendy": get_bendy_boundaries,
                  "per bend sinister": get_bendy_sinister_boundaries,
                  "bendy sinister": get_bendy_sinister_boundaries,
                  "per chevron": get_chevronelly_boundaries,
                  "chevronelly": get_chevronelly_boundaries,
                  "per chevron inverted": get_chevronelly_inverted_boundaries,
                  "chevronelly inverted": get_chevronelly_inverted_boundaries}
    field_sections = []
    (boundaries, endpoints) = directions[direction](num_sections, location)
    size = (kScreenWidth, kScreenHeight)
    # One surface and mask per tincture
    masks_by_tincture = {}
    for tincture in tinctures:
        surface = pygame.Surface(size, 0, 32)
        surface.fill(tincture)
        mask = pygame.Surface(size, 0, 32)
        masks_by_tincture[tincture] = (surface, mask)
        
    for i in range(num_sections):
        tincture = tinctures[i % len(tinctures)]
        (surface, mask) = masks_by_tincture[tincture]
        # If the stripes would extend outside the location rect,
        # don't let them
        mask.set_clip(location)
        pygame.draw.polygon(mask, kGrey, boundaries[i])
        # TAKE THIS OUT
        for point in boundaries[i]:
            pygame.draw.circle(surface, kAzure, point, 6)
        # END TAKE THIS OUT
        mask = trim_mask(mask, location)

    for (surface, mask) in masks_by_tincture.values():
        field_sections.append(FieldSection(surface, mask))

    field = Device("", field_sections)
    
    if line_type == LineType.PLAIN:
        pass
    elif line_type == LineType.INDENTED:
        lines = lines_of_division.indented(tinctures, endpoints)
        for section in lines.field_sections:
            section.mask = trim_mask(section.mask, location)
        field.merge(lines)
    else:
        print("Error: Unsupported line type", line_type.name)
    
    return field

def get_quarterly_field(tinctures, location):
    '''
    Returns a device object with a quarterly field.
    tinctures: a list of exactly two or four tinctures. Two is recommended.
      If two, the dexter chief and sinister base quarters are the 0th tincture,
      and the sinister chief and dexter base quarters are the 1st tincture.
      If four, the tinctures are used in the order
      [dexter chief, sinister chief, sinister base, dexter base].
    location: a Rect representing the location on the screen of the 
      quarterly portion of the field. If the quarterly field should 
      fill the entire shield, the Rect should be 
      Rect(kXMargin, kYMargin, kScreenWidth-2*kXMargin, kShieldBottom-kYMargin).
    '''
    if len(tinctures) != 2 and len(tinctures) != 4:
        print("Quarterly fields can't have", len(tinctures), "tinctures")
        return Device("")
    dexter_chief_quarter = [[location.left, location.top],
                            [location.centerx, location.top],
                            [location.centerx, location.centery],
                            [location.left, location.centery]]
    sinister_chief_quarter = [[location.centerx, location.top],
                            [location.right, location.top],
                            [location.right, location.centery],
                            [location.centerx, location.centery]]
    sinister_base_quarter = [[location.centerx, location.centery],
                            [location.right, location.centery],
                            [location.right, location.bottom],
                            [location.centerx, location.bottom]]
    dexter_base_quarter = [[location.left, location.centery],
                            [location.centerx, location.centery],
                            [location.centerx, location.bottom],
                            [location.left, location.bottom]]
    quarters = [dexter_chief_quarter, sinister_chief_quarter,
                sinister_base_quarter, dexter_base_quarter]
    size = (kScreenWidth, kScreenHeight)
    field_sections = []
    for i in range(4):
        surface = pygame.Surface(size, 0, 32)
        surface.fill(tinctures[i % len(tinctures)])
        mask = pygame.Surface(size, 0, 32)
        pygame.draw.polygon(mask, kGrey, quarters[i])
        mask = trim_mask(mask, location)
        field_sections.append(FieldSection(surface, mask))
    return Device("", field_sections)

def get_per_saltire_field(tinctures, location):
    '''
    Returns a device object with a per saltire field.
    tinctures: a list of exactly two or four tinctures. Two is recommended.
      If two, the chief and base sections are the 0th tincture and the
      dexter and sinister sections are the 1st tincture.
      If four, the tinctures are used widdershins from chief:
      [chief, dexter, base, sinister].
    location: a Rect representing the location on the screen of the per saltire 
      portion of the field. If the per saltire field should fill the entire shield, 
      the Rect should be 
      Rect(kXMargin, kYMargin, kScreenWidth-2*kXMargin, kShieldBottom-kYMargin).
    '''
    if len(tinctures) != 2 and len(tinctures) != 4:
        print("Per saltire fields can't have", len(tinctures), "tinctures")
        return Device("")
    chief_boundary =    [[location.left, location.top],
                         [location.right, location.top],
                         [location.centerx, location.centery]]
    dexter_boundary =   [[location.left, location.top],
                         [location.left, location.bottom],
                         [location.centerx, location.centery]]
    base_boundary =     [[location.left, location.bottom],
                         [location.right, location.bottom],
                         [location.centerx, location.centery]]
    sinister_boundary = [[location.right, location.top],
                         [location.right, location.bottom],
                         [location.centerx, location.centery]]
    boundaries = [chief_boundary, dexter_boundary, base_boundary, sinister_boundary]
    size = (kScreenWidth, kScreenHeight)
    field_sections = []
    for i in range(4):
        surface = pygame.Surface(size, 0, 32)
        surface.fill(tinctures[i % len(tinctures)])
        mask = pygame.Surface(size, 0, 32)
        pygame.draw.polygon(mask, kGrey, boundaries[i])
        mask = trim_mask(mask, location)
        field_sections.append(FieldSection(surface, mask))
    return Device("", field_sections)

def get_per_chevron_throughout_field(tinctures, location):
    '''
    Returns a Device with a per chevron throughout field.
    tinctures: a list of exactly two tinctures.
      The outer sections are the 0th tincture and the inner section
      is the 1st tincture.
    location: a Rect representing the location on the screen of the per chevron throughout 
      portion of the field. If the entire field should be per chevron througout, 
      the Rect should be 
      Rect(kXMargin, kYMargin, kScreenWidth-2*kXMargin, kShieldBottom-kYMargin).
    '''
    if len(tinctures) != 2:
        print ("A per chevron throughout field must have exactly two tinctures.")
        return Device("")
    chief_boundary = [[location.left, location.top], [location.left, location.bottom],
                      [location.centerx, location.top], [location.right, location.bottom],
                      [location.right, location.top]]
    base_boundary = [[location.left, location.bottom],
                     [location.centerx, location.top],
                     [location.right, location.bottom]] 
    size = (kScreenWidth, kScreenHeight)
    chief_surface = pygame.Surface(size, 0, 32)
    chief_surface.fill(tinctures[0])
    chief_mask = pygame.Surface(size, 0, 32)
    pygame.draw.polygon(chief_mask, kGrey, chief_boundary)
    chief_mask = trim_mask(chief_mask, location)
    chief_section = FieldSection(chief_surface, chief_mask)
    
    base_surface = pygame.Surface(size, 0, 32)
    base_surface.fill(tinctures[1])
    base_mask = pygame.Surface(size, 0, 32)
    pygame.draw.polygon(base_mask, kGrey, base_boundary)
    base_mask = trim_mask(base_mask, location)
    base_section = FieldSection(base_surface, base_mask)
    return Device("", [chief_section, base_section])
    
def get_per_chevron_inverted_throughout_field(tinctures, location):
    '''
    Returns a Device with a per chevron inverted throughout field.
    tinctures: a list of exactly two tinctures.
      The middle section is the 0th tincture and the outer sections
      are the 1st tincture.
    location: a Rect representing the location on the screen of the per chevron
      inverted throughout portion of the field. If the entire field should be 
      per chevron inverted througout, the Rect should be 
      Rect(kXMargin, kYMargin, kScreenWidth-2*kXMargin, kShieldBottom-kYMargin).
    '''
    x_margin = int(kScreenWidth/22)
    if len(tinctures) != 2:
        print ("A per chevron inverted throughout field must have exactly two tinctures.")
        return Device("")
    chief_boundary = [[location.left, location.top],
                     [location.centerx, location.bottom],
                     [location.right, location.top]]
    base_boundary = [[location.left, location.bottom], [location.left, location.top],
                      [location.centerx, location.bottom], [location.right, location.top],
                      [location.right, location.bottom]] 
    size = (kScreenWidth, kScreenHeight)
    chief_surface = pygame.Surface(size, 0, 32)
    chief_surface.fill(tinctures[0])
    chief_mask = pygame.Surface(size, 0, 32)
    pygame.draw.polygon(chief_mask, kGrey, chief_boundary)
    chief_mask = trim_mask(chief_mask, location)
    chief_section = FieldSection(chief_surface, chief_mask)
    
    base_surface = pygame.Surface(size, 0, 32)
    base_surface.fill(tinctures[1])
    base_mask = pygame.Surface(size, 0, 32)
    pygame.draw.polygon(base_mask, kGrey, base_boundary)
    base_mask = trim_mask(base_mask, location)
    base_section = FieldSection(base_surface, base_mask)
    return Device("", [chief_section, base_section])

def get_vetu_field(tinctures, location):
    '''
    Returns a Device with a vetu field.
    tinctures: a list of exactly two tinctures.
      The outer sections are the 0th tincture, and the inner
      lozenge is the 1st tincture.
    location: a Rect representing the location on the screen of the vetu
      portion of the field. For a vetu field on the full shield, the Rect should be 
      Rect(kXMargin, kYMargin, kScreenWidth-2*kXMargin, kShieldBottom-kYMargin).
   '''
    if len(tinctures) != 2:
        print ("A vetu field must have exactly two tinctures.")
        return Device("")
    outer_boundary = [[location.centerx, location.top],
                      [location.left, location.top], [location.left, location.bottom],
                      [location.right, location.bottom], [location.right, location.top],
                      [location.centerx, location.top], [location.left, location.centery],
                      [location.centerx, location.bottom], [location.right, location.centery]]
    inner_boundary = outer_boundary[5:]
    size = (kScreenWidth, kScreenHeight)
    outer_surface = pygame.Surface(size, 0, 32)
    outer_surface.fill(tinctures[0])
    outer_mask = pygame.Surface(size, 0, 32)
    pygame.draw.polygon(outer_mask, kGrey, outer_boundary)
    outer_mask = trim_mask(outer_mask, location)
    outer_section = FieldSection(outer_surface, outer_mask)
    
    inner_surface = pygame.Surface(size, 0, 32)
    inner_surface.fill(tinctures[1])
    inner_mask = pygame.Surface(size, 0, 32)
    pygame.draw.polygon(inner_mask, kGrey, inner_boundary)
    inner_mask = trim_mask(inner_mask, location)
    inner_section = FieldSection(inner_surface, inner_mask)
    return Device("", [outer_section, inner_section])

def get_vetu_ploye_field(tinctures, location):
    '''
    Returns a Device with a vetu ploye field.
    tinctures: a list of exactly two tinctures.
      The outer sections are the 0th tincture, and the inner
      lozenge is the 1st tincture.
    location: a Rect representing the location on the screen of the vetu ploye
      portion of the field. For a vetu ploye field on the full shield, the Rect should be 
      Rect(kXMargin, kYMargin, kScreenWidth-2*kXMargin, kShieldBottom-kYMargin).

   '''
    if len(tinctures) != 2:
        print ("A vetu ploye field must have exactly two tinctures.")
        return Device("")
    size = (kScreenWidth, kScreenHeight)
    outer_surface = pygame.Surface(size, 0, 32)
    outer_surface.fill(tinctures[0])
    outer_mask = pygame.Surface(size, 0, 32)
    # starburst_mask.png is already kGrey in the appropriate places
    outer_mask_scaled = pygame.transform.scale(
        pygame.image.load(os.path.join("art", "starburst_mask.png")),
        (location.width, location.height))
    outer_mask.blit(outer_mask_scaled, (location.left, location.top))
    outer_mask = trim_mask(outer_mask, location)
    outer_section = FieldSection(outer_surface, outer_mask)

    inner_surface = pygame.Surface(size, 0, 32)
    inner_surface.fill(tinctures[1])
    inner_mask = pygame.Surface(size, 0, 32)
    inner_mask.fill(kGrey)
    inner_mask = trim_mask(inner_mask, location)
    inner_section = FieldSection(inner_surface, inner_mask)
    # Order is important here: inner_section is just a solid color with no shape,
    # so outer_section needs to be on top.
    return Device("", [inner_section, outer_section])

def get_per_pall_field(tinctures, location):
    '''
    Returns a device with a per pall field.
    tinctures: a list of exactly 3 tinctures,
     which will be used in the order [chief, dexter, sinister].
    location: a Rect representing the location on the screen of the per pall
      portion of the field. For a per pall field on the full shield, the Rect should be 
      Rect(kXMargin, kYMargin, kScreenWidth-2*kXMargin, kShieldBottom-kYMargin).
    '''
    if len(tinctures) != 3:
        print("A per pall field must have exactly 3 tinctures.")
        return Device("")
    center = [location.centerx, int(location.top+location.height*0.3)]
    chief_boundary = [[location.left, location.top], [location.right, location.top], center]
    dexter_boundary = [[location.left, location.top], [location.left, location.bottom],
                       [location.centerx, location.bottom], center]
    sinister_boundary = [[location.right, location.top], [location.right, location.bottom],
                         [location.centerx, location.bottom], center]
    size = (kScreenWidth, kScreenHeight)
    
    chief_surface = pygame.Surface(size, 0, 32)
    chief_surface.fill(tinctures[0])
    chief_mask = pygame.Surface(size, 0, 32)
    pygame.draw.polygon(chief_mask, kGrey, chief_boundary)
    
    dexter_surface = pygame.Surface(size, 0, 32)
    dexter_surface.fill(tinctures[1])
    dexter_mask = pygame.Surface(size, 0, 32)
    pygame.draw.polygon(dexter_mask, kGrey, dexter_boundary)
    
    sinister_surface = pygame.Surface(size, 0, 32)
    sinister_surface.fill(tinctures[2])
    sinister_mask = pygame.Surface(size, 0, 32)
    pygame.draw.polygon(sinister_mask, kGrey, sinister_boundary)
    
    chief_mask = trim_mask(chief_mask, location)
    dexter_mask = trim_mask(dexter_mask, location)
    sinister_mask = trim_mask(sinister_mask, location)
    chief_section = FieldSection(chief_surface, chief_mask)
    dexter_section = FieldSection(dexter_surface, dexter_mask)
    sinister_section = FieldSection(sinister_surface, sinister_mask)
    return Device("", [chief_section, dexter_section, sinister_section])

def get_per_pall_reversed_field(tinctures, location):
    '''
    Returns a device with a per pall reversed field.
    tinctures: a list of exactly 3 tinctures,
     which will be used in the order [dexter, sinister, base].
    location: a Rect representing the location on the screen of the per pall reversed
      portion of the field. For a per pall reversed field on the full shield, 
      the Rect should be 
      Rect(kXMargin, kYMargin, kScreenWidth-2*kXMargin, kShieldBottom-kYMargin).
    '''
    if len(tinctures) != 3:
        print("A per pall reversed field must have exactly 3 tinctures.")
        return Device("")
    center = [location.centerx, int(location.top+location.height*0.5)]
    base_boundary = [[location.left, location.bottom], [location.right, location.bottom], center]
    dexter_boundary = [[location.left, location.bottom], [location.left, location.top],
                       [location.centerx, location.top], center]
    sinister_boundary = [[location.right, location.bottom], [location.right, location.top],
                         [location.centerx, location.top], center]
    size = (kScreenWidth, kScreenHeight)
    
    base_surface = pygame.Surface(size, 0, 32)
    base_surface.fill(tinctures[0])
    base_mask = pygame.Surface(size, 0, 32)
    pygame.draw.polygon(base_mask, kGrey, base_boundary)
    
    dexter_surface = pygame.Surface(size, 0, 32)
    dexter_surface.fill(tinctures[1])
    dexter_mask = pygame.Surface(size, 0, 32)
    pygame.draw.polygon(dexter_mask, kGrey, dexter_boundary)
    
    sinister_surface = pygame.Surface(size, 0, 32)
    sinister_surface.fill(tinctures[2])
    sinister_mask = pygame.Surface(size, 0, 32)
    pygame.draw.polygon(sinister_mask, kGrey, sinister_boundary)
    
    base_mask = trim_mask(base_mask, location)
    dexter_mask = trim_mask(dexter_mask, location)
    sinister_mask = trim_mask(sinister_mask, location)
    base_section = FieldSection(base_surface, base_mask)
    dexter_section = FieldSection(dexter_surface, dexter_mask)
    sinister_section = FieldSection(sinister_surface, sinister_mask)
    return Device("", [dexter_section, sinister_section, base_section])

def get_gyronny_field(num_sections, tinctures, location, horizontal=False):
    '''
    Returns a Device with a gyronny field of num_sections sections.
    num_sections: the number of sections. 6, 8, 10, and 12 are supported.
     4 is just quarterly or per saltire. 
    tinctures: A list of exactly two tinctures; the zeroth one 
     will be used in the dexter chief corner.
    location: a Rect representing the location on the screen of the gyronny
      portion of the field. For a gyronny field on the full shield, the Rect should be 
      Rect(kXMargin, kYMargin, kScreenWidth-2*kXMargin, kShieldBottom-kYMargin).
      If the gyronny field does not take up the whole shield, it will be a polygon with
      <num_sections> sides.
    horizontal: For gyronny of 6 or 10,
     if it is set to False, there will be a vertical line of division but no
     horizontal one. If it is set to True, there will be a horizontal line of division but no vertical one. 
     This variable has no effect on gyronny of 8 or 12 because they have both horizontal and vertical lines of division.
    '''
    if num_sections not in [6,8,10,12]:
        print("A gyronny field must have 6, 8, 10, or 12 sections.")
        return Device("")
    if len(tinctures) != 2:
        print("A gyronny field must have exactly 2 tinctures.")
        return Device("")
    
    center = [location.centerx, location.centery]
    arc_width_radians = 2*math.pi/num_sections
    if num_sections in (8, 12) or not horizontal:
        thetas = [i*arc_width_radians - math.pi*0.5 for i in range(num_sections)]
    else:
        thetas = [(i+0.5)*arc_width_radians - math.pi*0.5 for i in range(num_sections)]
    x_points = [max(location.width, location.height)*math.cos(theta) for theta in thetas]
    y_points = [max(location.width, location.height)*math.sin(theta) for theta in thetas]
    sections = []
    for i in range(num_sections):
        boundary = [center,
                    [int(x_points[i]+center[0]), int(y_points[i]+center[1])],
                    [int(x_points[(i+1) % num_sections]+center[0]),
                     int(y_points[(i+1) % num_sections]+center[1])]]
        size = (kScreenWidth, kScreenHeight)
        surface = pygame.Surface(size, 0, 32)
        surface.fill(tinctures[(i+1) % len(tinctures)])
        mask = pygame.Surface(size, 0, 32)
        pygame.draw.polygon(mask, kGrey, boundary)
        mask = trim_mask(mask, location)
        sections.append(FieldSection(surface, mask))
    return Device("", sections)

def get_checky_field(num_sections, tinctures, location):
    '''
    Returns a Device with a checky field.
    num_sections: the number of individual boxes across the top of the shield.
     This is distinct from the total number of boxes on the shield and may be less
     than the number of boxes in the longest vertical column.
    tinctures: A list of exactly two tinctures; the zeroth one 
     will be used in the dexter chief corner.
    location: a Rect representing the location on the screen of the lozengy
      portion of the field. For a lozengy field on the full shield, the Rect should be 
      Rect(kXMargin, kYMargin, kScreenWidth-2*kXMargin, kShieldBottom-kYMargin).
    '''
    if len(tinctures) != 2:
        print("A checky field must have exactly 2 tinctures.")
        return Device("")
    side_length = int(location.width/num_sections)
    if side_length < 30:
        print("Warning: that many sections won't work well on this size of screen. Consider using fewer.")
    sections = []
    cur_x = location.left
    cur_y = location.top
    cur_tincture = 0
    next_row_start_tincture = 1
    size = (kScreenWidth, kScreenHeight)
    tincture_0_surface = pygame.Surface(size, 0, 32)
    tincture_0_surface.fill(tinctures[0])
    tincture_1_surface = pygame.Surface(size, 0, 32)
    tincture_1_surface.fill(tinctures[1])
    tincture_0_mask = pygame.Surface(size, 0, 32)
    tincture_1_mask = pygame.Surface(size, 0, 32)
    while True:
        boundary = [[cur_x, cur_y], [cur_x, cur_y + side_length],
                    [cur_x + side_length, cur_y + side_length], [cur_x + side_length, cur_y]]
        if cur_tincture == 0:
            pygame.draw.polygon(tincture_0_mask, kGrey, boundary)
        else:
            pygame.draw.polygon(tincture_1_mask, kGrey, boundary)
        cur_x += side_length
        cur_tincture = (cur_tincture+1) % 2
        if cur_x > location.right + side_length:
            cur_x = location.left
            cur_y += side_length
            cur_tincture = next_row_start_tincture
            next_row_start_tincture = (next_row_start_tincture + 1) % 2
        if cur_y >= location.bottom:
            tincture_0_mask = trim_mask(tincture_0_mask, location)
            tincture_1_mask = trim_mask(tincture_1_mask, location)
            sections.append(FieldSection(tincture_0_surface, tincture_0_mask))
            sections.append(FieldSection(tincture_1_surface, tincture_1_mask))
            return Device("", sections)
            
def get_lozengy_field(num_sections, tinctures, location, proportion = 2):
    '''
    Returns a Device with a lozengy field.
    num_sections: the number of individual lozenges across the top of the field.
     This is distinct from the total number of lozenges on the field.
    tinctures: A list of exactly two tinctures; the zeroth one 
     will be used in the initial row of bottom-halves.
    location: a Rect representing the location on the screen of the lozengy
      portion of the field. For a lozengy field on the full shield, the Rect should be 
      Rect(kXMargin, kYMargin, kScreenWidth-2*kXMargin, kShieldBottom-kYMargin).
    proportion: the ratio of the lozenge height to the lozenge width. The default is 2,
     for lozenges twice as tall as they are wide. Proportions < 1 may not look very good.
    '''
    if len(tinctures) != 2:
        print("A lozengy field must have exactly 2 tinctures.")
        return Device("")
    size = (kScreenWidth, kScreenHeight)
    tincture_0_surface = pygame.Surface(size, 0, 32)
    tincture_0_surface.fill(tinctures[0])
    tincture_1_surface = pygame.Surface(size, 0, 32)
    tincture_1_surface.fill(tinctures[1])
    tincture_0_mask = pygame.Surface(size, 0, 32)
    tincture_1_mask = pygame.Surface(size, 0, 32)
    
    width = int((location.width)/num_sections)
    height = int(width * proportion)
    if width < 30 or height < 30:
        print("Warning: that many sections won't work well on this size of screen. Consider using fewer.")
    sections = []
    # [left, top, right, bottom]
    start_x_points = [location.left, location.left + int(width/2), location.left + width, location.left + int(width/2)]
    x_points = list(start_x_points)
    y_points =[location.top, location.top - int(height/2), location.top, location.top + int(height/2)]
    cur_tincture = 0
    while True:
        boundary = [[x_points[i], y_points[i]] for i in range(4)]
        if cur_tincture == 0:
            pygame.draw.polygon(tincture_0_mask, kGrey, boundary)
        else:
            pygame.draw.polygon(tincture_1_mask, kGrey, boundary)
        x_points = [x + width for x in x_points]
        if x_points[0] >= location.right:
            x_points = start_x_points
            # use the tincture to keep track of the offset between rows
            if cur_tincture == 0:
                x_points = [int(x - width/2) for x in x_points]
            y_points = [int(y + height/2) for y in y_points]
            cur_tincture = (cur_tincture + 1) % 2
            if y_points[1] >= location.bottom:
                sections.append(FieldSection(tincture_0_surface, tincture_0_mask))
                sections.append(FieldSection(tincture_1_surface, tincture_1_mask))
                return Device("", sections)
            
def get_fretty_field(num_sections, tinctures, location, outlines = False):
    '''
    Returns a Device with a fretty field.
    num_sections: the number of repeats across the top of the field.
    tinctures: A list of exactly two tinctures; the zeroth one 
     will be used in the initial row of bottom-halves.
    location: a Rect representing the location on the screen of the fretty
      portion of the field. For a fretty field on the full shield, the Rect should be 
      Rect(kXMargin, kYMargin, kScreenWidth-2*kXMargin, kShieldBottom-kYMargin).
    outlines: if True, each bendlet will have thin sable outlines in a "woven" pattern.
    '''
    if len(tinctures) != 2:
        print("A fretty field must have exactly 2 tinctures.")
        return Device("")
    size = (kScreenWidth, kScreenHeight)
    tincture_0_surface = pygame.Surface(size, 0, 32)
    tincture_0_surface.fill(tinctures[0])
    tincture_1_surface = pygame.Surface(size, 0, 32)
    tincture_1_surface.fill(tinctures[1])
    tincture_0_mask = pygame.Surface(size, 0, 32)
    tincture_1_mask = pygame.Surface(size, 0, 32)
    tincture_1_mask.fill(kGrey)
    # interval is the distance from the top of one square-between-frets
    # to the one directly left or right of it.
    interval = int(location.width/(num_sections))
    # 0.5 because each side is half the x-width of the square,
    # reduce to 0.3 to leave room for the frets
    side_offset = int(math.sqrt(2)*0.3*interval)
    # horizontal or vertical, not perpendicular, distance across a fret
    fret_width = int(interval-2*side_offset)
    vertical_offset = side_offset + int(fret_width/2)
    boundary = [[location.left + int(fret_width/2), location.top],
                [location.left + side_offset + int(fret_width/2), location.top - side_offset],
                [location.left + 2*side_offset + int(fret_width/2), location.top],
                [location.left + side_offset + int(fret_width/2), location.top + side_offset]]
    row_start_boundary = boundary
    if outlines:
        width = 5
        extension_length = math.ceil(int(fret_width/2))
        extend_deasil = True
        sinister_chief_deasil = [[location.left+int(fret_width/2), location.top],
                                 [location.left+int(fret_width/2)+side_offset+extension_length,
                                  location.top-side_offset-extension_length]]
        sinister_base_deasil = [[location.left+side_offset+int(fret_width/2),
                                 location.top-side_offset],
                                [location.left+2*side_offset+int(fret_width/2)+extension_length,
                                 location.top+extension_length]]
        dexter_base_deasil = [[location.left+2*side_offset+int(fret_width/2),
                               location.top],
                              [location.left+side_offset+int(fret_width/2)-extension_length,
                               location.top+side_offset+extension_length]]
        dexter_chief_deasil = [[location.left+side_offset+int(fret_width/2),
                                location.top+side_offset],
                               [location.left+int(fret_width/2)-extension_length,
                                location.top-extension_length]]
        outline_points_deasil = [sinister_chief_deasil, sinister_base_deasil,
                                 dexter_base_deasil, dexter_chief_deasil]
        dexter_chief_widdershins = [[location.left-side_offset-extension_length,
                                       location.top+extension_length],
                                      [location.left,
                                       location.top-side_offset]]
        sinister_chief_widdershins = [[location.left-extension_length,
                                      location.top-side_offset-extension_length],
                                     [location.left+side_offset,
                                      location.top]]
        sinister_base_widdershins = [[location.left+side_offset+extension_length,
                                    location.top-extension_length],
                                   [location.left,
                                    location.top+side_offset]]
        dexter_base_widdershins = [[location.left+extension_length,
                                     location.top+side_offset+extension_length],
                                    [location.left-side_offset,
                                     location.top]]
        outline_points_widdershins = [sinister_chief_widdershins, sinister_base_widdershins,
                                      dexter_base_widdershins, dexter_chief_widdershins]
        # Separate lists so they can be modified separately
        row_start_sinister_chief_deasil = [list(point) for point in sinister_chief_deasil]
        row_start_sinister_base_deasil = [list(point) for point in sinister_base_deasil]
        row_start_dexter_chief_deasil = [list(point) for point in dexter_chief_deasil]
        row_start_dexter_base_deasil = [list(point) for point in dexter_base_deasil]
        row_start_outline_points_deasil = [row_start_sinister_chief_deasil,
                                           row_start_sinister_base_deasil,
                                           row_start_dexter_base_deasil,
                                           row_start_dexter_chief_deasil]
        row_start_sinister_chief_widdershins = [list(point) for point in sinister_chief_widdershins]
        row_start_sinister_base_widdershins = [list(point) for point in sinister_base_widdershins]
        row_start_dexter_chief_widdershins = [list(point) for point in dexter_chief_widdershins]
        row_start_dexter_base_widdershins = [list(point) for point in dexter_base_widdershins]
        row_start_outline_points_widdershins = [row_start_sinister_chief_widdershins,
                                                row_start_sinister_base_widdershins,
                                                row_start_dexter_base_widdershins,
                                                row_start_dexter_chief_widdershins]
    while boundary[1][1] <= location.bottom:
        if outlines:
            if extend_deasil:
                outline_points = list(outline_points_deasil)
                extend_deasil = False
            else:
                outline_points = list(outline_points_widdershins)
                extend_deasil = True
        while boundary[3][0] <= location.right:
            pygame.draw.polygon(tincture_0_mask, kGrey, boundary)
            # Move the square to the right
            boundary = [[i[0] + interval, i[1]] for i in boundary]
            if outlines:
                for line in outline_points:
                    # Put the lines on both so they mesh nicely
                    pygame.draw.line(tincture_0_surface, kSable, line[0], line[1], width)
                    pygame.draw.line(tincture_1_surface, kSable, line[0], line[1], width)
                    # Move the lines to the right
                    line[0][0] += interval
                    line[1][0] += interval
        # Move the square back to the left edge
        for i in range(len(boundary)):
            boundary[i][0] = row_start_boundary[i][0]
        # Offset each row by interval/2 from the previous
        boundary = [[i[0] - int(interval/2), i[1]] for i in boundary]
        # Move the square down
        boundary = [[i[0], i[1] + vertical_offset] for i in boundary]
        row_start_boundary = boundary
        if outlines:
            # Move the outlines back to the left edge
            for i in range(4):
                outline_points_deasil[i][0][0] = int(row_start_outline_points_deasil[i][0][0])
                outline_points_deasil[i][1][0] = int(row_start_outline_points_deasil[i][1][0])
                outline_points_widdershins[i][0][0] = int(row_start_outline_points_widdershins[i][0][0])
                outline_points_widdershins[i][1][0] = int(row_start_outline_points_widdershins[i][1][0])
            for line in outline_points_deasil:
                for point in line:
                    # Move the outlines down
                    point[1] += vertical_offset
            for line in outline_points_widdershins:
                for point in line:
                    # Move the outlines down
                    point[1] += vertical_offset
            row_start_sinister_chief_deasil = [list(point) for point in sinister_chief_deasil]
            row_start_sinister_base_deasil = [list(point) for point in sinister_base_deasil]
            row_start_dexter_chief_deasil = [list(point) for point in dexter_chief_deasil]
            row_start_dexter_base_deasil = [list(point) for point in dexter_base_deasil]
            row_start_outline_points_deasil = [row_start_sinister_chief_deasil,
                                               row_start_sinister_base_deasil,
                                               row_start_dexter_base_deasil,
                                               row_start_dexter_chief_deasil]
            row_start_sinister_chief_widdershins = [list(point) for point in sinister_chief_widdershins]
            row_start_sinister_base_widdershins = [list(point) for point in sinister_base_widdershins]
            row_start_dexter_chief_widdershins = [list(point) for point in dexter_chief_widdershins]
            row_start_dexter_base_widdershins = [list(point) for point in dexter_base_widdershins]
            row_start_outline_points_widdershins = [row_start_sinister_chief_widdershins,
                                                    row_start_sinister_base_widdershins,
                                                    row_start_dexter_base_widdershins,
                                                    row_start_dexter_chief_widdershins]
                

    # Reverse order because the frets are actually being modeled as the negative space
    # and the squares between them as the positive space.
    tincture_0_mask = trim_mask(tincture_0_mask, location)
    tincture_1_mask = trim_mask(tincture_1_mask, location)
    sections = [FieldSection(tincture_1_surface, tincture_1_mask),
                FieldSection(tincture_0_surface, tincture_0_mask)]
    return Device("", sections)
            
def get_scaly_field(num_sections, tinctures, location):
    '''
    Returns a Device with a scaly field.
    num_sections: the number of repeats across the top of the field.
    tinctures: A list of exactly two tinctures; the zeroth one 
     will be used for the background and the second for the arcs.
    location: a Rect representing the location on the screen of the scaly
      portion of the field. For a scaly field on the full shield, the Rect should be 
      Rect(kXMargin, kYMargin, kScreenWidth-2*kXMargin, kShieldBottom-kYMargin).
    '''
    if len(tinctures) != 2:
        print("A scalyk field must have exactly 2 tinctures.")
        return Device("")
    size = (kScreenWidth, kScreenHeight)
    surface = pygame.Surface(size, 0, 32)
    mask = pygame.Surface(size, 0, 32)
    # no masking, just exploit blit order on the surface
    # to get out of cutting off the arcs at the right place
    pygame.draw.polygon(mask, kGrey, [(location.left, location.top),
                                      (location.left, location.bottom),
                                      (location.right, location.bottom),
                                      (location.right, location.top)])
    radius = int(location.width/num_sections/2)
    # go from base to chief so chief scales are "on top of" base scales
    center = [location.left, location.bottom]
    offset_next_row = True
    while center[1] >= location.top-radius:
        while center[0] <= location.right:
            pygame.draw.circle(surface, tinctures[0], center, radius)
            # 2 is the width of the unfilled circular arc
            pygame.draw.circle(surface, tinctures[1], center, radius, 2)
            center[0] += radius*2
        center[0] = location.left
        if offset_next_row:
            center[0] += radius
        offset_next_row = not offset_next_row
        center[1] -= radius
    # no need to trim the mask, since we're not blitting
    # anything other than the location Rect on it
    sections = [FieldSection(surface, mask)]
    return Device("", sections)

def get_masoned_field(num_sections_x, num_sections_y, tinctures, location,
                      line_width = 5):
    '''
    Returns a Device with a masoned field.
    num_sections_x: the number of "bricks" in each row.
    num_sections_y: the number of rows.
    tinctures: A list of exactly two tinctures; the zeroth one 
     will be used for the "bricks" and the second for the "mortar".
    location: a Rect representing the location on the screen of the masoned
      portion of the field. For a masoned field on the full shield, the Rect should be 
      Rect(kXMargin, kYMargin, kScreenWidth-2*kXMargin, kShieldBottom-kYMargin).
    line_width: the width of the "mortar" lines in pixels. Optional.
    '''
    if len(tinctures) != 2:
        print("A masoned field must have exactly 2 tinctures.")
        return Device("")
    size = (kScreenWidth, kScreenHeight)
    surface = pygame.Surface(size, 0, 32)
    surface.fill(tinctures[0])
    mask = pygame.Surface(size, 0, 32)
    # no complicated masking, just stick everything on the surface
    # and use the mask to trim to the location area
    pygame.draw.polygon(mask, kGrey, [(location.left, location.top),
                                      (location.left, location.bottom),
                                      (location.right, location.bottom),
                                      (location.right, location.top)])
    x_interval = int(location.width/num_sections_x)
    y_interval = int(location.height/num_sections_y)
    x = location.left
    y_top = location.top
    offset_next_row = True
    while y_top <= location.bottom:
        while x <= location.right:
            pygame.draw.line(surface, tinctures[1], (x, y_top),
                             (x, y_top + y_interval), line_width)
            x += x_interval
        pygame.draw.line(surface, tinctures[1], (location.left, y_top),
                         (location.right, y_top), line_width)
        y_top += y_interval
        x = location.left
        if offset_next_row:
            x += int(x_interval/2)
        offset_next_row = not offset_next_row
    # no need to trim the mask, since we're not blitting
    # anything other than the location Rect on it
    sections = [FieldSection(surface, mask)]
    return Device("", sections)

def get_party_of_six_field(tinctures, location):
    '''
    Returns a Device with a party of 6 field.
    tinctures: A list of exactly two tinctures; the zeroth one 
     will be used for the dexter chief corner.
    location: a Rect representing the location on the screen of the party of 6
      portion of the field. For a party of 6 field on the full shield, the Rect should be 
      Rect(kXMargin, kYMargin, kScreenWidth-2*kXMargin, kShieldBottom-kYMargin).
    '''
    if len(tinctures) != 2:
        print("A party of 6 field must have exactly 2 tinctures.")
        return Device("")
    size = (kScreenWidth, kScreenHeight)
    surface = pygame.Surface(size, 0, 32)
    mask = pygame.Surface(size, 0, 32)
    # no complicated masking, just stick everything on the surface
    # and use the mask to trim to the location area
    one_third_x = location.left + int(location.width/3)
    two_thirds_x = location.left + int(2*location.width/3)
    half_y = location.top + int(location.height/2)
    pygame.draw.polygon(surface, tinctures[0], [(location.left, location.top),
                                      (location.left, half_y),
                                      (one_third_x, half_y),
                                      (one_third_x, location.top)])
    pygame.draw.polygon(surface, tinctures[1], [(location.left, half_y),
                                      (location.left, location.bottom),
                                      (one_third_x, location.bottom),
                                      (one_third_x, half_y)])
    pygame.draw.polygon(surface, tinctures[1], [(one_third_x, location.top),
                                      (one_third_x, half_y),
                                      (two_thirds_x, half_y),
                                      (two_thirds_x, location.top)])
    pygame.draw.polygon(surface, tinctures[0], [(one_third_x, half_y),
                                      (one_third_x, location.bottom),
                                      (two_thirds_x, location.bottom),
                                      (two_thirds_x, half_y)])
    pygame.draw.polygon(surface, tinctures[0], [(two_thirds_x, location.top),
                                      (two_thirds_x, half_y),
                                      (location.right, half_y),
                                      (location.right, location.top)])
    pygame.draw.polygon(surface, tinctures[1], [(two_thirds_x, half_y),
                                      (two_thirds_x, location.bottom),
                                      (location.right, location.bottom),
                                      (location.right, half_y)])
    
    pygame.draw.polygon(mask, kGrey, [(location.left, location.top),
                                      (location.left, location.bottom),
                                      (location.right, location.bottom),
                                      (location.right, location.top)])
    # no need to trim the mask, since we're not blitting
    # anything other than the location Rect on it
    sections = [FieldSection(surface, mask)]
    return Device("", sections)

import math
from device_generator import *
constant_definitions =open("constants.py")
exec(constant_definitions.read())

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
    return FieldSection(surface, mask)

def get_paly_boundaries(n, location):
    '''
    Returns a list of lists of lists which is the boundary boxes 
      for a paly of n field.
    n: the number of stripes. Use 2 for per pale.
    location: a Rect representing the location on the screen of the paly portion of the field.
      If the paly field should fill the entire shield, the Rect should be 
      Rect(kXMargin, kYMargin, kScreenWidth-2*kXMargin, kShieldBottom-kYMargin).
    '''
    boundaries = []
    for i in range(n):
        left_edge = int(location.left + location.width*i/n)
        right_edge = int(location.left + location.width*(i+1)/n)
        boundaries.append(
            [[left_edge, location.top], [left_edge, location.bottom],
             [right_edge, location.bottom], [right_edge, location.top]])
    return boundaries

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
    for i in range(n):
        top_edge = int(location.top + location.height*i/n)
        bottom_edge = int(location.top + location.height*(i+1)/n)
        boundaries.append(
            [[location.left, top_edge], [location.right, top_edge],
             [location.right, bottom_edge], [location.left, bottom_edge]])
    return boundaries

def get_bendy_boundaries(n, location):
    '''
    Returns a list of lists of lists which is the boundary boxes 
      for a bendy of n field.
    n: the number of sections. Use 2 for per bend sinister.
    location: a Rect representing the location on the screen of the bendy portion of the field.
     If the bendy field should fill the entire shield, the Rect should be 
     Rect(kXMargin, kYMargin, kScreenWidth-2*kXMargin, kShieldBottom-kYMargin).
    '''
    boundaries = []
    for i in range(n):
        # multiply by 2 because you need a 2x rectangle to get
        # every stripe from top to left. This will produce some
        # boundaries that go outside the location rect, but get_striped_field
        # will trim them later.
        dexter_chief = location.right - int(location.width*i*2/n)
        sinister_chief = location.right - int(location.width*(i+1)*2/n)
        dexter_base = location.top + int(location.height*(i)*2/n)
        sinister_base = location.top + int(location.height*(i+1)*2/n)
        boundaries.append(
            [[dexter_chief, location.top],
             [sinister_chief, location.top],
             [location.right, sinister_base], [location.right, dexter_base]])
    return boundaries

def get_bendy_sinister_boundaries(n, location):
    '''
    Returns a list of lists of lists which is the boundary boxes 
      for a bendy sinister of n field.
    n: the number of sections. Use 2 for per bend.
    location: a Rect representing the location on the screen of the 
      bendy sinister portion of the field.
      If the bendy sinister field should fill the entire shield, the Rect should be 
      Rect(kXMargin, kYMargin, kScreenWidth-2*kXMargin, kShieldBottom-kYMargin).
    '''
    boundaries = []
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
    return boundaries

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

def get_striped_field(num_sections, tinctures, direction, location):
    '''
    Returns a list of FieldSection objects representing a portion of the field 
      with one or more parallel lines of division.
    num_sections: the number of sections.
    tinctures: a list of tincture objects, e.g. [kVert, kArgent], dexter chief first.
    direction: a string indicating direction.
      Must be one of the keys in the dict below.
    location: a Rect representing the location on the screen of the striped portion of the field.
      If the striped field should fill the entire shield, the Rect should be 
      Rect(kXMargin, kYMargin, kScreenWidth-2*kXMargin, kShieldBottom-kYMargin).
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
    fieldsections = []
    boundaries = directions[direction](num_sections, location)
    for i in range(num_sections):
        size = (kScreenWidth, kScreenHeight)
        surface = pygame.Surface(size, 0, 32)
        surface.fill(tinctures[i % len(tinctures)])
        mask = pygame.Surface(size, 0, 32)
        # If the stripes would extend outside the location rect,
        # don't let them
        mask.set_clip(location)
        pygame.draw.polygon(mask, kGrey, boundaries[i])
        fieldsections.append(FieldSection(surface, mask))
    return fieldsections

# CURRENTLY BROKEN
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
        field_sections.append(FieldSection(surface, mask))
    return Device("", field_sections)

def get_per_saltire_field(tinctures, location):
    '''
    Returns a device object with a per saltire field.
    tinctures: a list of exactly two or four tinctures. Two is recommended.
      If two, the chief and base sections are the 0th tincture and the
      dexter and sinister sections are the 1st tincture.
      If four, the tinctures are used anticlockwise from chief:
      [chief, dexter, base, sinister].
    location: a Rect representing the location on the screen of the per saltire 
      portion of the field. If the per saltire field should fill the entire shield, 
      the Rect should be 
      Rect(kXMargin, kYMargin, kScreenWidth-2*kXMargin, kShieldBottom-kYMargin).
    '''
    if len(tinctures) != 2 and len(tinctures) != 4:
        print("Quarterly fields can't have", len(tinctures), "tinctures")
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
    chief_section = FieldSection(chief_surface, chief_mask)
    
    base_surface = pygame.Surface(size, 0, 32)
    base_surface.fill(tinctures[1])
    base_mask = pygame.Surface(size, 0, 32)
    pygame.draw.polygon(base_mask, kGrey, base_boundary)
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
    chief_section = FieldSection(chief_surface, chief_mask)
    
    base_surface = pygame.Surface(size, 0, 32)
    base_surface.fill(tinctures[1])
    base_mask = pygame.Surface(size, 0, 32)
    pygame.draw.polygon(base_mask, kGrey, base_boundary)
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
    outer_section = FieldSection(outer_surface, outer_mask)
    
    inner_surface = pygame.Surface(size, 0, 32)
    inner_surface.fill(tinctures[1])
    inner_mask = pygame.Surface(size, 0, 32)
    pygame.draw.polygon(inner_mask, kGrey, inner_boundary)
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
    outer_section = FieldSection(outer_surface, outer_mask)

    inner_surface = pygame.Surface(size, 0, 32)
    inner_surface.fill(tinctures[1])
    inner_mask = pygame.Surface(size, 0, 32)
    inner_mask.fill(kGrey)
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
      portion of the field. For a vetu ploye field on the full shield, the Rect should be 
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
      portion of the field. For a vetu ploye field on the full shield, the Rect should be 
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
    
    base_section = FieldSection(base_surface, base_mask)
    dexter_section = FieldSection(dexter_surface, dexter_mask)
    sinister_section = FieldSection(sinister_surface, sinister_mask)
    return Device("", [dexter_section, sinister_section, base_section])

def get_gyronny_field(num_sections, tinctures, horizontal=False):
    '''
    Returns a Device with a gyronny field of num_sections sections.
    num_sections: the number of sections. 6, 8, 10, and 12 are supported.
     4 is just quarterly or per saltire. 
    tinctures: A list of exactly two tinctures; the first one 
     will be used in the dexter chief corner.
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
    
    center = [int(kScreenWidth/2), int(kScreenHeight*0.4)]
    arc_width_radians = 2*math.pi/num_sections
    if num_sections in (8, 12) or not horizontal:
        thetas = [i*arc_width_radians - math.pi*0.5 for i in range(num_sections)]
    else:
        thetas = [(i+0.5)*arc_width_radians - math.pi*0.5 for i in range(num_sections)]
    x_points = [max(kScreenWidth, kScreenHeight)*math.cos(theta) for theta in thetas]
    y_points = [max(kScreenWidth, kScreenHeight)*math.sin(theta) for theta in thetas]
    sections = []
    for i in range(num_sections):
        boundary = [center,
                    [int(x_points[i]+center[0]), int(y_points[i]+center[1])],
                    [int(x_points[(i+1) % num_sections]+center[0]),
                     int(y_points[(i+1) % num_sections]+center[1])]]
        sections.append(FieldSection(boundary, tincture=tinctures[(i+1) % len(tinctures)]))
    return Device("", sections)

def get_checky_field(num_sections, tinctures):
    '''
    Returns a Device with a checky field.
    num_sections: the number of individual boxes across the top of the shield.
     This is distinct from the total number of boxes on the shield and may be less
     than the number of boxes in the longest vertical column.
    tinctures: A list of exactly two tinctures; the first one 
     will be used in the dexter chief corner.
    '''
    if len(tinctures) != 2:
        print("A checky field must have exactly 2 tinctures.")
        return Device("")
    side_length = int((kScreenWidth-2*kXMargin)/num_sections)
    if side_length < 30:
        print("Warning: that many sections won't work well on this size of screen. Consider using fewer.")
    sections = []
    cur_x = kXMargin
    cur_y = kYMargin
    cur_tincture = 0
    next_row_start_tincture = 1
    while True:
        boundary = [[cur_x, cur_y], [cur_x, cur_y + side_length],
                    [cur_x + side_length, cur_y + side_length], [cur_x + side_length, cur_y]]
        sections.append(FieldSection(boundary, tincture=tinctures[cur_tincture]))
        cur_x += side_length
        cur_tincture = (cur_tincture+1) % 2
        if cur_x > kScreenWidth - kXMargin + side_length:
            cur_x = kXMargin
            cur_y += side_length
            cur_tincture = next_row_start_tincture
            next_row_start_tincture = (next_row_start_tincture + 1) % 2
        if cur_y >= kScreenHeight:
            return Device("", sections)
            
def get_lozengy_field(num_sections, tinctures, proportion = 2):
    '''
    Returns a Device with a lozengy field.
    num_sections: the number of individual lozenges across the top of the shield.
     This is distinct from the total number of lozenges on the shield,
    tinctures: A list of exactly two tinctures; the first one 
     will be used in the initial row of bottom-halves.
    proportion: the ratio of the lozenge height to the lozenge width. The default is 2,
     for lozenges twice as tall as they are wide. Proportions < 1 may not look very good.
    '''
    if len(tinctures) != 2:
        print("A lozengy field must have exactly 2 tinctures.")
        return Device("")
    width = int((kScreenWidth-2*kXMargin)/num_sections)
    height = int(width * proportion)
    if width < 30 or height < 30:
        print("Warning: that many sections won't work well on this size of screen. Consider using fewer.")
    sections = []
    # [left, top, right, bottom]
    start_x_points = [kXMargin, kXMargin + int(width/2), kXMargin + width, kXMargin + int(width/2)]
    x_points = list(start_x_points)
    y_points =[kYMargin, kYMargin - int(height/2), kYMargin, kYMargin + int(height/2)]
    cur_tincture = 0
    while True:
        boundary = [[x_points[i], y_points[i]] for i in range(4)]
        sections.append(FieldSection(boundary, tincture=tinctures[cur_tincture]))
        x_points = [x + width for x in x_points]
        if x_points[0] >= (kScreenWidth - kXMargin):
            x_points = start_x_points
            # use the tincture to keep track of the offset between rows
            if cur_tincture == 0:
                x_points = [int(x - width/2) for x in x_points]
            y_points = [int(y + height/2) for y in y_points]
            cur_tincture = (cur_tincture + 1) % 2
            if y_points[1] >= kScreenHeight:
                return Device("", sections)

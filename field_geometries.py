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
     Rect(kXMargin, kYMargin, kScreenWidth, kScreenHeight).
    '''
    boundary = [[location.left, location.top], [location.left, location.bottom],
                [location.right, location.bottom], [location.right, location.top]]
    return FieldSection(boundary, tincture = tincture)

def get_paly_boundaries(num_sections, location):
    '''
    Returns a list of lists of lists which is the boundary boxes 
      for a paly of n field.
    num_sections: the number of sections. Use 2 for per pale.
    location: a Rect representing the location on the screen of the paly portion of the field.
     If the paly field should fill the entire shield, the Rect should be 
     Rect(kXMargin, kYMargin, kScreenWidth, kScreenHeight).
    '''
    #TODO start here, replace constants with left/right/top/bottom/etc
    boundary_sections = []
    for i in range(num_sections):
        left_edge = int(kScreenWidth*i/num_sections)
        right_edge = int(kScreenWidth*(i+1)/num_sections)
        boundary_sections.append(
            [[left_edge, 0], [left_edge, kScreenHeight],
             [right_edge, kScreenHeight], [right_edge, 0]])
    return boundary_sections

def get_barry_boundaries(n):
    '''
    Returns a list of lists of lists which is the boundary boxes 
      for a barry of n field.
    n: the number of sections. Use 2 for per fess.
    '''
    boundary_sections = []
    for i in range(n):
        # fudge factor because the bottom margin is so large
        # +kMargin means the first tincture will always be visible first
        fudge_factor = 0.85
        top_edge = int(kScreenHeight*i/n*fudge_factor+kYMargin) 
        bottom_edge = int(kScreenHeight*(i+1)/n*fudge_factor+kYMargin)
        boundary_sections.append(
            [[0, top_edge], [kScreenWidth, top_edge],
             [kScreenWidth, bottom_edge], [0, bottom_edge]])
    return boundary_sections

def get_bendy_boundaries(n):
    '''
    Returns a list of lists of lists which is the boundary boxes 
      for a bendy of n field.
    n: the number of sections. Use 2 for per bend sinister.
    '''
    boundary_sections = []
    fudge_factor = 1.95 #hack to handle margins
    for i in range(n):
        dexter_chief = int(kScreenWidth*i*fudge_factor/n)
        sinister_chief = int(kScreenWidth*(i+1)*fudge_factor/n)
        dexter_base = int(kScreenHeight*(i)*fudge_factor/n)
        sinister_base = int(kScreenHeight*(i+1)*fudge_factor/n)
        boundary_sections.append(
            [[kScreenWidth-dexter_chief, 0], [kScreenWidth-sinister_chief, 0],
             [kScreenWidth, sinister_base], [kScreenWidth, dexter_base]])
    return boundary_sections

def get_bendy_sinister_boundaries(n):
    '''
    Returns a list of lists of lists which is the boundary boxes 
      for a bendy sinister of n field.
    n: the number of sections. Use 2 for per bend.
    '''
    boundary_sections = []
    fudge_factor = 1.95 #hack to handle margins
    for i in range(n):
        dexter_chief = int(kScreenWidth*i*fudge_factor/n)
        sinister_chief = int(kScreenWidth*(i+1)*fudge_factor/n)
        dexter_base = int(kScreenHeight*(i)*fudge_factor/n)
        sinister_base = int(kScreenHeight*(i+1)*fudge_factor/n)
        boundary_sections.append(
            [[dexter_chief, 0], [sinister_chief, 0],
             [0, sinister_base], [0, dexter_base]])
    return boundary_sections

def get_chevronelly_boundaries(n):
    '''
    Returns a list of lists of lists which is the boundary boxes 
      for a chevronelly of n field.
    n: the number of sections. Use 2 for per chevron.
    '''
    boundary_sections = []
    y_offset = int(kScreenHeight/8)
    for i in range(n):
        boundary_sections.append([[0, kScreenHeight*i/n],
                                  [kScreenWidth/2, kScreenHeight*i/n-y_offset],
                                  [kScreenWidth, kScreenHeight*i/n],
                                  [kScreenWidth, kScreenHeight*(i+1)/n],
                                  [kScreenWidth/2, kScreenHeight*(i+1)/n-y_offset],
                                  [0, kScreenHeight*(i+1)/n]])
    return boundary_sections

def get_chevronelly_inverted_boundaries(n):
    '''
    Returns a list of lists of lists which is the boundary boxes 
      for a chevronelly inverted of n field.
    n: the number of sections. Use 2 for per chevron.
    '''
    boundary_sections = []
    y_offset = int(kScreenHeight/10)
    for i in range(n):
        boundary_sections.append([[0, kScreenHeight*i/n-y_offset],
                                  [kScreenWidth/2, kScreenHeight*i/n],
                                  [kScreenWidth, kScreenHeight*i/n-y_offset],
                                  [kScreenWidth, kScreenHeight*(i+1)/n-y_offset],
                                  [kScreenWidth/2, kScreenHeight*(i+1)/n],
                                  [0, kScreenHeight*(i+1)/n-y_offset]])
    return boundary_sections

def get_striped_field(num_sections, tinctures, direction):
    '''
    Returns a Device object with a field whose lines of division 
      all go a single direction.
    num_sections: the number of sections.
    tinctures: a list of tincture objects, e.g. [kVert, kArgent], dexter chief first.
    direction: a string indicating direction.
      Must be one of the keys in the dict below.
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
    boundaries = directions[direction](num_sections)
    for i in range(num_sections):
        fieldsections.append(FieldSection(boundaries[i],
                                          tincture = tinctures[i % len(tinctures)]))
    return Device("", fieldsections)

def get_quarterly_field(tinctures):
    '''
    Returns a device object with a quarterly field.
    tinctures: a list of exactly two or four tinctures. Two is recommended.
      If two, the dexter chief and sinister base quarters are the 0th tincture,
      and the sinister chief and dexter base quarters are the 1st tincture.
      If four, the tinctures are used in the order
      [dexter chief, sinister chief, sinister base, dexter base].
    '''
    if len(tinctures) != 2 and len(tinctures) != 4:
        print("Quarterly fields can't have", len(tinctures), "tinctures")
        return Device("")
    dexter_chief_quarter = [[0, 0],
                            [0, int(kScreenHeight*5/12)],
                            [int(kScreenWidth/2), int(kScreenHeight*5/12)],
                            [int(kScreenWidth/2), 0]]
    sinister_chief_quarter = [[int(kScreenWidth/2), 0],
                              [int(kScreenWidth/2), int(kScreenHeight*5/12)],
                              [kScreenWidth, int(kScreenHeight*5/12)],
                              [kScreenWidth, 0]]
    sinister_base_quarter = [[int(kScreenWidth/2), int(kScreenHeight*5/12)],
                             [int(kScreenWidth/2), kScreenHeight],
                             [kScreenWidth, kScreenHeight],
                             [kScreenWidth, int(kScreenHeight*5/12)]]
    dexter_base_quarter = [[0, int(kScreenHeight*5/12)],
                           [0, kScreenHeight],
                           [int(kScreenWidth/2), kScreenHeight],
                           [int(kScreenWidth/2), int(kScreenHeight*5/12)]]
    dexter_chief_section = FieldSection(dexter_chief_quarter, tincture = tinctures[0])
    sinister_chief_section = FieldSection(sinister_chief_quarter, tincture = tinctures[1])
    sinister_base_section = FieldSection(sinister_base_quarter,
                                         tincture = tinctures[2 % len(tinctures)])
    dexter_base_section = FieldSection(dexter_base_quarter,
                                       tincture = tinctures[3 % len(tinctures)])
    return Device("", [dexter_chief_section, sinister_chief_section,
                       dexter_base_section, sinister_base_section])

def get_per_saltire_field(tinctures):
    '''
    Returns a device object with a per saltire field.
    tinctures: a list of exactly two or four tinctures. Two is recommended.
      If two, the chief and base sections are the 0th tincture and the
      dexter and sinister sections are the 1st tincture.
      If four, the tinctures are used anticlockwise from chief:
      [chief, dexter, base, sinister].
    '''
    if len(tinctures) != 2 and len(tinctures) != 4:
        print("Quarterly fields can't have", len(tinctures), "tinctures")
        return Device("")
    chief_saltire_boundary = [[int(kScreenWidth*.03), 0],
                              [int(kScreenWidth/2), int(kScreenHeight*5/12)],
                              [int(kScreenWidth*.97), 0]]
    dexter_saltire_boundary = [[int(kScreenWidth*.03), 0],
                               [int(kScreenWidth/2), int(kScreenHeight*5/12)],
                               [int(kScreenWidth*.03), int(kScreenHeight*10/12)]]
    # There are four points here. Don't mess with this
    # without looking at it really carefully first.
    base_saltire_boundary = [[int(kScreenWidth*.03), int(kScreenHeight*10/12)],
                             [int(kScreenWidth/2), int(kScreenHeight*5/12)],
                             [int(kScreenWidth*.97), int(kScreenHeight*10/12)],
                             [int(kScreenWidth/2), kScreenHeight]]
    sinister_saltire_boundary = [[int(kScreenWidth*.97), 0],
                                 [int(kScreenWidth/2), int(kScreenHeight*5/12)],
                                 [int(kScreenWidth*.97), int(kScreenHeight*10/12)]]
    chief_saltire_section = FieldSection(chief_saltire_boundary, tincture = tinctures[0])
    dexter_saltire_section = FieldSection(dexter_saltire_boundary, tincture = tinctures[1])
    base_saltire_section = FieldSection(base_saltire_boundary,
                                        tincture = tinctures[2 % len(tinctures)])
    sinister_saltire_section = FieldSection(sinister_saltire_boundary,
                                            tincture = tinctures[3 % len(tinctures)])
    return Device("", [chief_saltire_section, dexter_saltire_section,
                       base_saltire_section, sinister_saltire_section])

def get_per_chevron_throughout_field(tinctures):
    '''
    Returns a Device with a per chevron throughout field.
    tinctures: a list of exactly two tinctures.
      The outer sections are the 0th tincture and the inner section
      is the 1st tincture.
    '''
    if len(tinctures) != 2:
        print ("A per chevron throughout field must have exactly two tinctures.")
        return Device("")
    chief_boundary = [[0,0], [0, kScreenHeight], [int(kScreenWidth/2), kYMargin],
                             [kScreenWidth, kScreenHeight], [kScreenWidth, 0]]
    base_boundary = [[0, kScreenHeight], [int(kScreenWidth/2), kYMargin],
                     [kScreenWidth, kScreenHeight]]
    chief_section = FieldSection(chief_boundary, tincture = tinctures[0])
    base_section = FieldSection(base_boundary, tincture = tinctures[1])
    return Device("", [chief_section, base_section])
    
def get_per_chevron_inverted_throughout_field(tinctures):
    '''
    Returns a Device with a per chevron inverted throughout field.
    tinctures: a list of exactly two tinctures.
      The middle section is the 0th tincture and the outer sections
      are the 1st tincture.
    '''
    x_margin = int(kScreenWidth/22)
    if len(tinctures) != 2:
        print ("A per chevron inverted throughout field must have exactly two tinctures.")
        return Device("")
    base_boundary = [[x_margin,0], [x_margin, kScreenHeight],
                     [kScreenWidth-x_margin, kScreenHeight], [kScreenWidth-x_margin, 0],
                     [int(kScreenWidth/2),  int(kScreenHeight*0.87)]]
    chief_boundary = [[x_margin, 0], [int(kScreenWidth/2), int(kScreenHeight*0.87)],
                     [kScreenWidth-x_margin, 0]]
    chief_section = FieldSection(chief_boundary, tincture = tinctures[0])
    base_section = FieldSection(base_boundary, tincture = tinctures[1])
    return Device("", [chief_section, base_section])

def get_vetu_field(tinctures):
    '''
    Returns a Device with a vetu field.
    tinctures: a list of exactly two tinctures.
      The outer sections are the 0th tincture, and the inner
      lozenge is the 1st tincture.
   '''
    x_margin = 75
    y_margin = int(kScreenHeight/23)
    shield_bottom = int(kScreenHeight*0.87)
    y_midpoint = int((y_margin + shield_bottom)/2)
    if len(tinctures) != 2:
        print ("A vetu field must have exactly two tinctures.")
        return Device("")
    # Just do the whole field in the outer tincture
    # and then stick the lozenge on top of it.
    outer_boundary = [[0, 0], [0, kScreenHeight],
                     [kScreenWidth, kScreenHeight], [kScreenWidth, 0]]
    inner_boundary = [[int(kScreenWidth/2), y_margin],
                      [kScreenWidth-x_margin, y_midpoint],
                      [int(kScreenWidth/2), shield_bottom],
                      [x_margin, y_midpoint]]
    outer_section = FieldSection(outer_boundary, tincture = tinctures[0])
    inner_section = FieldSection(inner_boundary, tincture = tinctures[1])
    return Device("", [outer_section, inner_section])

def get_vetu_ploye_field(tinctures):
    '''
    Returns a Device with a vetu ploye field.
    tinctures: a list of exactly two tinctures.
      The outer sections are the 0th tincture, and the inner
      lozenge is the 1st tincture.
   '''
    x_margin = 75
    y_margin = int(kScreenHeight/23)
    shield_bottom = int(kScreenHeight*0.87)
    y_midpoint = int((y_margin + shield_bottom)/2)
    y_fudge_factor = 7
    if len(tinctures) != 2:
        print ("A vetu ploye field must have exactly two tinctures.")
        return Device("")
    # Just do the whole field in the inner tincture
    # and then stick the ellipses on top of it.
    inner_boundary = [[0, 0], [0, kScreenHeight],
                     [kScreenWidth, kScreenHeight], [kScreenWidth, 0]]
    dexter_chief_rect = Rect(-1*kScreenWidth/2, -1*y_midpoint, kScreenWidth, y_midpoint*2)
    sinister_chief_rect = Rect(kScreenWidth/2, -1*y_midpoint, kScreenWidth, y_midpoint*2)
    dexter_base_rect = Rect(-1*kScreenWidth/2, y_midpoint-y_fudge_factor,
                            kScreenWidth, y_midpoint*2)
    sinister_base_rect = Rect(kScreenWidth/2, y_midpoint-y_fudge_factor,
                              kScreenWidth, y_midpoint*2)
    dexter_chief_section = FieldSection([], ellipse = dexter_chief_rect,
                                        tincture = tinctures[0])
    sinister_chief_section = FieldSection([], ellipse = sinister_chief_rect,
                                        tincture = tinctures[0])
    dexter_base_section = FieldSection([], ellipse = dexter_base_rect,
                                        tincture = tinctures[0])
    sinister_base_section = FieldSection([], ellipse = sinister_base_rect,
                                        tincture = tinctures[0])
    inner_section = FieldSection(inner_boundary, tincture=tinctures[1])
    return Device("", [inner_section, dexter_chief_section, sinister_chief_section,
                       dexter_base_section, sinister_base_section])

def get_per_pall_field(tinctures):
    '''
    Returns a device with a per pall field.
    tinctures: a list of exactly 3 tinctures,
     which will be used in the order [chief, dexter, sinister].
    '''
    if len(tinctures) != 3:
        print("A per pall field must have exactly 3 tinctures.")
        return Device("")
    center = [int(kScreenWidth/2), int(kScreenHeight*0.3)]
    chief_boundary = [[0, 0], [kScreenWidth, 0], center]
    dexter_boundary = [[0, 0], [0, kScreenHeight], [int(kScreenWidth/2), kScreenHeight], center]
    sinister_boundary = [[kScreenWidth, 0], [kScreenWidth, kScreenHeight],
                         [int(kScreenWidth/2), kScreenHeight], center]
    chief_section = FieldSection(chief_boundary, tincture=tinctures[0])
    dexter_section = FieldSection(dexter_boundary, tincture=tinctures[1])
    sinister_section = FieldSection(sinister_boundary, tincture=tinctures[2])
    return Device("", [chief_section, dexter_section, sinister_section])

def get_per_pall_reversed_field(tinctures):
    '''
    Returns a device with a per pall reversed field.
    tinctures: a list of exactly 3 tinctures,
     which will be used in the order [dexter, sinister, base].
    '''
    if len(tinctures) != 3:
        print("A per pall reversed field must have exactly 3 tinctures.")
        return Device("")
    center = [int(kScreenWidth/2), int(kScreenHeight*0.5)]
    base_boundary = [[0, kScreenHeight], [kScreenWidth, kScreenHeight], center]
    dexter_boundary = [[0, 0], [0, kScreenHeight], center, [int(kScreenWidth/2), 0]]
    sinister_boundary = [[kScreenWidth, 0], [kScreenWidth, kScreenHeight],
                         center, [int(kScreenWidth/2), 0]]
    dexter_section = FieldSection(dexter_boundary, tincture=tinctures[0])
    sinister_section = FieldSection(sinister_boundary, tincture=tinctures[1])
    base_section = FieldSection(base_boundary, tincture=tinctures[2])
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

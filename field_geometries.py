from device_generator import *
constant_definitions =open("constants.py")
exec(constant_definitions.read())

def get_plain_field(tincture):
    '''
    Returns a Device with a field of a single tincture.
    tincture: the tincture in question, as a tuple of 
      three integers representing RGB values.
    '''
    boundary = [[0, 0], [0, kScreenHeight], [kScreenWidth, kScreenHeight], [kScreenWidth, 0]]
    return Device("", [FieldSection(boundary, tincture)])

def get_paly_boundaries(n):
    '''
    Returns a list of lists of lists which is the boundary boxes 
      for a paly of n field.
    n: the number of sections. Use 2 for per pale.
    '''
    boundary_sections = []
    for i in range(n):
        left_edge = int(kScreenWidth*i/n)
        right_edge = int(kScreenWidth*(i+1)/n)
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
        top_edge = int(kScreenHeight*i/n*fudge_factor+kMargin) 
        bottom_edge = int(kScreenHeight*(i+1)/n*fudge_factor+kMargin)
        boundary_sections.append(
            [[0, top_edge], [kScreenWidth, top_edge],
             [kScreenWidth, bottom_edge], [0, bottom_edge]])
    return boundary_sections

def get_bendy_boundaries(n):
    '''
    Returns a list of lists of lists which is the boundary boxes 
      for a bendy of n field.
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

def get_bendy_sinister_boundaries(n):
    '''
    Returns a list of lists of lists which is the boundary boxes 
      for a bendy sinister of n field.
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

def get_striped_field(num_sections, tinctures, direction):
    '''
    Returns a Device object with a field whose lines of division 
      all go a single direction.
    num_sections: the number of sections.
    tinctures: a list of tincture objects, e.g. [kVert, kArgent].
    direction: a string indicating direction.
      Must be one of the keys in the dict below.
    '''
    # The values in this dict are functions.
    directions = {"per pale": get_paly_boundaries, "paly": get_paly_boundaries,
                  "per fess": get_barry_boundaries, "barry": get_barry_boundaries,
                  "per bend": get_bendy_boundaries, "bendy": get_bendy_boundaries,
                  "per bend sinister": get_bendy_sinister_boundaries, "bendy sinister": get_bendy_sinister_boundaries}
    fieldsections = []
    boundaries = directions[direction](num_sections)
    for i in range(num_sections):
        fieldsections.append(FieldSection(boundaries[i], tinctures[i % len(tinctures)]))
    return Device("", fieldsections)

def get_quarterly_field(tinctures):
    '''
    Returns a device object with a quarterly field.
    tinctures: a list of exactly two tinctures.
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
    dexter_chief_section = FieldSection(dexter_chief_quarter, tinctures[0])
    sinister_chief_section = FieldSection(sinister_chief_quarter, tinctures[1])
    sinister_base_section = FieldSection(sinister_base_quarter, tinctures[2 % len(tinctures)])
    dexter_base_section = FieldSection(dexter_base_quarter, tinctures[3 % len(tinctures)])
    return Device("", [dexter_chief_section, sinister_chief_section,
                       dexter_base_section, sinister_base_section])


'''

dexter_chief_quarter = [[0, 0], [0, int(kScreenHeight*5/12)], [int(kScreenWidth/2), int(kScreenHeight*5/12)], [int(kScreenWidth/2), 0]]
sinister_chief_quarter = [[int(kScreenWidth/2), 0], [int(kScreenWidth/2), int(kScreenHeight*5/12)], [kScreenWidth, int(kScreenHeight*5/12)], [kScreenWidth, 0]]
dexter_base_quarter = [[0, int(kScreenHeight*5/12)], [0, kScreenHeight], [int(kScreenWidth/2), kScreenHeight], [int(kScreenWidth/2), int(kScreenHeight*5/12)]]
sinister_base_quarter = [[int(kScreenWidth/2), int(kScreenHeight*5/12)], [int(kScreenWidth/2), kScreenHeight], [kScreenWidth, kScreenHeight], [kScreenWidth, int(kScreenHeight*5/12)]]
dexter_chief_gules = FieldSection(dexter_chief_quarter, kGules)
sinister_chief_argent = FieldSection(sinister_chief_quarter, kArgent)
dexter_base_argent = FieldSection(dexter_base_quarter, kArgent)
sinister_base_gules = FieldSection(sinister_base_quarter, kGules)
quarterly = Device("", [dexter_chief_gules, sinister_chief_argent, dexter_base_argent, sinister_base_gules])
quarterly.display_device()
chief_saltire_boundary = [[int(kScreenWidth*.03), 0], [int(kScreenWidth/2), int(kScreenHeight*5/12)], [int(kScreenWidth*.97), 0]]
dexter_saltire_boundary = [[int(kScreenWidth*.03), 0], [int(kScreenWidth/2), int(kScreenHeight*5/12)], [int(kScreenWidth*.03), int(kScreenHeight*10/12)]]
# There are four points here. Don't mess with this without looking at it really carefully first.
base_saltire_boundary = [[int(kScreenWidth*.03), int(kScreenHeight*10/12)], [int(kScreenWidth/2), int(kScreenHeight*5/12)], [int(kScreenWidth*.97), int(kScreenHeight*10/12)], [int(kScreenWidth/2), kScreenHeight]]
sinister_saltire_boundary = [[int(kScreenWidth*.97), 0], [int(kScreenWidth/2), int(kScreenHeight*5/12)], [int(kScreenWidth*.97), int(kScreenHeight*10/12)]]
chief_saltire_section = FieldSection(chief_saltire_boundary, kArgent)
dexter_saltire_section = FieldSection(dexter_saltire_boundary, kPurpure)
base_saltire_section = FieldSection(base_saltire_boundary, kArgent)
sinister_saltire_section = FieldSection(sinister_saltire_boundary, kPurpure)
per_saltire = Device("", [chief_saltire_section, dexter_saltire_section, base_saltire_section, sinister_saltire_section])
per_saltire.display_device()
    
paly_5 = get_paly_field(7, [kVert, kArgent, kAzure])
paly_5.display_device()
'''

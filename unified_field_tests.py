import field_geometries
from device_generator import Device

from pygame import Rect

constant_definitions =open("constants.py")
exec(constant_definitions.read())
full_shield = Rect(kXMargin, kYMargin, kScreenWidth-2*kXMargin, kShieldBottom-kYMargin)
small_square = Rect(300, 300, 200, 200)
'''
# Plain field
field_geometries.get_plain_field(kPurpure, full_shield).display_device()
# Two-color parallel sections
field_geometries.get_striped_field(2, [kPurpure, kArgent], "per pale", full_shield).display_device()
field_geometries.get_striped_field(7, [kPurpure, kArgent], "paly", full_shield).display_device()
field_geometries.get_striped_field(2, [kPurpure, kArgent], "per fess", full_shield).display_device()
field_geometries.get_striped_field(7, [kPurpure, kArgent], "barry", full_shield).display_device()
field_geometries.get_striped_field(2, [kPurpure, kArgent], "per bend", full_shield).display_device()
field_geometries.get_striped_field(7, [kPurpure, kArgent], "bendy", full_shield).display_device()
field_geometries.get_striped_field(2, [kPurpure, kArgent], "per bend sinister", full_shield).display_device()
field_geometries.get_striped_field(7, [kPurpure, kArgent], "bendy sinister", full_shield).display_device()
field_geometries.get_striped_field(2, [kPurpure, kArgent], "per chevron", full_shield).display_device()
field_geometries.get_striped_field(7, [kPurpure, kArgent], "chevronelly", full_shield).display_device()
field_geometries.get_striped_field(2, [kPurpure, kArgent], "per chevron inverted", full_shield).display_device()
field_geometries.get_striped_field(7, [kPurpure, kArgent], "chevronelly inverted", full_shield).display_device()
# Quarterly
field_geometries.get_quarterly_field([kArgent, kPurpure], full_shield).display_device()
# Canton
field_geometries.get_quarterly_field([kArgent, kPurpure, kPurpure, kPurpure], full_shield).display_device()
# Per saltire
field_geometries.get_per_saltire_field([kArgent, kPurpure], full_shield).display_device()
# Per chevron throughout (and inverted)
field_geometries.get_per_chevron_throughout_field([kPurpure, kArgent], full_shield).display_device()
field_geometries.get_per_chevron_inverted_throughout_field([kPurpure, kArgent], full_shield).display_device()
# Vetu
field_geometries.get_vetu_field([kArgent, kPurpure], full_shield).display_device()
field_geometries.get_vetu_ploye_field([kArgent, kPurpure], full_shield).display_device()
# Per pall (and inverted)
field_geometries.get_per_pall_field([kArgent, kPurpure, kAzure], full_shield).display_device()
field_geometries.get_per_pall_reversed_field([kPurpure, kAzure, kArgent], full_shield).display_device()
# Gyronny
field_geometries.get_gyronny_field(6, [kPurpure, kArgent], full_shield).display_device()
field_geometries.get_gyronny_field(6, [kPurpure, kArgent], full_shield, horizontal=True).display_device()
field_geometries.get_gyronny_field(8, [kPurpure, kArgent], full_shield).display_device()
field_geometries.get_gyronny_field(10, [kPurpure, kArgent], full_shield).display_device()
field_geometries.get_gyronny_field(10, [kPurpure, kArgent], full_shield, horizontal=True).display_device()
field_geometries.get_gyronny_field(12, [kPurpure, kArgent], full_shield).display_device()
# "Lots of little blocks" situations
field_geometries.get_checky_field(8, [kPurpure, kArgent], full_shield).display_device() 
field_geometries.get_lozengy_field(8, [kPurpure, kArgent], full_shield).display_device() 
field_geometries.get_lozengy_field(20, [kPurpure, kArgent], full_shield).display_device() 
field_geometries.get_lozengy_field(8, [kPurpure, kArgent], full_shield, 1).display_device() 
field_geometries.get_lozengy_field(8, [kPurpure, kArgent], full_shield, 4).display_device()
field_geometries.get_lozengy_field(8, [kPurpure, kArgent], full_shield, 0.5).display_device()  
field_geometries.get_fretty_field(3, [kAzure, kOr], small_square, True).display_device()  
field_geometries.get_scaly_field(7, [kPurpure, kArgent], full_shield).display_device()  
'''
field_geometries.get_masoned_field(7, 12, [kPurpure, kArgent], full_shield).display_device()

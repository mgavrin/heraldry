import field_geometries
from device_generator import Device

from pygame import Rect

constant_definitions =open("constants.py")
exec(constant_definitions.read())
full_shield = Rect(kXMargin, kYMargin, kScreenWidth-2*kXMargin, kShieldBottom-kYMargin)

'''
# Plain field
Device("", [field_geometries.get_plain_field(kPurpure, full_shield)]).display_device()
# Two-color parallel sections
Device("", field_geometries.get_striped_field(2, [kPurpure, kArgent], "per pale", full_shield)).display_device()
Device("", field_geometries.get_striped_field(7, [kPurpure, kArgent], "paly", full_shield)).display_device()
Device("", field_geometries.get_striped_field(2, [kPurpure, kArgent], "per fess", full_shield)).display_device()
Device("", field_geometries.get_striped_field(7, [kPurpure, kArgent], "barry", full_shield)).display_device()
'''
#################### BEGIN BROKEN SECTION
Device("", field_geometries.get_striped_field(2, [kPurpure, kArgent], "per bend", full_shield)).display_device()
Device("", field_geometries.get_striped_field(7, [kPurpure, kArgent], "bendy", full_shield)).display_device()
'''
Device("", field_geometries.get_striped_field(2, [kPurpure, kArgent], "per bend sinister", full_shield)).display_device()
Device("", field_geometries.get_striped_field(7, [kPurpure, kArgent], "bendy sinister", full_shield)).display_device()
Device("", field_geometries.get_striped_field(2, [kPurpure, kArgent], "per chevron", full_shield)).display_device()
Device("", field_geometries.get_striped_field(7, [kPurpure, kArgent], "chevronelly", full_shield)).display_device()
Device("", field_geometries.get_striped_field(2, [kPurpure, kArgent], "per chevron inverted", full_shield)).display_device()
Device("", field_geometries.get_striped_field(7, [kPurpure, kArgent], "chevronelly inverted", full_shield)).display_device()
# Quarterly
field_geometries.get_quarterly_field([kArgent, kPurpure]).display_device()
# Canton
field_geometries.get_quarterly_field([kArgent, kPurpure, kPurpure, kPurpure]).display_device()
# Per saltire
field_geometries.get_per_saltire_field([kArgent, kPurpure]).display_device()
# Per chevron throughout (and inverted)
field_geometries.get_per_chevron_throughout_field([kArgent, kPurpure]).display_device()
field_geometries.get_per_chevron_inverted_throughout_field([kArgent, kPurpure]).display_device()
# Vetu
field_geometries.get_vetu_field([kArgent, kPurpure]).display_device()
field_geometries.get_vetu_ploye_field([kArgent, kPurpure]).display_device()
# Per pall (and inverted)
field_geometries.get_per_pall_field([kArgent, kPurpure, kAzure]).display_device()
field_geometries.get_per_pall_reversed_field([kPurpure, kAzure, kArgent]).display_device()
# Gyronny
field_geometries.get_gyronny_field(6, [kPurpure, kArgent]).display_device()
field_geometries.get_gyronny_field(6, [kPurpure, kArgent], horizontal=True).display_device()
field_geometries.get_gyronny_field(8, [kPurpure, kArgent]).display_device()
field_geometries.get_gyronny_field(10, [kPurpure, kArgent]).display_device()
field_geometries.get_gyronny_field(10, [kPurpure, kArgent], horizontal=True).display_device()
field_geometries.get_gyronny_field(12, [kPurpure, kArgent]).display_device()
# "Lots of little blocks" situations
field_geometries.get_checky_field(8, [kPurpure, kArgent]).display_device() 
field_geometries.get_lozengy_field(8, [kPurpure, kArgent]).display_device() 
field_geometries.get_lozengy_field(20, [kPurpure, kArgent]).display_device() 
field_geometries.get_lozengy_field(8, [kPurpure, kArgent], 1).display_device() 
field_geometries.get_lozengy_field(8, [kPurpure, kArgent], 4).display_device()
field_geometries.get_lozengy_field(8, [kPurpure, kArgent], 0.5).display_device()  
'''

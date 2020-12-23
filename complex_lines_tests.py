import field_geometries
import lines_of_division
from device_generator import Device

from pygame import Rect

constant_definitions =open("constants.py")
exec(constant_definitions.read())
# Rect is (left, top, width, height)
full_shield = Rect(kXMargin, kYMargin, kScreenWidth-2*kXMargin, kShieldBottom-kYMargin)
band_width = 150
'''
fesswise_line = Rect(kXMargin, 375,
                     kScreenWidth-2*kXMargin, band_width)
field = field_geometries.get_striped_field(2, [kPurpure, kArgent], "per fess", full_shield)
line = lines_of_division.indented([kPurpure, kArgent], fesswise_line, lines_of_division.Orientation.FESSWISE)
field.merge(line)
field.display_device()

palewise_line = Rect(int((kScreenWidth-band_width)*0.5), kYMargin,
                     band_width, kShieldBottom-kYMargin)
field = field_geometries.get_striped_field(2, [kPurpure, kArgent], "per pale", full_shield)
line = lines_of_division.indented([kPurpure, kArgent], palewise_line, lines_of_division.Orientation.PALEWISE)
field.merge(line)
field.display_device()
'''

field = field_geometries.get_striped_field(2, [kPurpure, kArgent], "per bend", full_shield)
line = lines_of_division.indented([kPurpure, kArgent], full_shield, lines_of_division.Orientation.BENDWISE, 24)
field.merge(line)
field.display_device()

field = field_geometries.get_striped_field(2, [kPurpure, kArgent], "per bend", full_shield)
line = lines_of_division.indented([kPurpure, kArgent], full_shield, lines_of_division.Orientation.BENDWISE, 25)
field.merge(line)
field.display_device()

field = field_geometries.get_striped_field(2, [kPurpure, kArgent], "per bend sinister", full_shield)
line = lines_of_division.indented([kPurpure, kArgent], full_shield, lines_of_division.Orientation.BENDWISE_SINISTER, 24)
field.merge(line)
field.display_device()

field = field_geometries.get_striped_field(2, [kPurpure, kArgent], "per bend sinister", full_shield)
line = lines_of_division.indented([kPurpure, kArgent], full_shield, lines_of_division.Orientation.BENDWISE_SINISTER, 25)
field.merge(line)
field.display_device()

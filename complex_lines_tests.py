import field_geometries
import lines_of_division
from device_generator import Device

from pygame import Rect

constant_definitions =open("constants.py")
exec(constant_definitions.read())
# Rect is (left, top, width, height)
full_shield = Rect(kXMargin, kYMargin, kScreenWidth-2*kXMargin, kShieldBottom-kYMargin)
band_width = 150
fesswise_line = Rect(kXMargin, 375,
                     kScreenWidth-2*kXMargin, band_width)

field = field_geometries.get_striped_field(2, [kPurpure, kArgent], "per fess", full_shield)
line = lines_of_division.indented([kPurpure, kArgent], fesswise_line, lines_of_division.Orientation.FESSWISE)
field.merge(line)
field.display_device()

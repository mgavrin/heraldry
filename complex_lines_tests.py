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
field_geometries.get_striped_field(
    2, [kPurpure, kArgent], "per pale", full_shield,
    field_geometries.LineType.INDENTED).display_device()

field_geometries.get_striped_field(
    7, [kPurpure, kArgent], "paly", full_shield,
    field_geometries.LineType.INDENTED).display_device()

field_geometries.get_striped_field(
    2, [kPurpure, kArgent], "per fess", full_shield,
    field_geometries.LineType.INDENTED).display_device()

field_geometries.get_striped_field(
    5, [kPurpure, kArgent], "per fess", full_shield,
    field_geometries.LineType.INDENTED).display_device()
'''
field_geometries.get_striped_field(
    2, [kPurpure, kArgent], "per bend", full_shield,
    field_geometries.LineType.INDENTED).display_device()

small_square = Rect(300, 300, 200, 200)
field_geometries.get_striped_field(
    7, [kPurpure, kArgent], "bendy", full_shield,
    field_geometries.LineType.INDENTED).display_device()

field_geometries.get_striped_field(
    2, [kPurpure, kArgent], "per bend sinister", full_shield,
    field_geometries.LineType.INDENTED).display_device()

import field_geometries
from device_generator import Device

from pygame import Rect

constant_definitions =open("constants.py")
exec(constant_definitions.read())
full_shield = Rect(kXMargin, kYMargin, kScreenWidth-2*kXMargin, kShieldBottom-kYMargin)
small_square = Rect(300, 300, 200, 200)
dexter_half = Rect(kXMargin, kYMargin, int(0.5*(kScreenWidth-2*kXMargin)), kShieldBottom-kYMargin)
sinister_half = Rect(int(0.5*kScreenWidth), kYMargin, int(0.5*(kScreenWidth-2*kXMargin)), kShieldBottom-kYMargin)

# Per pale purpure and barry argent and azure
Device("", [field_geometries.get_plain_field(kPurpure, dexter_half)] + field_geometries.get_striped_field(7, [kArgent, kAzure], "barry", sinister_half)).display_device()

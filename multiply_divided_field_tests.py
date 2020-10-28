import field_geometries
from device_generator import Device

from pygame import Rect

constant_definitions =open("constants.py")
exec(constant_definitions.read())
full_shield = Rect(kXMargin, kYMargin, kScreenWidth-2*kXMargin, kShieldBottom-kYMargin)
small_square = Rect(300, 300, 200, 200)
dexter_half = Rect(kXMargin, kYMargin, int(0.5*(kScreenWidth-2*kXMargin)), kShieldBottom-kYMargin)
sinister_half = Rect(int(0.5*kScreenWidth), kYMargin, int(0.5*(kScreenWidth-2*kXMargin)), kShieldBottom-kYMargin)

'''
print("Per pale azure fretty Or and barry purpure and argent")
dexter_half_device = field_geometries.get_fretty_field(
    3, [kAzure, kOr], dexter_half, True)
sinister_half_device = field_geometries.get_striped_field(7, [kPurpure, kArgent], "barry", sinister_half)
dexter_half_device.merge(sinister_half_device)
dexter_half_device.display_device()
'''

print("Barry 13 gules and argent, a canton azure")
canton = Rect(kXMargin, kYMargin,
              int(0.5*(kScreenWidth-2*kXMargin)), int(7/13*full_shield.height))
bottom_layer = field_geometries.get_striped_field(13, [kGules, kArgent], "barry", full_shield)
top_layer = field_geometries.get_plain_field(kAzure, canton)
bottom_layer.merge(top_layer) #order matters here
bottom_layer.display_device()

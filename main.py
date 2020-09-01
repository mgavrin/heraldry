import field_geometries

constant_definitions =open("constants.py")
exec(constant_definitions.read())

field_geometries.get_striped_field(2, [kPurpure, kArgent], "per chevron inverted").display_device()

field_geometries.get_striped_field(7, [kPurpure, kArgent], "per chevron inverted").display_device()

import field_geometries

constant_definitions =open("constants.py")
exec(constant_definitions.read())

field_geometries.get_striped_field(2, [kPurpure, kArgent], "per bend sinister").display_device()

field_geometries.get_striped_field(27, [kPurpure, kArgent], "bendy").display_device()

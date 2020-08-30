import field_geometries

constant_definitions =open("constants.py")
exec(constant_definitions.read())

field_geometries.get_striped_field(27, [kVert, kArgent], "per fess").display_device()

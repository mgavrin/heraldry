import field_geometries

constant_definitions =open("constants.py")
exec(constant_definitions.read())

field_geometries.get_vetu_field([kArgent, kPurpure]).display_device()

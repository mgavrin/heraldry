import field_geometries

constant_definitions =open("constants.py")
exec(constant_definitions.read())

field_geometries.get_quarterly_field([kPurpure, kArgent]).display_device()

field_geometries.get_quarterly_field([kPurpure, kArgent, kAzure, kOr]).display_device()

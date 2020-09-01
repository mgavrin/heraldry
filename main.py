import field_geometries

constant_definitions =open("constants.py")
exec(constant_definitions.read())

field_geometries.get_per_chevron_throughout_field([kPurpure, kArgent]).display_device()

field_geometries.get_per_chevron_inverted_throughout_field([kPurpure, kArgent]).display_device()

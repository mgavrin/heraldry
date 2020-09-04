import field_geometries

constant_definitions =open("constants.py")
exec(constant_definitions.read())

'''
# Plain field
field_geometries.get_plain_field(kPurpure).display_device()
# Two-color parallel sections
field_geometries.get_striped_field(2, [kArgent, kPurpure], "per pale").display_device()
field_geometries.get_striped_field(7, [kArgent, kPurpure], "paly").display_device()
field_geometries.get_striped_field(2, [kArgent, kPurpure], "per fess").display_device()
field_geometries.get_striped_field(7, [kArgent, kPurpure], "barry").display_device()
field_geometries.get_striped_field(2, [kArgent, kPurpure], "per bend").display_device()
field_geometries.get_striped_field(7, [kArgent, kPurpure], "bendy").display_device()
field_geometries.get_striped_field(2, [kArgent, kPurpure], "per bend sinister").display_device()
field_geometries.get_striped_field(7, [kArgent, kPurpure], "bendy sinister").display_device()
field_geometries.get_striped_field(2, [kArgent, kPurpure], "per chevron").display_device()
field_geometries.get_striped_field(7, [kArgent, kPurpure], "chevronelly").display_device()
field_geometries.get_striped_field(2, [kArgent, kPurpure], "per chevron inverted").display_device()
field_geometries.get_striped_field(7, [kArgent, kPurpure], "chevronelly inverted").display_device()
# Quarterly
field_geometries.get_quarterly_field([kArgent, kPurpure]).display_device()
# Canton
field_geometries.get_quarterly_field([kArgent, kPurpure, kPurpure, kPurpure]).display_device()
# Per saltire
field_geometries.get_per_saltire_field([kArgent, kPurpure]).display_device()
# Per chevron throughout (and inverted)
field_geometries.get_per_chevron_throughout_field([kArgent, kPurpure]).display_device()
field_geometries.get_per_chevron_inverted_throughout_field([kArgent, kPurpure]).display_device()
# Vetu
field_geometries.get_vetu_field([kArgent, kPurpure]).display_device()
field_geometries.get_vetu_ploye_field([kArgent, kPurpure]).display_device()
# Per pall (and inverted)
'''
field_geometries.get_per_pall_field([kArgent, kPurpure, kAzure]).display_device()
field_geometries.get_per_pall_reversed_field([kPurpure, kAzure, kArgent]).display_device()

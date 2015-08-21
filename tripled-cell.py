from cctbx import xray

# Simple interface to load a ShelX .res file
# Interpret constraints but then forget about them,
# So we just get a list of scatterers x,y,z, U's, etc
xs = xray.structure.from_shelx(filename='03srv209.res')

# Let's look at the unit cell
uc = xs.unit_cell()
print uc.parameters()
print "volume: %f" % uc.volume()

# Convenience routine for debugging
#xs.show_scatterers()

# Same but graphical (no Olex2, Coot or ShelXle!)
# First we import the tool we need (only needed once)
try:
    from crys3d.qttbx.xray_structure_viewer import display
except IOError:
    def display(*args, **kwds): pass
# then use it
#display(xray_structure=xs)

# Let's look at symmetries
info = xs.space_group_info()
info.show_summary()
print "Hall: %s" % info.type().hall_symbol()
# List of all symmetries
print "Symmetries:"
for rt in info.group():
    print rt.as_xyz()
# The mathematical object representing the group
g = info.group()
print "Inversion at origin:%s" % ('no', 'yes')[g.is_origin_centric()]

# Let's triple the cell
from cctbx import sgtbx
g.expand_ltr(sgtbx.tr_vec((1,0,1),3).new_denominator(g.t_den()))
g.expand_ltr(sgtbx.tr_vec((2,0,2),3).new_denominator(g.t_den()))
tripled_info = sgtbx.space_group_info(group=g)
tripled_info.show_summary()
print tripled_info.type().hall_symbol()

# Let's change the space group of the structure now
xs.as_cif_simple(open('03srv209x3.cif', 'w'))


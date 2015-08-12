import os
import glob
dname = os.path.basename(os.path.normpath(os.path.dirname(__file__)))
modules = glob.glob(os.path.dirname(__file__)+"/*.py")
mods = [os.path.basename(f)[:-3] for f in modules if not os.path.basename(f).startswith('_')]
for name in mods:
	exec("from " + dname +"." + name +" import *")
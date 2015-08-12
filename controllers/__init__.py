import os
import glob
#print(os.path.dirname(__file__))
dname = os.path.basename(os.path.normpath(os.path.dirname(__file__)))
modules = glob.glob(os.path.dirname(__file__)+"/*.py")
#__all__ = [os.path.basename(f)[:-3] for f in modules if not os.path.basename(f).startswith('_')]
mods = [os.path.basename(f)[:-3] for f in modules if not os.path.basename(f).startswith('_')]
for name in mods:
	#print("from controllers." + name +" import *")
	exec("from " + dname +"." + name +" import *")
	#__import__("controllers."+name, locals(), globals())
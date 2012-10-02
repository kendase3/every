from distutils.core import setup
import py2exe, os 

# ok internet.  i'll trust your garbage code just this once...
originalSystemDLL = py2exe.build_exe.isSystemDLL
def isSystemDLL(pathname):
	if os.path.basename(pathname).lower() in ["sdl_ttf.dll"]:
		return 0
	return originalSystemDLL(pathname)
py2exe.build_exe.isSystemDLL = isSystemDLL

dataList = [os.path.join("fonts", "freemonobold.ttf")] 
setup(console=['teensyclient.py'],
	data_files = dataList)

import importlib
import inspect
import sys

import libcloud
import libcloud.compute
import libcloud.compute.drivers

"""
import cherrypy
class server( object ):
	def index( self ):
		return "HI"
	index.exposed = True

cherrypy.quickstart( server() )
"""

# Iterate through all available drivers.
for driver in libcloud.compute.drivers.__all__:
	
	# Since the path isn't going to change, generate it once.
	module_path = "libcloud.compute.drivers.{0}".format(driver)

	# Import the module by name. This will add it to sys.modules.
	importlib.import_module( module_path )

	# Iterate over the classes of the compute module.
	for member_name, member_val in inspect.getmembers( sys.modules[module_path], inspect.isclass ):

		# Regex match for /NodeDriver$/ ..
		print "I have member name of {0}".format( member_name )
import importlib
import inspect
import sys
import re

import libcloud

"""
import cherrypy
class server( object ):
	def index( self ):
		return "HI"
	index.exposed = True

cherrypy.quickstart( server() )
"""

def get_argspecs( what ):
	"""
	Iterate through the particular drivers.

	what can currently be 'compute', 'dns', 'loadbalancer', or 'storage'
	"""
	_return = [ ]

	# Import the particular module and drivers.
	importlib.import_module( "libcloud.{0}".format(what) )
	importlib.import_module( "libcloud.{0}.drivers".format(what) )

	# Iterate through all available drivers.
	# Note that we cannot rely on libcloud.#{what}.drivers.__all__ because the
	# dns packages does not populate it.

	for driver in sys.modules["libcloud.{0}.drivers".format(what)].__all__:
		
		# Since the path isn't going to change, generate it once.
		module_path = "libcloud.compute.drivers.{0}".format(driver)

		# Import the module by name. This will add it to sys.modules.
		importlib.import_module( module_path )

		# Iterate over the classes of the compute module.
		for member_name, member_val in inspect.getmembers( sys.modules[module_path], inspect.isclass ):

			# Regex match for /.*NodeDriver$/ ..
			if not re.match( ".*NodeDriver$", member_name ):
				continue

			# Get the spec for the node drivers __init__ ..
			arg_spec = inspect.getargspec( getattr( member_val, "__init__" ) )

			# Quick hack. See LIBCLOUD-405 for why this exists.
			if len( arg_spec[0] ) == 1:
				continue

			_return.append( driver )
	return _return

print get_argspecs( "compute" )
print get_argspecs( "dns" )

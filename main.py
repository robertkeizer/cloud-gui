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

	what can currently be
		'compute'
		'dns'
		'loadbalancer'
		'storage'
	"""
	_return = [ ]

	# Import the base module and the drivers.
	importlib.import_module( "libcloud.{0}".format(what) )
	importlib.import_module( "libcloud.{0}.drivers".format(what) )

	_drivers = __import__( "libcloud.{0}.drivers".format(what), globals(), locals(), [ "*" ] )
	
	for driver_name,driver_obj in _drivers.__dict__.items():

		print driver_name

		if not "libcloud.{0}.drivers.{1}".format(what,driver_name) in sys.modules:
			continue

		for member_name, member_val in inspect.getmembers( driver_obj, inspect.isclass ):

			# Regex match for /.*NodeDriver$/ ..
			if not re.match( ".*NodeDriver$", member_name ):
				continue

			# Get the spec for the node drivers __init__ ..
			arg_spec = inspect.getargspec( getattr( member_val, "__init__" ) )

			# Quick hack. See LIBCLOUD-405 for why this exists.
			if len( arg_spec[0] ) == 1:
				continue

			print "I have {0}.{1}".format( driver_name, member_name )

	return _return

#print get_argspecs( "compute" )
#print get_argspecs( "dns" )
print get_argspecs( "loadbalancer" )

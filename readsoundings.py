# readsoundings.py file 

import numpy as np

def parse_SPC(filename, skip_rows=7):
	""" Returns a "record array" which is a special type
	of array that has column names and row access 
	built into it.  The column names and data types
	are defined by the dtype object."""
	dtype = [('p', float),			# pressure, mb
			 ('z', float),			# altitude, m
			 ('T', float),			# temperature, C
			 ('Td', float),			# dewpoint, C
			 ('wind_dir', float),	# wind direction, degrees
			 ('wind_spd', float)	# wind speed, knots
			 ]
	data = np.genfromtxt(filename, dtype = dtype, skip_header=skip_rows, delimiter=',')
	return data
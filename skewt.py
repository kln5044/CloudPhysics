# Kelly's python code 


import numpy as np 
import math

C_to_K = 273.15 
skew_slope = 40

def x_from_Tp(T,p):
	""" Calculates x from equation 1. """
	x = T - (skew_slope*math.exp(p))
	return x

def y_from_p(p):
	""" Calculates y from equation 2. """
	y = -(math.exp(p))
	return y

def p_from_y (y):
	""" Calculates p from equation 1. """
		p = -(math.exp(y))
		return p 

def T_from_xp (x,p):
		""" Calculates t from x and p. """
		t = x + skew_slope*(math.exp(p))
		return t

def to_thermo(x,y):
	""" Transform T_C (in degrees Celsius)
		and p (in mb) to (x,y). """
		y = y_from_p(p)
		x = x_from_Tp(T_C+C_to_K, p)
		return x, y

def from_thermo(T_C,p):
	""" Transform T_C (in degrees Celsius)
		and p (in mb) to (x,y). """
		y = y_from_p(p)
		x = x_from_Tp(T_C+C_to_K, p)
		return x,y
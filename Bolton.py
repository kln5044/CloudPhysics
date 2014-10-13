C_to_K = 273.15
c_p_dry = 1005.7
c_V_dry = 718.66
eps = 0.622
k_dry = 0.0007

def sat_vapor_pressure(T):
	""" Inputs temperature in Celsius, outputs saturation 
		vapor pressure in mb.  Equation taken from
		Bolton (1980).  For temperatures less than 35 deg
		C and greater than -35 deg C, this equation 
		provides results to an accuracy of 0.1%. """ 

		es = 6.112 * exp((17.67*T)/(T+243.5)) 
		return es 

def sat_vapor_temperature(e_s):
	""" Inputs saturation vapor pressure in mb, outputs
		saturation vapor pressure in degrees Celsius.
		Equation taken from Botlon (1980) and gives
		temperatures accurate to 0.03 deg C for a
		range of temperatures from -35 deg C to 
		35 deg C. """ 

		sat_T = ((243.5*log(e_s))-440.8)/(19.48-log(e_s))
		return sat_T

def sat_mixing_ratio(p,T):
	""" Inputs pressure in mb and temperature in 
		degrees Celsius, outputs saturation mixing 
		ratio in kg/kg. """

		w = (eps*sat_vapor_pressure(T))/(p-sat_vapor_pressure(T))
		return w 

def mixing_ratio_line(p,w_s):
	""" Inputs pressure in mb and saturation mixing 
		ratio in kg/kg, outputs temperature in 
		degrees Celsius. """

		es = (w_s*p)/(eps-w_s)
		T = sat_vapor_temperature(es)
		return T 

def RH(T,p,w):
	""" Inputs temperature in Celsius, pressure in mb,
		and mixing ratio in kg/kg, outputs relative
		humidity as a percent. """
		
		RH = (w/(sat_mixing_ratio(p,T))) * 100
		return RH 

def T_LCL(T,RH):
	""" Inputs temperature in Kelvin and relative
		humidity as a percent, outputs the lifted
		condensation level temperature in Kelvin."""

		T = 
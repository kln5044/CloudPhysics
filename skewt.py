import numpy as np 
import  Bolton
import matplotlib.pyplot as plt
from mpl_toolkits.axisartist import Subplot
from matplotlib.ticker import FuncFormatter, Formatter 
from mpl_toolkits.axisartist.grid_helper_curvelinear import GridHelperCurveLinear 
from readsoundings import parse_SPC

#import os
#print os.listdir("/Users/Kelly/Documents/TTU/CloudPhysics")
path_to_file = "/Users/Kelly/Documents/TTU/CloudPhysics/14101212_OBS_PIT.txt"
sounding_data = parse_SPC(path_to_file)

# Extract temperature from the sounding  and find the lines
# with physical data values
snd_T = sounding_data['T']
snd_P = sounding_data['p']
snd_Td = sounding_data['Td']
# all temperature values, degrees C, should be in this range.
good_T = (snd_T > -100.0) & (snd_T < 60.0)
# all pressure values, in mb, should be in this range.
good_P = (snd_P > 99.0) & (snd_P < 1001.0)
# all dewpoint columns, degrees C, should be in this range.
good_Td = (snd_Td > -200.0) & (snd_Td < 60.0)

C_to_K = 273.15 
skew_slope = 40


def x_from_Tp(T,p):
	""" Calculates x from equation 1. """
	x = T - (skew_slope*np.log(p))
	return x

def y_from_p(p):
	""" Calculates y from equation 2. """
	y = -(np.log(p))
	return y

def p_from_y (y):
	""" Calculates p from equation 1. """
	p = (np.exp(-y))
	return p 

def T_from_xp (x,p):
	""" Calculates t from x and p. """
	t = x + (skew_slope*(np.log(p)))
	return 


def to_thermo(x,y):
	""" Transform (x,y) coordinates to T in
	degrees Celsius and p in mb. """
	p = p_from_y(y)
	T_C = T_from_xp(x, p) - C_to_K
	return T_C, p 

def from_thermo(T_C,p):
	""" Transform T_C (in degrees Celsius)
	and p (in mb) to (x,y). """
	y = y_from_p(p)
	x = x_from_Tp(T_C+C_to_K, p)
	return x, y

# Converting temperature, dew point, and pressure
# for plotting using the x and y coordinate 
# conversion functions.

x_snd_Td, y_snd_p = from_thermo(snd_Td, snd_P)
x_snd_T, y_snd_p = from_thermo(snd_T, snd_P)

# values along the bottom and left edges
p_bottom = 1050.0
p_top = 150
T_min = -40 + C_to_K
T_max = 50 + C_to_K

x_min, y_min = from_thermo((T_min - C_to_K), p_bottom)
x_max, y_max = from_thermo((T_max - C_to_K), p_top)


p_levels = np.arange(1000, 150-50, -50)
T_C_levels = np.arange(-80, 40+10, 10)				# T levels in deg Celsius
T_levels = T_C_levels + C_to_K 						# T levels in K
theta_levels = np.arange(-40, 100+10, 10) + C_to_K # Theta levels in K 
theta_ep_levels = theta_levels.copy() 				# Theta ep levels in K
mixing_ratios = np.asarray([.0004, .001, .002, .003, .005, .008, .012, .016, .020])
													# Mixing ratio in kg/kg


p_all = np.arange(p_bottom, p_top-1,-1)			# Pressure levels in 1 mb increments
y_p_levels = y_from_p(p_levels)
y_all_p = y_from_p(p_all)
x_T_levels = [x_from_Tp(Ti, p_all) for Ti in T_levels]
x_thetas = [x_from_Tp(Bolton.theta_dry(theta_i, p_all),p_all) for theta_i in theta_levels]
x_mixing_ratios = [x_from_Tp((Bolton.mixing_ratio_line(p_all,Bolton.sat_mixing_ratio(p_all, Ti))), p_all) for Ti in T_C_levels]

mesh_T, mesh_p = np.meshgrid(
	np.arange(-60.0, T_levels.max()-C_to_K+0.1, 0.1), p_all)
theta_ep_mesh = Bolton.theta_ep_field(mesh_T, mesh_p)



# Plotting Code!

skew_grid_helper = GridHelperCurveLinear((from_thermo, to_thermo))


fig = plt.figure()
ax = Subplot(fig, 1, 1, 1, grid_helper=skew_grid_helper)
fig.add_subplot(ax)

for yi in y_p_levels: 
	ax.plot((x_min, x_max), (yi,yi), color = (1.0, 0.8, 0.8))

for x_T in x_T_levels: 
	ax.plot(x_T, y_all_p, color=(1.0, 0.5, 0.5))

for x_theta in x_thetas:
	ax.plot(x_theta, y_all_p, color=(1.0, 0.7, 0.7))

for x_mixing_ratio in x_mixing_ratios:
	good = p_all >= 600  # restrict mixing ratio lines to below 600 mb
	ax.plot(x_mixing_ratio[good], y_all_p[good], color = (0.8, 0.8, 0.6))

n_moist = len(theta_ep_mesh)
moist_colors = ((0.6, 0.9, 0.7),)*n_moist
ax.contour(x_from_Tp(mesh_T+C_to_K, mesh_p), y_from_p(mesh_p),
	theta_ep_mesh, theta_ep_levels, colors = moist_colors)

ax.axis((x_min, x_max, y_min, y_max))

def format_coord(x, y):
	T, p = to_thermo(x, y)
	return "{0:5.1f} C, {1:5.1f} mb".format(float(T), float(p))

ax.format_coord = format_coord
ax.plot(x_snd_Td, y_snd_p, linewidth = 2, color = 'g')
ax.plot(x_snd_T, y_snd_p, linewidth = 2, color = 'r')

plt.show()
#!/usr/bin/env python

#Andrew Burt - a.burt@ucl.ac.uk

import argparse
import numpy
import numpy.linalg
import scipy.io
import matplotlib.pyplot
from mpl_toolkits.mplot3d import Axes3D

def meshCylinder(p0,p1,R,high_quality=False):
	faces = 6
	if(high_quality == True):
		faces = 25 #looks good to me
	###
	#create mesh of cylinder - by 'Amy Teegarden' - https://stackoverflow.com/questions/32317247/
	v = p1 - p0
	mag = numpy.linalg.norm(v)
	v = v / mag
	not_v = numpy.array([1, 0, 0])
	if (v == not_v).all():
		not_v = numpy.array([0, 1, 0])
	n1 = numpy.cross(v,not_v)
	n1 /= numpy.linalg.norm(n1)
	n2 = numpy.cross(v, n1)
	t = numpy.linspace(0, mag, faces)
	theta = numpy.linspace(0, 2 * numpy.pi, faces)
	t, theta = numpy.meshgrid(t, theta)
	X, Y, Z = [p0[i] + v[i] * t + R * numpy.sin(theta) * n1[i] + R * numpy.cos(theta) * n2[i] for i in [0, 1, 2]]
	#
	return X,Y,Z

def plotModels(models,azimuth=30,elevation=30,high_quality=False,disp_axes=False,outname='model.pdf'):

	fig = matplotlib.pyplot.figure(frameon=False)
	ax = fig.add_subplot(111, projection='3d')
	ax.view_init(azim=azimuth,elev=elevation)
	for i in range(len(models)):
		model = scipy.io.loadmat(models[i])
		if(len(models) == 1):
			colour = 'k'
		else:
			colour = numpy.random.rand(3,)
		for j in range(len(model['qsm']['cylinder'][0][0][0][0]['radius'])):
			R = model['qsm']['cylinder'][0][0][0][0]['radius'][j][0]
			p0 = numpy.array([model['qsm']['cylinder'][0][0][0][0]['start'][j][0],model['qsm']['cylinder'][0][0][0][0]['start'][j][1],model['qsm']['cylinder'][0][0][0][0]['start'][j][2]])
			p1 = numpy.array([model['qsm']['cylinder'][0][0][0][0]['start'][j][0] + (model['qsm']['cylinder'][0][0][0][0]['length'][j][0] * model['qsm']['cylinder'][0][0][0][0]['axis'][j][0]),model['qsm']['cylinder'][0][0][0][0]['start'][j][1] + (model['qsm']['cylinder'][0][0][0][0]['length'][j][0] * model['qsm']['cylinder'][0][0][0][0]['axis'][j][1]),model['qsm']['cylinder'][0][0][0][0]['start'][j][2] + (model['qsm']['cylinder'][0][0][0][0]['length'][j][0] * model['qsm']['cylinder'][0][0][0][0]['axis'][j][2])])
			X,Y,Z = meshCylinder(p0,p1,R,high_quality=high_quality)
			ax.plot_surface(X,Y,Z,alpha=0.75,linewidth=0,color=colour)
	###
	#set aspect ratio to 1 - by 'karlo' - https://stackoverflow.com/questions/13685386/
	ax.set_aspect('equal')
	x_limits = ax.get_xlim3d()
	y_limits = ax.get_ylim3d()
	z_limits = ax.get_zlim3d()
	x_range = abs(x_limits[1] - x_limits[0])
	x_middle = numpy.mean(x_limits)
	y_range = abs(y_limits[1] - y_limits[0])
	y_middle = numpy.mean(y_limits)
	z_range = abs(z_limits[1] - z_limits[0])
	z_middle = numpy.mean(z_limits)
	plot_radius = 0.5*max([x_range, y_range, z_range])
	ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
	ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
	ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])
	###
	if(disp_axes == False):
		matplotlib.pyplot.axis('off')
	matplotlib.pyplot.savefig(outname)
	matplotlib.pyplot.close(fig)

if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument('-m','--models',nargs='*',help='QSMs generated via optqsm')
	parser.add_argument('-a','--azimuth',type=int,default=30,help='azimuth angle')
	parser.add_argument('-e','--elevation',type=int,default=30,help='elevation angle')
	parser.add_argument('-o','--outname',type=str,default='models.pdf',help='plot filename and format')
	parser.add_argument('-q','--highquality',action='store_true',help='render cylinders in higher quality')
	parser.add_argument('-ax','--dispaxes',action='store_true',help='display axes')
	args = parser.parse_args()
	plotModels(args.models,azimuth=args.azimuth,elevation=args.elevation,outname=args.outname,high_quality=args.highquality,disp_axes=args.dispaxes)

#!/usr/bin/env python

#Andrew Burt - a.burt@ucl.ac.uk

import argparse
import numpy
import matplotlib.pyplot
from mpl_toolkits.mplot3d import Axes3D

def plotClouds(woodclouds,leafclouds,azimuth=30,elevation=30,outname='clouds.pdf',disp_axes=False):

	fig = matplotlib.pyplot.figure(frameon=False)
	ax = fig.add_subplot(111, projection='3d')
	ax.view_init(azim=azimuth,elev=elevation)
	for i in range(len(woodclouds)):
		cloud = numpy.loadtxt(woodclouds[i])
		colour = '#8B4513'
		ax.scatter(cloud[:,0],cloud[:,1],cloud[:,2],alpha=1,s=0.01,lw=0,color=colour)
	for i in range(len(leafclouds)):
		cloud = numpy.loadtxt(leafclouds[i])
		colour = '#228B22'
		ax.scatter(cloud[:,0],cloud[:,1],cloud[:,2],alpha=1,s=0.01,lw=0,color=colour)
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
	parser.add_argument('-w','--woodclouds',nargs='*',help='ASCII xyx wood clouds')
	parser.add_argument('-l','--leafclouds',nargs='*',help='ASCII xyx leaf clouds')
	parser.add_argument('-a','--azimuth',type=int,default=30,help='azimuth angle')
	parser.add_argument('-e','--elevation',type=int,default=30,help='elevation angle')	
	parser.add_argument('-ax','--dispaxes',action='store_true',help='display axes')
	parser.add_argument('-o','--outname',type=str,default='clouds.pdf',help='plot filename and format')
	args = parser.parse_args()
	plotClouds(args.woodclouds,args.leafclouds,azimuth=args.azimuth,elevation=args.elevation,outname=args.outname,disp_axes=args.dispaxes)

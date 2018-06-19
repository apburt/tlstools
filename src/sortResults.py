#!/usr/bin/env python

#Andrew Burt - a.burt@ucl.ac.uk

import argparse
import sys
import math
import numpy

def matchTid(tid,array):

	arr_index = numpy.where(array['tid'] == tid)
	return arr_index[0][0]

def sortResults(atresults,apresults,mresults):

	atdata = numpy.genfromtxt(atresults,dtype=None,names=True,encoding='ASCII')
	apdata = numpy.genfromtxt(apresults,dtype=None,names=True,encoding='ASCII')
	mtmp = numpy.genfromtxt(mresults,dtype=None,encoding='ASCII')
	if(len(mtmp) != len(atdata)):
		sys.exit("tree-level allom data is of different length than tree-level QSM data")
	tresults = numpy.zeros(len(atdata),dtype=numpy.dtype(atdata.dtype.descr + [('qsm_t_vol','<f8'),('qsm_t_vol_std','<f8'),('qsm_t_agb','<f8'),('qsm_t_agb_std','<f8'),('qsm_t_agb_u','<f8')]))
	presults = numpy.zeros(1,dtype=numpy.dtype(apdata.dtype.descr + [('qsm_p_agb','<f8'),('qsm_p_agb_u','<f8')]))
	for i in range(len(atdata)):
		for j in range(len(atdata[0])):
			tresults[i][j] = atdata[i][j]
	for i in range(len(mtmp)):
		idx = matchTid(mtmp[i][0],tresults)
		tresults[idx]['qsm_t_vol'] = mtmp[i][1]
		tresults[idx]['qsm_t_vol_std'] = mtmp[i][2]
		tresults[idx]['qsm_t_agb'] = tresults[idx]['qsm_t_vol'] * tresults[idx]['rho']
		tresults[idx]['qsm_t_agb_std'] = tresults[idx]['qsm_t_vol_std'] * tresults[idx]['rho']
		tresults[idx]['qsm_t_agb_u'] = (1.96  * tresults[idx]['qsm_t_agb_std']) / tresults[idx]['qsm_t_agb']
	for i in range(len(apdata.dtype.descr)):
		label = apdata.dtype.descr[i][0]
		presults[label] = apdata[label]
	presults['qsm_p_agb'] = numpy.sum(tresults['qsm_t_agb'])
	presults['qsm_p_agb_u'] = (1/math.sqrt(len(tresults))) * numpy.mean(tresults['qsm_t_agb_u'])
	tfname = presults['pid'][0] + '_tree'
	pfname = presults['pid'][0] + '_plot'
	numpy.save(tfname,tresults)
	numpy.save(pfname,presults)

if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument('-at','--allometrytreeresults',type=str,help='tree-level results from nlallom')
	parser.add_argument('-ap','--allometryplotresults',type=str,help='plot-level results from nlallom')
	parser.add_argument('-m','--modelresults',type=str,help='results from optqsm')
	args = parser.parse_args()
	sortResults(args.allometrytreeresults,args.allometryplotresults,args.modelresults)

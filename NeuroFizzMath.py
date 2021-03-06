#!/usr/bin/env python
#  Classes for different neuron models.

from __future__ import division
from scipy import *
import numpy as np
import pylab
import matplotlib as mp
from matplotlib import pyplot as plt  
import sys
import math as mt

def rk4(t0 = 0, x0 = np.array([1]), t1 = 5 , dt = 0.01, ng = None):
    tsp = np.arange(t0, t1, dt)
    Nsize = np.size(tsp)
    X = np.empty((Nsize, np.size(x0)))
    X[0] = x0
    for i in range(1, Nsize):
        k1 = ng(X[i-1],tsp[i-1])
        k2 = ng(X[i-1] + dt/2*k1, tsp[i-1] + dt/2)
        k3 = ng(X[i-1] + dt/2*k2, tsp[i-1] + dt/2)
        k4 = ng(X[i-1] + dt*k3, tsp[i-1] + dt)
        X[i] = X[i-1] + dt/6*(k1 + 2*k2 + 2*k3 + k4)
    return X

class FN():
    name = "Fitzhugh-Nagumo"
    x0 = np.array([0.01,0.01])

    def __init__(self, name):
        self.name = name

    def model(self,x,t, a = 0.75, b = 0.8, c = 3,  i = -0.39):
        return np.array([c*(x[0]+ x[1]- x[0]**3/3 + i),
                         -1/c*(x[0]- a + b*x[1])])

    def do_pplot():
        pylab.figure()
        X = rk4(x0, t1=100, dt=0.02, ng=model)
        pylab.plot(X[:,1], X[:,0])
        pylab.title("Phase Portrait")
        pylab.xlabel("Membrane Recovery Variable")
        pylab.ylabel("Membrane Potential")
        pylab.savefig('FNpplot.png')
        pylab.show()
        return

    def do_fftplot():
        X = rk4(x0, t1 = 100,dt = 0.02, ng = model)
        Y = mean(X)    # determine DC component of signal
        X = X - Y      # subtract DC component from signal to get rid of peak at 0
        ps = np.abs(np.fft.fft(X[4:,0]))**2
        time_step = 1 / 30
        freqs = np.fft.fftfreq(int(len(X[4:,0])/2 - 1), time_step)
        idx = np.argsort(freqs)
        pylab.plot(freqs[idx], ps[idx])
        pylab.title("Power Spectrum of Membrane Potential Signal - FN")
        pylab.xlabel("Frequency (kHz)")
        pylab.ylabel("Power")
        pylab.xlim(0,0.4)
        pylab.ylim(0,2e7)
        pylab.savefig('FNfftplot.png')
        pylab.show()
        return

class ML():
    name = 'Morris-Lecar'
    x0 = np.array([0,0])
    def __init__(self, name, x0):
       self.name = name

    def model(x,t,c = 20,vk=-84,gk = 8,vca = 130,gca = 4.4,vl = -60,gl = 2,phi = 0.04,v1 = -1.2,v2 = 18,v3 = 2,v4 = 30,i = 79):
        return np.array([(-gca*(0.5*(1 + mt.tanh((x[0] - v1)/v2)))*(x[0]-vca) - gk*x[1]*(x[0]-vk) - gl*(x[0]-vl) + i),
                        (phi*((0.5*(1 + mt.tanh((x[0] - v3)/v4))) - x[1]))/(1/mt.cosh((x[0] - v3)/(2*v4)))])

    def do_pplot():
        pylab.figure()
        X = rk4(x0, t1 = 1000,dt = 0.1, ng = model)
        pylab.plot(X[:,0], X[:,1])
        pylab.title("Phase Portrait - single uncoupled ML neuron")
        pylab.xlabel("Membrane Potential")
        pylab.ylabel("Membrane Recovery Variable")
        pylab.savefig('MLpplot.png')
        pylab.show()
        return

    def do_tplot():
        pylab.figure()
        X = rk4(x0, t1 = 1000,dt = 0.1, ng = model)
        t0 = 0
        t1 = 1000
        dt = 0.1
        tsp = np.arange(t0, t1, dt)
        pylab.plot(tsp,X[:,0])
        pylab.title("Membrane Potential over Time - single uncoupled ML neuron")
        pylab.xlabel("Time")
        pylab.ylabel("Membrane Potential")
        pylab.savefig('MLtplot.png')
        pylab.show()
        return

    def do_fftplot():
        X = rk4(x0, t1 = 800,dt = 0.1, ng = model)
        Y = mean(X)		# determine DC component of signal
        X = X - Y		# subtract DC component from signal to get rid of peak at 0
        ps = np.abs(np.fft.fft(X[:,0]))**2
        time_step = 1 / 30
        freqs = np.fft.fftfreq(int(X.size/2 - 1), time_step)
        idx = np.argsort(freqs)
        pylab.plot(freqs[idx], ps[idx])
        pylab.title("Power Spectrum of Membrane Potential Signal")
        pylab.xlabel("Frequency (kHz)")
        pylab.ylabel("Power")
        pylab.xlim(0,0.4)
        pylab.ylim(0,2e10)
        pylab.savefig('MLfftplot.png')
        pylab.show()
        return

class IZ():
    name = 'Izhikevich'
    x0 = np.array([0,0])
    def __init__(self, name, x0):
       self.name = name

    def model(x,t, a = 0.02, b = 0.2, c = -65, d = 2, i = 10):
        if x[0] >= 30:
            x[0] = c
            x[1] = x[1] + d
        return np.array([0.04*(x[0]**2) + 5*x[0] + 140 - x[1] + i,
                        a*(b*x[0] - x[1])])


class HR():
    name = 'Hindmarsh-Rose'
    x0 = np.array([3, 0, -1.2])
    def __init__(self, name, x0):
       self.name = name

    def model(x,t, a = 1.0, b = 3.0, c = 1.0, d = 5.0, r = 0.006, s = 4.0, I = 1.84, xnot = -1.5, k = 0.05):
        return np.array([x[1] - a*(x[0]**3) + (b*(x[0]**2)) - x[2] + I + k*(x[3] - x[0]),
                        c - d*(x[0]**2) - x[1],
                        r*(s*(x[0] - xnot) - x[2]),
                        x[4] - a*(x[3]**3) + (b*(x[3]**2)) - x[5] + I + k*(x[0] - x[3]),
                        c - d*(x[3]**2) - x[4],
                        r*(s*(x[3] - xnot) - x[5])])

class HH():
    name = 'Hodgkins-Huxley'
    x0 = np.array([0.01,0.01,0.01,0.01])
    def __init__(self, name, x0):
       self.name = name

    def model(x,t, g_K=36, g_Na=120, g_L=0.3, E_K=12, E_Na=-115, E_L=-10.613, C_m=1, I=-10):
        alpha_n = (0.01*(x[0]+10))/(exp((x[0]+10)/10)-1)
        beta_n = 0.125*exp(x[0]/80)
        alpha_m = (0.1*(x[0]+25))/(exp((x[0]+25)/10)-1)
        beta_m = 4*exp(x[0]/18)
        alpha_h = (0.07*exp(x[0]/20))
        beta_h = 1 / (exp((x[0]+30)/10)+1)
        return np.array([(g_K*(x[1]**4)*(x[0]-E_K) + g_Na*(x[2]**3)*x[3]*(x[0]-E_Na) + g_L*(x[0]-E_L) - I)*(-1/C_m),
                        alpha_n*(1-x[1]) - beta_n*x[1],
                        alpha_m*(1-x[2]) - beta_m*x[2],
                        alpha_h*(1-x[3]) - beta_h*x[3]])

	
		

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 26 16:26:55 2023

@author: caueteixeira
"""

import hiperwalk as hpw
import numpy as np
import matplotlib.pyplot as plt

a=20
b=20

Torusab = hpw.Grid((a,b), periodic=True)
tRun=float(a*b)

QuantumWalkonTorusab = hpw.ContinuousTime(graph=Torusab,gamma=1.0)

for i in range(1,101):
    
    gammaexp = (i/100.0)
    QuantumWalkonTorusab.set_hamiltonian(gamma=gammaexp, marked=0)
    # QuantumWalkonTorusab.set_marked(marked=0)
    
    state=QuantumWalkonTorusab.uniform_state()    
    stateMatrix=QuantumWalkonTorusab.simulate(time=(tRun, 1),initial_state=state,hpc=False)
    
    # print(QuantumWalkonTorusab.get_hamiltonian())
    # print(QuantumWalkonTorusab.get_gamma())
    # print('==================')
    
    Y1 = []#stateMatrix[200]#[]
    X1 = np.arange(0, tRun)
    # print((gammaexp, len(X1)))
    #print(X1)
    
    print('================================')
    print((gammaexp, tRun))
    print('--------------------------------')
    
    for j in X1:
        Y1.append(abs(stateMatrix[int(j)][0])**2)
        #stateMatrix[j][50]*np.conj(stateMatrix[j][50]))
        #Norma=np.linalg.norm(stateMatrix[j])
        #print(Norma)
    
    # print(QuantumWalkonTorusab.get_evolution(1, hpc=False))
    print('--------------------------------')
    print(stateMatrix)
    probs = QuantumWalkonTorusab.probability_distribution(stateMatrix)
    print('================================')
    print()
        
    plt.plot(X1,Y1,'ro')         
    plt.xlabel('$t$')
    plt.ylabel('$<\Psi(t)|0>$')
    #plt.ylim([-1, 1])
    plt.legend(['$\gamma$ unico'])
    plt.grid()
    plt.savefig('GammaTorus' + str(a) + ',' + str(b) + '(gammaexp=' + str(gammaexp) + ').pdf')
    plt.show()
    plt.close()
    
    # probs = QuantumWalkonTorusab.probability_distribution(stateMatrix)
    # probs = probs[:,0]
    
    # hpw.plot_probability_distribution(probs, plot='line')

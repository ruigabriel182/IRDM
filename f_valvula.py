# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 14:37:56 2023

@author: Notbook
"""

# IMPORTAÇÃO DAS BIBLIOTECAS PRINCNIPAIS
import numpy as np

def f_valvula (rede, Q, valvula, nTubo, nValvula):

    for i in range(nValvula):
        if (abs(Q[nTubo+i]) > 0):
            if(valvula[i].tipo == str('TCV') and valvula[i].Kvalvula > 0):
                valvula[i].R2 = 8*valvula[i].Kvalvula/(9.81*np.pi**2*valvula[i].D**4)
                valvula[i].R2_0 = valvula[i].R2*abs(Q[nTubo+i])
                valvula[i].G2 = 2*valvula[i].R2_0 
        else:
            valvula[i].R2_0 = 10**-8
            valvula[i].G2 = 10**-8 
                
    R2_0 = np.array([n.R2_0 for n in valvula]).reshape(-1, 1)
    G2 = np.array([n.G2 for n in valvula]).reshape(-1, 1)
    
    return G2, R2_0, valvula

def f_valvula_transitorio (rede, Q, valvula, nTubo, nValvula):

    for i in range(nValvula):
        if (abs(Q[nTubo+i]) > 0):
            if(valvula[i].tipo == str('TCV') and valvula[i].Kvalvula > 0):
                valvula[i].R2 = 8*valvula[i].Kvalvula/(9.81*np.pi**2*valvula[i].D**4)
                valvula[i].R2_0 = valvula[i].R2*abs(Q[nTubo+i])
                valvula[i].G2 = valvula[i].R2_0 
        else:
            valvula[i].G2 = 10**-8
                
    G2 = np.array([n.G2 for n in valvula]).reshape(-1, 1)
    
    return G2, valvula
            
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 07:53:52 2024

@author: RUI GABRIEL
"""

# IMPORTAÇÃO DAS BIBLIOTECAS PRINCNIPAIS
import numpy as np

def f_bomba (rede, Q, bomba, nTubo, nValvula, nBomba):
    
    for i in range(nBomba):
        if (abs(Q[nTubo+nValvula+i]) > 0):
            bomba[i].R3_0 = (-bomba[i].coef_A/abs(Q[nTubo+nValvula+i])*(bomba[i].rotacao)**2 + (bomba[i].coef_B)*abs(Q[nTubo+nValvula+i]))
            bomba[i].G3 = 2*(bomba[i].coef_B)*abs(Q[nTubo+nValvula+i])        
        else:
            bomba[i].R3_0 = 10**-8
            bomba[i].G3 = 10**-8
            
    R3_0 = np.array([n.R3_0 for n in bomba]).reshape(-1, 1)
    G3 = np.array([n.G3 for n in bomba]).reshape(-1, 1)
    
    return G3, R3_0, bomba

def f_bomba_transitorio (rede, Q, dt, T, n_rotacao, bomba_manobra, bomba, nTubo, nValvula, nBomba):
    
    for i in range(nBomba):
        if (abs(Q[nTubo+nValvula+i]) > 0):            
            if i == bomba_manobra:
                bomba[i].rotacao = n_rotacao[int(T/dt)]  
                
            bomba[i].G3 = (-bomba[i].coef_A/abs(Q[nTubo+nValvula+i])*(bomba[i].rotacao)**2 + (bomba[i].coef_B)*abs(Q[nTubo+nValvula+i]))     
        else:
            bomba[i].G3 = 10**-8
            
    G3 = np.array([n.G3 for n in bomba]).reshape(-1, 1)
    
    return G3, bomba
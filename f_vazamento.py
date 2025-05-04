# -*- coding: utf-8 -*-
"""
Created on Sat Sep  2 10:35:00 2023

@author: RUI GABRIEL
"""

# IMPORTAÇÃO DAS BIBLIOTECAS PRINCNIPAIS
import numpy as np

def f_vazamento (rede, Q, no, nNo, nTubo, nValvula, nBomba):
    y = .5 # expoente da vazão
    j = 0
    for i in range(nNo):
        no[i].R4 = None
        no[i].R4_0 = None
        no[i].G4 = None
        if no[i].Cd is not None and no[i].Cd > 0:
            if abs(Q[nTubo + nValvula + nBomba + j]) > 0:
                no[i].R4 = (1/no[i].Cd)**(1/y)
                no[i].R4_0 = float(no[i].R4*abs(Q[nTubo + nValvula + nBomba + j])**(1/y-1))
                no[i].G4 = (1/y)*no[i].R4_0 # G4 = ge do manual do epanet 2.2 p. 126
                j += 1
            else:
                no[i].R4_0 = 10**-8
                no[i].G4 = 10**-8
            
        if no[i].Cd == 0:
            no[i].Cd = None

    R4_0 = np.array([n.R4_0 for n in no if n.R4_0 != None]).reshape(-1, 1)
    G4 = np.array([n.G4 for n in no if n.G4 != None]).reshape(-1, 1)
    return G4, R4_0, no

def f_vazamento_transitorio (rede, Q, no, nNo, nTubo, nValvula, nBomba):
    y = .5 # expoente da vazão
    j = 0
    for i in range(nNo):
        no[i].R4 = None
        no[i].G4 = None # Limpando as variáveis de uma possível iteração anterior
        if no[i].Cd is not None and no[i].Cd > 0:       
            if abs(Q[nTubo + nValvula + j]) > 0: 
                no[i].R4 = (1/no[i].Cd)**(1/y)
                no[i].G4 = float(no[i].R4*abs(Q[nTubo + nValvula + nBomba + j])**(1/y-1))
                j += 1            
            else:
                no[i].G4 = 10**-8
                
        if no[i].Cd == 0:
            no[i].Cd = None
                
    G4 = np.array([n.G4 for n in no if n.G4 != None]).reshape(-1, 1)
    return G4, no

        
        
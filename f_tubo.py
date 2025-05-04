# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 07:39:43 2023

@author: RUI GABRIEL
"""

# IMPORTAÇÃO DAS BIBLIOTECAS PRINCNIPAIS
import numpy as np

def f_atrito (rede, Q, tubo, nTubo):
    visc_c = 1.00*10**-6    
    for i in range(nTubo):
        tubo[i].Ktubo = 0
        if (abs(Q[i]) > 0):
            Rey = 4*abs(Q[i]) / (np.pi*tubo[i].D*visc_c)
            localizada = 8*tubo[i].Ktubo/(9.81*np.pi**2*tubo[i].D**4)
            if (tubo[i].rug < 40): # calculo do fator de atrito para Swaimee-Jain (p. 47 Hidráulica Básica - Porto)
                parc_1 = (64/Rey)**8
                parc_2 = tubo[i].rug / (3.7*tubo[i].D)
                parc_3 = 5.74 / (Rey^.9)
                parc_4 = (2500/Rey)**6
                parc_5 = np.log(parc_2 + parc_3)
                parc_6 = (parc_5-parc_4)**-16
                tubo[i].f = (parc_1 + 9.5*parc_6)**.125
                continua = (8*tubo[i].f*tubo[i].L/(9.81*np.pi**2*tubo[i].D**5))
                tubo[i].R1 = continua + localizada
                tubo[i].R1_0 = tubo[i].R1*abs(Q[i])
                tubo[i].G1 = 2*tubo[i].R1_0
            if (tubo[i].rug >= 40):
                # tubo[i].f = 1033.55*(Rey**-.148) / ((tubo[i].rug**1.852)*(tubo[i].D**.0184)) # Eq. Gustavo
                tubo[i].f = ((14.07*visc_c**-.08*Rey**-.08*tubo[i].D**-0.01)/(tubo[i].rug))**(1/.54) # Eq. 7 artigo Chyr Pyng Liou (1998)
                # tubo[i].f = 0.018
                continua = (8*tubo[i].f*tubo[i].L/(9.81*np.pi**2*tubo[i].D**5))
                tubo[i].R1 = continua + localizada
                tubo[i].R1_0 = tubo[i].R1*abs(Q[i])
                tubo[i].G1 = 2*tubo[i].R1_0
        else:
            tubo[i].f = 0
            tubo[i].R1 = 10^-8
            tubo[i].R1_0 = 10^-8
            tubo[i].G1 = 10^-8
            
    R1_0 = np.array([n.R1_0 for n in tubo]).reshape(-1, 1)
    G1 = np.array([n.G1 for n in tubo]).reshape(-1, 1)
    
    return G1, R1_0, tubo

def f_atrito_transitorio (rede, Q, dt, T, k_manobra, tubo_manobra, tubo, nTubo):

    visc_c = 1.00*10**-6    
    for i in range(nTubo):
        tubo[i].Ktubo = 0
        if (abs(Q[i]) > 0):
            Rey = 4*abs(Q[i]) / (np.pi*tubo[i].D*visc_c)
            if i == tubo_manobra:
                tubo[i].Ktubo = k_manobra[int(T/dt)]
                # print(f"{tubo[i].Ktubo}")
            
            localizada = 8*tubo[i].Ktubo/(9.81*np.pi**2*tubo[i].D**4)
            
            if (tubo[i].rug < 40): # calculo do fator de atrito para Swaimee-Jain (p. 47 Hidráulica Básica - Porto)
                parc_1 = (64/Rey)**8
                parc_2 = tubo[i].rug / (3.7*tubo[i].D)
                parc_3 = 5.74 / (Rey^.9)
                parc_4 = (2500/Rey)**6
                parc_5 = np.log(parc_2 + parc_3)
                parc_6 = (parc_5-parc_4)**-16
                tubo[i].f = (parc_1 + 9.5*parc_6)**.125
                continua = (8*tubo[i].f*tubo[i].L/(9.81*np.pi**2*tubo[i].D**5))
                tubo[i].R1 = continua + localizada
                tubo[i].R1_0 = tubo[i].R1*abs(Q[i])
                tubo[i].G1 = tubo[i].R1_0 - tubo[i].I/dt
            if (tubo[i].rug >= 40):
                tubo[i].f = ((14.07*visc_c**-.08*Rey**-.08*tubo[i].D**-0.01)/(tubo[i].rug))**(1/.54) # Eq. 7 artigo Chyr Pyng Liou (1998)
                continua = (8*tubo[i].f*tubo[i].L/(9.81*np.pi**2*tubo[i].D**5))
                tubo[i].R1 = continua + localizada
                tubo[i].R1_0 = tubo[i].R1*abs(Q[i])
                tubo[i].G1 = tubo[i].R1_0 - tubo[i].I/dt
        else:
            tubo[i].G1 = np.array([-tubo[i].I/dt])
            
    G1 = np.array([n.G1 for n in tubo]).reshape(-1, 1)

    return G1, tubo
                
            
                
            
    
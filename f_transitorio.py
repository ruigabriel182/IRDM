# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 15:33:14 2023

@author: RUI GABRIEL
"""

# IMPORTAÇÃO DAS BIBLIOTECAS PRINCNIPAIS
import numpy as np
import time

# IMPORTAÇÃO DOS MÓDULOS DE SUPORTE
import f_tubo as ft
import f_valvula as fv
import f_bomba as fb
import f_vazamento as fl

start_time = time.time()
def regime_transitorio(rede, Qpermanente, A10, A12, A21, D, H0, no_idx_vazamento, dt, 
                       t_simulacao, k_manobra, tubo_manobra, n_rotacao, bomba_manobra, 
                       nTubo, nNo,nRNF, nRNV, nValvula, nBomba, tubo, no, rnf, valvula, bomba):
 
    Q = Qpermanente
    
    # MATRIZ B
    B1 = np.array([n.I/dt for n in tubo]).reshape(-1, 1)
    B2 = np.zeros((nValvula, 1))
    B3 = np.zeros((nBomba, 1))
    B4 = np.zeros((len(no_idx_vazamento),1))
    B_vetor = np.concatenate((B1, B2, B3, B4), axis=0)
    B = np.diagflat(B_vetor)
    
    # MATRIZ NULA 
    Z = np.zeros((len(A21),len(A12[0])))
    
    # MATRIZ AA
    AA = np.block([[B, A12], [A21, Z]])  # Montagem da Matriz do sistema (Fixa)
    
    # MATRIZ BB0
    BB0 = np.dot(A10, H0)
    
    #CALCULO DO REGIME TRANSITÓRIO
    Qcal = np.zeros_like(Q)
    Hcal = np.zeros(nNo)
    Hcal_lista = []
    Qcal_lista = []
    Hcal_lista.append(Hcal)
    Qcal_lista.append(Q)
    T = 0
    
    # VARIÁVEIS DE ENTRADA PELO USUÁRIO
    while T < t_simulacao:
               
        # MATRIZ A11  - MATRIZ COM AS PERDAS DE CARGA
        G1, tubo = ft.f_atrito_transitorio (rede, Q, dt, T, k_manobra, tubo_manobra, tubo, nTubo)
        G2, valvula = fv.f_valvula_transitorio (rede, Q, valvula, nTubo, nValvula)
        G3, bomba = fb.f_bomba_transitorio(rede, Q, dt, T, n_rotacao, bomba_manobra, bomba, nTubo, nValvula, nBomba)
        G4, no = fl.f_vazamento_transitorio (rede, Q, no, nNo, nTubo, nValvula, nBomba)
        G_vetor = np.concatenate((G1, G2, G3, G4), axis=0)
        G = np.diagflat(G_vetor)
        
        # MATRIZ BB
        BB1 = -np.dot(G, Q) - BB0  # Monta a parte superior do vetor de solução
        BB = np.concatenate((BB1, D), axis=0)  # Monta o vetor de solução
        
        # RESOLUÇÃO
        XX = np.linalg.solve(AA, BB)  # Resolve o sistema de equações
        
        # RESULTADOS
        Qcal = XX[:len(Q)]  # Obtém a vazão do vetor de incógnitas
        Hcal = XX[len(Q):]  # Obtém carga do vetor de incógnitas
    
        # SALVA O VALOR DA VAZÃO PARA A PROXIMA ITERAÇÃO
        Q = Qcal
        Qcal_lista.append(Qcal)
        Hcal_lista.append(Hcal)        
        T = T + dt
        # print(f"{n_rotacao[int(T/dt)]}")
        
    return Qcal_lista, Hcal_lista
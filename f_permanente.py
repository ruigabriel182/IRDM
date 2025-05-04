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
def regime_permanente(rede, nTubo, nNo, nRNF, nRNV, nValvula, nBomba, tubo, no, rnf, valvula, bomba):
              
    # VARIÁVEIS DE ENTRADA PELO USUÁRIO
    conv_erro = 10**-12 # Tolerância do erro numérico na solução da rede (somatório de vazões)
    
    Qtubo = np.array([n.Qi for n in tubo]) # Chute para v = 1 m/s = área do tubo
    Qvalvula =  np.array([n.Qi for n in valvula]) # Chute para v = 1 m/s = área da vávlvula
    Qbomba =  np.array([n.QBEP for n in bomba])
    indices_zero = [i for i, n in enumerate(no) if n.Cd == 0]
    
    # Altera os valores correspondentes para None
    for idx in indices_zero:
        no[idx].Cd = None # Da erro quando ta com zero, logo, to atribuindo como None 
        
    no_idx_semvazamento = [i for i, n in enumerate(no) if n.Cd == None] # Nós que não tem CD para retirar dos trechos e reservatórios fictícios   
    no_idx_vazamento = [i for i, n in enumerate(no) if n.Cd != None] # Nós que tem CD
    Qvazamento = np.array([10/1000 for n in no if n.Cd != None and n.Cd > 0]) # Chute de 1 L/s para os nós que possuem Cd
    Q = np.concatenate((Qtubo, Qvalvula, Qbomba, Qvazamento)).reshape(-1, 1) # Adotando a vazão inicial para inicializar as variáveis
    
    
    # MATRIZ A12 - MATRIZ COM AS CARGAS DOS NOS (JUNÇÕES) / MATRIZ A10 - MATRIZ COM AS CARGAS FIXA (RNF)
    N1_idx = [n.N1_index for n in tubo] # index nó de inicio
    N2_idx = [n.N2_index for n in tubo] # index nó de fim
    RNF_idx = [n.index for n in rnf] # index RNF
    A12 = np.zeros((nTubo + nValvula + nBomba + nNo - np.size(no_idx_semvazamento),nNo), dtype=int) # +nValvula + nNo por causa dos links virtuais do vazameneto
    A10 = np.zeros((nTubo + nValvula + nBomba + nNo - np.size(no_idx_semvazamento), nRNF + nNo - np.size(no_idx_semvazamento)), dtype=int)
    for i in range(nTubo): # Para os tubos e reservatórios e RNF
        if N1_idx[i] <= (nNo-1):
            A12[i, N1_idx[i]] = -1
        else:
            A10[i,RNF_idx.index(N1_idx[i])] = -1
            # print(f"\nAviso: Tubo {tubo[i].ID} tem nó de início conectado à um reservatório/tanque.")        
        if N2_idx[i] <=(nNo-1):
            A12[i, N2_idx[i]] = 1
        else:
            A10[i,RNF_idx.index(N2_idx[i])] = 1
            # print(f"\nAviso: Tubo {tubo[i].ID} tem nó de fim conectado à um reservatório/tanque.") 
    
    N1_idx_valvula = [n.N1_index for n in valvula] # index nó de inicio
    N2_idx_valvula = [n.N2_index for n in valvula] # index nó de fim
    for i in range(nValvula): # Para as válvulas
        if N1_idx_valvula[i] <= (nNo-1):
            A12[nTubo + i, N1_idx_valvula[i]] = -1
        else:
            A10[nTubo + i,RNF_idx.index(N1_idx_valvula[i])] = -1
            # print(f"\nAviso: Válvula {valvula[i].ID} tem nó de início conectado à um reservatório/tanque.")        
        if N2_idx_valvula[i] <=(nNo-1):
            A12[nTubo + i, N2_idx_valvula[i]] = 1
        else:
            A10[nTubo + i,RNF_idx.index(N2_idx_valvula[i])] = 1
            # print(f"\nAviso: Válvula {valvula[i].ID} tem nó de fim conectado à um reservatório/tanque.") 
            
    N1_idx_bomba = [n.N1_index for n in bomba] # index nó de inicio
    N2_idx_bomba = [n.N2_index for n in bomba] # index nó de fim
    for i in range(nBomba): # Para as bombas
        if N1_idx_bomba[i] <= (nNo-1):
            A12[nTubo + nValvula + i, N1_idx_bomba[i]] = -1
        else:
            A10[nTubo + nValvula + i,RNF_idx.index(N1_idx_bomba[i])] = -1
            # print(f"\nAviso: Bomba {bomba[i].ID} tem nó de início conectado à um reservatório/tanque.")        
        if N2_idx_bomba[i] <=(nNo-1):
            A12[nTubo + nValvula + i, N2_idx_bomba[i]] = 1
        else:
            A10[nTubo + nValvula + i, RNF_idx.index(N2_idx_bomba[i])] = 1
            # print(f"\nAviso: Bomba {bomba[i].ID} tem nó de fim conectado à um reservatório/tanque.") 
            
    for i in range (nNo-np.size(no_idx_semvazamento)):
        A12[nTubo + nValvula + nBomba + i, no_idx_vazamento[i]] = -1
        A10[nTubo + nValvula + nBomba + i, nRNF + i] = 1
    
    # MATRIZ A21 - MATRIZ COM AS VAZÕES (TUBOS)
    A21 = A12.T # Matriz A21 é transposta de A12 
    
    # MATRIZ D - MATRIZ COM AS DEMANDA DOS NÓS (JUNÇÕES)
    D = np.array([n.demanda for n in no]).reshape(-1, 1)
    
    # MATRIZ H0 - MATRIZ COM OS VALORES DAS CARGAS FIXAS (RNF)
    carga_RNF = np.array([n.cota for n in rnf])
    z_no = np.array([n.cota for n in no if n.Cd != None])
    H0 = np.concatenate((carga_RNF, z_no), axis=0).reshape(-1, 1)
    
    #CALCULO DO REGIME PERMANENTE
    erro = 10000000000000
    max_iteracoes = 1000
    Qcal = np.zeros_like(Q)
    Hcal = np.zeros(nNo)
    Hcal_lista = []
    Qcal_lista = []
    erro_lista = []
    Hcal_lista.append(Hcal)
    Qcal_lista.append(Q)
    i = 0
    while True:
        
        # MATRIZ A11  - MATRIZ COM AS PERDAS DE CARGA
        G1, R1_0, tubo = ft.f_atrito(rede, Q, tubo, nTubo)
        G2, R2_0, valvula = fv.f_valvula(rede, Q, valvula, nTubo, nValvula)
        G3, R3_0, bomba = fb.f_bomba(rede, Q, bomba, nTubo, nValvula, nBomba)
        G4, R4_0, no = fl.f_vazamento(rede, Q, no, nNo, nTubo, nValvula, nBomba)
        A11_0_vetor = np.concatenate((R1_0, R2_0, R3_0, R4_0), axis=0)
        A11_0 = np.diagflat(A11_0_vetor)
    
        # MATRIZ D11
        D11_vetor = np.concatenate((G1, G2, G3, G4), axis=0)
        D11 = np.diagflat(D11_vetor)
        D11_inv = np.linalg.inv(D11)
        # print(f'\n Matriz G: \n{G_vetor}')
        
        # MATRIZ A
        A = A21 @ D11_inv @ A12 # Eq.10 p. 3 pdf do artigo Todini e Rossman (2021)
        A_inv = np.linalg.inv(A)
        
        # MATRIZ F
        F = A21 @ D11_inv @ ((D11 - A11_0) @ Q - A10 @ H0) - D # Eq.11 p. 3 pdf do artigo Todini e Rossman (2021)
        
        # CARGAS CALCULADAS
        Hcal = A_inv @ F # Eq.9 p. 3 pdf do artigo Todini e Rossman (2021)
        
        # CALCULA AS VAZÕES
        Qcal = Q - D11_inv @ (A11_0 @ Q + A12 @ Hcal + A10 @ H0) # Eq.9 p. 3 pdf do artigo Todini e Rossman (2021)
        
        # SALVA O VALOR DA VAZÃO PARA A PROXIMA ITERAÇÃO
        Q = Qcal
        Qcal_lista.append(Qcal)
        Hcal_lista.append(Hcal)
        
        # CALCULO DO ERRO
        erro = sum(Qcal_lista[-1] - Qcal_lista[-2]) / sum(Qcal_lista[-2]) # Balanço de massa (Q-D) # Critério de parada adotado no EPANET 2.2 e demonstrado no artigo Todini e Rossman (2021)
        erro_lista.append(erro)
        
        i += 1
        if conv_erro >= abs(erro) or i >= max_iteracoes:
            break
        
    return Qcal_lista, Hcal_lista, A10, A12, A21, D, H0, no_idx_vazamento
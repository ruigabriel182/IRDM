# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 07:37:24 2023

@author: RUI GABRIEL
"""
# IMPORTAÇÃO DAS BIBLIOTECAS PRINCNIPAIS
import numpy as np
from classTubo import class_Tubo
from classNo import class_No
from classRNF import class_RNF
from classValvula import class_Valvula
from classBomba import class_Bomba

# FUNÇÃO PARA COLETAR OS DADOS INICIAIS DA REDE
def numero_dados (rede):
    nTubo = rede.num_pipes
    nNo = rede.num_junctions
    nRNF = rede.num_reservoirs  
    nRNV = rede.num_tanks
    nValvula = rede.num_valves
    nBomba = rede.num_pumps
    return nTubo, nNo, nRNF, nRNV, nValvula, nBomba

# COLETA DE DADOS
def coletar_dados(rede):
    
    
# FUNÇÃO PARA CRIAR A LISTA DE TUBOS, NOS, RNF...
    nTubo, nNo, nRNF, nRNV, nValvula, nBomba = numero_dados(rede)
    tubo = [class_Tubo() for _ in range(nTubo)]
    no = [class_No() for _ in range(nNo)]
    rnf = [class_RNF() for _ in range(nRNF)]
    valvula = [class_Valvula() for _ in range(nValvula)]
    bomba = [class_Bomba() for _ in range (nBomba)]
    
# COLETA DE DADOS PARA OS TUBOS
    opcoes_hidraulica = rede._options.hydraulic
    unidade_headloss = opcoes_hidraulica.headloss
    
    if unidade_headloss == 'H-W':
        converte_rug = 1
    elif unidade_headloss == 'D-W':
        converte_rug = 1000
    
    tubo_ID = rede.link_name_list
    no_ID = rede.node_name_list
    for i in range(nTubo):
        #print(f"Tubo {i + 1} de {nTubo}")
    
        atributo_tubo = rede.get_link(tubo_ID[i])
        tubo[i].ID = tubo_ID[i] 
        tubo[i].index = i
        tubo[i].N1_ID = atributo_tubo.start_node_name
        tubo[i].N2_ID = atributo_tubo.end_node_name
        tubo[i].N1_index = no_ID.index(tubo[i].N1_ID)
        tubo[i].N2_index = no_ID.index(tubo[i].N2_ID)
        tubo[i].L = atributo_tubo.length
        tubo[i].D = atributo_tubo.diameter
        tubo[i].area = tubo[i].D**2 * np.pi/4
        tubo[i].rug = atributo_tubo.roughness/converte_rug
        tubo[i].status = atributo_tubo._initial_status.value
        tubo[i].Ktubo = atributo_tubo.minor_loss
        tubo[i].Qi = tubo[i].area # Vazão inicial (chute) para uma velocidade de 1 m/s (Q = A*V = Q = A)
        tubo[i].I = tubo[i].L/(9.81*tubo[i].area)
    
# COLETA DE DADOS PARA OS NOS (JUNÇÕES)
    opcoes_hidraulica = rede._options.hydraulic
    unidade_vazao = opcoes_hidraulica.inpfile_units

    if unidade_vazao == 'CMH':
        converte_vazao = 3600
    elif unidade_vazao == 'LPS':
        converte_vazao = 1000    

    no_ID = rede.node_name_list
    for i in range(nNo):
       #print(f"No {i + 1} de {nNo}")
       
       atributo_no = rede.get_node(no_ID[i])
       no[i].ID = no_ID[i]
       no[i].index = i
       no[i].demanda = atributo_no.base_demand
       no[i].Cd = atributo_no.emitter_coefficient
       no[i].cota = atributo_no.elevation
       no[i].x = atributo_no._coordinates[0]
       no[i].y = atributo_no._coordinates[1]
       
       
# COLETA DE DADOS PARA OS RESERVATÓRIOS (RNF)
    no_ID = rede.node_name_list
    rnf_ID = rede.reservoir_name_list
    for i in range(nRNF):
        #print(f"RNF {i + 1} de {nRNF}")
        
        atributo_RNF = rede.get_node(rnf_ID[i])
        rnf[i].ID = rnf_ID[i]
        rnf[i].index = no_ID.index(rnf[i].ID)
        rnf[i].cota = atributo_RNF.base_head
        rnf[i].x = atributo_no._coordinates[0]
        rnf[i].y = atributo_no._coordinates[1]
        
# COLETA DE DADOS PARA AS VÁLVULAS
    link_ID = rede.link_name_list
    valvula_ID = rede.valve_name_list
    for i in range(nValvula):
        #print(f"Valvula {i + 1} de {nValvula}")
        
        atributo_valvula = rede.get_link(valvula_ID[i])
        valvula[i].ID = valvula_ID[i]
        valvula[i].index = link_ID.index(valvula[i].ID)
        valvula[i].N1_ID = atributo_valvula.start_node_name
        valvula[i].N2_ID = atributo_valvula.end_node_name
        valvula[i].N1_index = no_ID.index(valvula[i].N1_ID)
        valvula[i].N2_index = no_ID.index(valvula[i].N2_ID)
        valvula[i].D = atributo_valvula.diameter
        valvula[i].area = valvula[i].D**2 * np.pi/4
        valvula[i].Kvalvula = atributo_valvula.setting # Tomar cuidado. Na TCV não importa o valor de loss coef, apenas do setting
        valvula[i].status = str(atributo_valvula.status) # Closed (0), Open (1), Active (2)
        valvula[i].tipo = atributo_valvula.valve_type
        valvula[i].setting = atributo_valvula.setting
        valvula[i].Qi = valvula[i].area # Vazão inicial (chute) para uma velocidade de 1 m/s (Q = A*V = Q = A)
        
# COLETA DE DADOS PARA AS BOMBAS
    bomba_ID = rede.pump_name_list
    for i in range(nBomba):
        atributo_bomba = rede.get_link(bomba_ID[i])
        curva = rede.get_curve(atributo_bomba.pump_curve_name)
        bomba[i].ID = bomba_ID[i]
        bomba[i].index = link_ID.index(bomba[i].ID)
        bomba[i].N1_ID = atributo_bomba.start_node_name
        bomba[i].N2_ID = atributo_bomba.end_node_name
        bomba[i].N1_index = no_ID.index(bomba[i].N1_ID)
        bomba[i].N2_index = no_ID.index(bomba[i].N2_ID)
        bomba[i].rotacao = atributo_bomba.initial_setting if isinstance(atributo_bomba.initial_setting, float) else 1
        bomba[i].HBEP = curva.points[0][1]
        bomba[i].QBEP = curva.points[0][0]
        additional_points = [(0, 4/3 * bomba[i].HBEP), (2 * bomba[i].QBEP, 0)]
        curva_points = curva.points + additional_points
        H_points = [point[1] for point in curva_points]
        Q_points = [point[0] for point in curva_points] # Em m³/s igual o epanet
        coef = np.polyfit(Q_points, H_points , 2)
        bomba[i].coef_A = abs(coef[2])
        bomba[i].coef_B = abs(coef[0])
        
    return tubo, no, rnf, valvula, bomba
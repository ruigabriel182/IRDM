# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 07:50:06 2023

@author: RUI GABRIEL
"""

# CLASSE PARA REPRESENTAR OS DADOS DAS TUBULAÇÕES
class class_Tubo:
    def __init__(self):
        self.ID = None
        self.index = None
        self.N1_ID = None
        self.N2_ID = None
        self.N1_index = None
        self.N2_index = None
        self.L = None
        self.D = None
        self.area = None
        self.rug = None
        self.status = None
        self.Ktubo = 0
        self.f = None
        self.Qi = None
        self.Q = None
        self.R1 = None
        self.R1_0 = None
        self.G1 = None
        self.I = None
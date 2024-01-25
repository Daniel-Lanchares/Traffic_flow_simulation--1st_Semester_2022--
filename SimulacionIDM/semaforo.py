#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 23 09:39:29 2021
"""

class Semaforo:
    def __init__(self, segs_señal, config={}):
        # Añadir las carreteras como atributo del semáforo
        self.segs_señal = segs_señal
        # Configuración predeterminada
        self.config_predet()
        # Actualiza la configuración con los valores dados
        for attr, val in config.items():
            setattr(self, attr, val)
        # Añade semáforos a las carreteras
        self.init_properties()

    def config_predet(self):
         #Ciclo típico para una intersección de un carril
         #Las tuplas tienen que tener tantos elementos como carreteras en segs_señal
        self.ciclo = [(False, True), (True, False)] 
        self.distancia_frenado = 50
        self.factor_frenado = 0.4
        self.distancia_detencion = 15
        self.longitud_ciclo = [30, 30]
        self.pos = 2 #Metros desde el final de la carretera

        self.ind_ciclo_actual = 0

        self.ultimo_t = 0

    def init_properties(self):
        for i in range(len(self.segs_señal)):
            for seg_señal in self.segs_señal[i]:
                seg_señal.crea_señal(self, i)

    #Devuelve el ciclo en un momento dado
    @property #La definimos como propiedad que podemos modificar
    def ciclo_actual(self):
        return self.ciclo[self.ind_ciclo_actual]
    '''
    #Rutina de actualización
    def actualiza(self, sim):
        k = (sim.t // self.longitud_ciclo[self.ind_ciclo_actual]) % len(self.ciclo)
        print(sim.t // self.longitud_ciclo[self.ind_ciclo_actual])
        self.ind_ciclo_actual = int(k)
        print(self.ind_ciclo_actual)
        '''
    def actualiza(self,sim):
        if sim.t-self.ultimo_t >= self.longitud_ciclo[self.ind_ciclo_actual]:
            self.ind_ciclo_actual = (self.ind_ciclo_actual + 1) % len(self.ciclo)
            self.ultimo_t = sim.t
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 23 09:41:16 2021
"""

from .vehiculo import Vehiculo
from numpy.random import randint

class Generador_vehiculos:
    def __init__(self, sim, config={}):
        self.sim = sim

        # Configurar
        self.config_predet()

        # Actualizar configuración (nos permite personalizar las clases)
        for attr, val in config.items():
            setattr(self, attr, val)

        # Propiedades inprescindibles para la clase (Arquitectura común)
        self.init_prop()

    def config_predet(self):
        self.ritmo_generacion = 20 #Vehículos/minuto
        self.vehiculos = [
            (1, {})
        ]
        self.t_ultima_generacion = 0

    def init_prop(self):
        '''
        Genera el primer vehículo
        '''
        self.siguiente_vehiculo = self.genera_vehiculo()

    def genera_vehiculo(self):
        '''
        Genera un vehículo de entre las posibilidades en función de los pesos
        '''
        total = sum(pareja[0] for pareja in self.vehiculos) #Peso total
        r = randint(1, total+1) #Como r < total+1 garantizamos una generación.
        for (peso, config) in self.vehiculos:
            r -= peso #Mayor el peso, mayor la probabilidad de que r-peso <= 0
            if r <= 0:
                return Vehiculo(config)

    def actualiza(self):
        '''
        Añade los vehículos creados
        '''
        if self.sim.t - self.t_ultima_generacion >= 60 / self.ritmo_generacion:
            # Si el tiempo transcurrido desde la última generación es
            # mayor que T_generación (60/ritmo en segundos): Añade el vehículo
            seg = self.sim.segs[self.siguiente_vehiculo.ruta[0]]      
            if len(seg.vehiculos) == 0\
               or seg.vehiculos[-1].x > self.siguiente_vehiculo.s0 + self.siguiente_vehiculo.l:
                # Si el segmento está vacío o hay hueco para generarlo
                self.siguiente_vehiculo.t_creacion = self.sim.t
                seg.vehiculos.append(self.siguiente_vehiculo)
                # Resetear los valores de última y próxima generación
                self.t_ultima_generacion = self.sim.t
            self.siguiente_vehiculo = self.genera_vehiculo()
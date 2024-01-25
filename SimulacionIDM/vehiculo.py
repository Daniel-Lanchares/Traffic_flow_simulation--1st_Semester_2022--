#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 23 09:12:49 2021
"""
import vpython as vp
import numpy as np
from .simulacion import *

class Vehiculo:
    def __init__(self, config={}): #Función que se ejecuta al crear un vehículo
        # configuración estándar
        self.config_predet()

        # Este bucle itera sobre los atributos ya declarados, permitiendo reescribirlos  
        for attr, val in config.items():
            setattr(self, attr, val)

        # Cálculo de propiedades útiles
        self.init_prop()

    def config_predet(self):   
        #Parámetros fijos
        self.l = 4               #Longitud del vehículo (m)
        self.h = 2               #Anchura (m)
        self.w = 1.5             #Altura(m)
        self.color=vp.color.red  #Color
        
        self.s0 = 2              #Distancia mínima deseada (m)
        self.T = 1               #Tiempo de reacción (s)¿?
        self.v_max = 16.6        #Velocidad máxima (m/s)
        self.a_max = 2.44        #Aceleración máxima (m/s2)
        self.b_max = 4.61        #Deceleración máxima deseada (m/s2)
        self.d = 4               #Coeficiente de agresividad (Aceleración más o menos brusca)

        #Integración con carreteras
        self.trayecto_circular= False
        self.ruta = []
        self.ind_seg_actual = 0

        #Atributos Variables
        self.x = 0               #Posición (m)
        self.v = self.v_max      #Velocidad (m/s)
        self.a = 0               #Aceleracción (m/s2)
        self.parado = False     #Atributo: Parado
        self.sin_pintar= True   #Para crear el objeto de vpython una sola vez por carretera

    def init_prop(self):
        #Propiedades variables que dependen de parámetros configurables
        self.sqrt_ab = 2*np.sqrt(self.a_max*self.b_max)
        self._v_max = self.v_max #Velocidad máxima de referencia (Ésta nunca será alterada, sólo usada para recuperar el valor original)
        
    def vp_vect(self, vec):#convierte lista o tupla en vector de vpython (V-vectores)
        vect=vp.vector(vec[0],vec[1],vec[2])
        return vect

    def vp_coche(self, vprin, vfin): #pinta rectángulos dada la carretera (SÓLO ACEPTA V-VECTORES)
        if self.sin_pintar:
            self.coche = vp.box(pos=(self.x*(vfin-vprin)/vp.mag(vfin-vprin) + vprin)+0.7*vp.vector(0,0,1), 
                                length=self.l, axis=(vfin-vprin), height=self.h, width=self.w, color=self.color)
            self.sin_pintar= False
        else:
            self.coche.pos=(self.x*(vfin-vprin)/vp.mag(vfin-vprin) + vprin)+0.7*vp.vector(0,0,1)
        return self.coche

    def actualiza(self, lider, dt):
        # Actualiza v y x por método de Euler
        if self.v + self.a*dt < 0: 
            #Precide velocidad negativa (No contemplado) y fuerza detención
            self.x -= 1/2*self.v*self.v/self.a
            self.v = 0
        else: #Aplicar el método de integración de Euler
            self.v += self.a*dt
            self.x += self.v*dt + self.a*dt*dt/2
        
        # Actualiza aceleración: Implementación del modelo IDM
        s = 0 #Distancia deseada/Distancia actual
        if lider: #Si el vehículo ya es el líder, esto no se ejecuta
            delta_x = lider.x - self.x - lider.l
            delta_v = self.v - lider.v

            s = (self.s0 + max(0, self.T*self.v + delta_v*self.v/self.sqrt_ab)) / delta_x 
            #Aseguramos S >= s0/delta_x

        self.a = self.a_max * (1-(self.v/self.v_max)**self.d - s**2) #Modelo IDM

        if self.parado: 
            self.a = -self.b_max*self.v/self.v_max
        
    def para(self):
        self.parado = True

    def arranca(self):
        self.parado = False

    def frena(self, v):
        self.v_max = v

    def deja_frenar(self):
        self.v_max = self._v_max



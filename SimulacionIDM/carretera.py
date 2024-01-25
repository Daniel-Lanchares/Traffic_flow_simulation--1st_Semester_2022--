#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 23 09:37:45 2021
"""
from scipy.spatial import distance
from collections import deque
import vpython as vp
import numpy as np

'''
IMPLEMNTAR: variar el color de la calzada según la densidad de tráfico: Según n en actualiza
'''

class Carretera: #Principio y final serán siempre tuplas, salvo para converir a vp.vector 
    def __init__(self, prin, fin, indice='unknown', config={}):
        self.prin = prin
        self.fin = fin
        self.longitud = distance.euclidean(self.prin, self.fin)
        self.vprin, self.vfin = self.vp_vect(vec=self.prin), self.vp_vect(vec=self.fin)
        self.indice=indice

        #Tipo especial de lista, con métodos para añadir y eliminar los extremos
        #(Coches que llegan a la carretera / la abandonan)
        self.vehiculos = deque() #Coches en la carretera 

        self.config_predet()
        
        for attr, val in config.items():
            setattr(self, attr, val)
        
        self.vmax = self.v_max/3.6   #Velocidad máxima en la carretera (m/s)
        #Renderizado
        if self.visible:
           self.vp_carretera(self.vprin, self.vfin)

    def config_predet(self):
        self.visible = True          # Permite trabajar con texturas de múltiples carriles
        self.color = vp.color.blue   # Color predeterminado
        self.fl = 12                 # Flecha cada fl unidades
        self.tiene_semaforo = False 
        self.v_max = 30              #Velocidad máxima en la carretera (km/h)
        

    def vp_vect(self, vec):
        '''
        convierte lista o tupla en vector de vpython (V-vectores)
        '''
        vect=vp.vector(vec[0],vec[1],vec[2])
        return vect

    def vp_carretera(self, prin, fin): 
        '''
        pinta rectángulos dado principio y fin, así como la señalización (SÓLO ACEPTA V-VECTORES)
        '''
        carretera = vp.box(pos=0.5*(prin+fin), length=vp.mag(prin-fin)+0.5, axis=(fin-prin), height=3, width=0.2, color=self.color) 
        for i in range(int(np.round(self.longitud/self.fl))): 
            flecha= vp.arrow(pos=prin + self.fl*i*carretera.axis/self.longitud + 0.1*vp.vector(0,0,1), axis=5*vp.hat(carretera.axis))
            etx = vp.label(pos=(flecha.pos+flecha.axis), text=str(self.indice), xoffset=6)
        return carretera

    def crea_señal(self, semaforo, grupo):
        '''
        Añade un semáforo a la carretera
        '''
        self.semaforo = semaforo
        self.grupo_semaforo = grupo
        self.tiene_semaforo = True
        self.señal=vp.box(pos=self.vfin-self.semaforo.pos*vp.hat(self.vfin-self.vprin), 
                          axis=0.2*vp.hat(self.vfin-self.vprin), height=3, width=0.4, color=vp.color.green)

    @property
    def estado_semaforo(self): #Propiedad que se actualiza
        if self.tiene_semaforo:
            i = self.grupo_semaforo
            return self.semaforo.ciclo_actual[i]
        return True

    def actualiza(self, dt):
        n = len(self.vehiculos)

        if n > 0:
            self.vehiculos[-1].v_max=self.vmax  #Ajusta el límite de velocidad del último vehículo en llegar
            # Actualiza el primer coche (líder = None)
            self.vehiculos[0].actualiza(None, dt)
            self.vehiculos[0].vp_coche(self.vprin, self.vfin)
            # Actualiza el resto (líder = i-1, i>=1)
            for i in range(1, n):
                lider = self.vehiculos[i-1]
                self.vehiculos[i].actualiza(lider, dt)
                self.vehiculos[i].vp_coche(self.vprin, self.vfin)

        if self.tiene_semaforo:
            # Si tiene semáforo 
            if self.estado_semaforo:
                # Si está en verde deja pasar a los vehículos
                self.señal.color=vp.color.green
                if n>0: #Necesario si hay vehículos detenidos al ponerse en verde
                    self.vehiculos[0].arranca()
                    for vehiculo in self.vehiculos:
                        vehiculo.deja_frenar()
            else:
                # Si está en rojo
                self.señal.color=vp.color.red
                if n>0:
                    if self.vehiculos[0].x >= self.longitud - self.semaforo.distancia_frenado:
                        # Frena vehículos reduciendo su velociadad máxima permitida
                        self.vehiculos[0].frena(self.semaforo.factor_frenado*self.vehiculos[0]._v_max)
                    if self.vehiculos[0].x >= self.longitud - self.semaforo.distancia_detencion and\
                       self.vehiculos[0].x <= self.longitud - self.semaforo.distancia_detencion / 2:
                        # Detener los vehículos que estén a tiempo de parar para el semáforo
                        self.vehiculos[0].para()
                    #Se ha saltado el semáforo    
                    if self.vehiculos[0].x >= self.longitud: 
                        self.vehiculos[0].arranca()
                        self.vehiculos[0].deja_frenar()

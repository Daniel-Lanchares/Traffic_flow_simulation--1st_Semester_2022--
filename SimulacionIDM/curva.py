#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 23 09:36:34 2021
"""

import vpython as vp

class Curva:
    def __init__(self,prin, fin, control, resolucion, config_seg={},config_cur={}):
        
        self.config_predet()
        self.prin=prin
        self.fin=fin
        self.control=control
        self.res=resolucion
        
        # Este bucle itera sobre los atributos ya declarados, permitiendo reescribirlos  
        for attr, val in config_cur.items():
            setattr(self, attr, val)
        
        self.puntos=self.curva_bez(self.prin,self.fin,self.control,self.res, config_seg)
        
    
    def config_predet(self):
        self.controles=[]
        self.manillas=[]
        self.cont_color=vp.color.yellow
    
    def c_puntos(self, prin, fin, control, resolucion=5):
    	# Devuelve los puntos de la curva
        puntos = []
    
        for i in range(resolucion+1): #Parametrización de la curva de Bezier
            t = i/resolucion
            if len(control)==1:
                x = (1-t)**2 * prin[0] + 2*(1-t)*t * control[0][0] + t**2 *fin[0]
                y = (1-t)**2 * prin[1] + 2*(1-t)*t * control[0][1] + t**2 *fin[1]
                z = (1-t)**2 * prin[2] + 2*(1-t)*t * control[0][2] + t**2 *fin[2]
            elif len(control)==2:
                x= (1-t)**3 * prin[0] + 3*t*(1-t)**2 * control[0][0] +3*t**2*(1-t) * control[1][0] + t**3 * fin[0]
                y= (1-t)**3 * prin[1] + 3*t*(1-t)**2 * control[0][1] +3*t**2*(1-t) * control[1][1] + t**3 * fin[1]
                z= (1-t)**3 * prin[2] + 3*t*(1-t)**2 * control[0][2] +3*t**2*(1-t) * control[1][2] + t**3 * fin[2]
            puntos.append((x, y, z))
    
        return puntos
    
    def curva_bez(self, prin, fin, control, resolucion=15, config={}): #Crea la curva y convierte al formato deseado
        points = self.c_puntos(prin, fin, control, resolucion=resolucion)
        for punto in control: 
            self.controles.append(vp.sphere(pos=vp.vector(punto[0],punto[1],punto[2]), raduis=1, color= self.cont_color))
        
        self.manillas.append(vp.box(
               pos=0.5*vp.vector(control[0][0]+prin[0], control[0][1]+prin[1],control[0][2]+prin[2]), 
               axis=vp.vector(control[0][0]-prin[0], control[0][1]-prin[1],control[0][2]-prin[2]), 
               height=0.3, width=0.3, color=self.cont_color))
        
        self.manillas.append(vp.box(
               pos=0.5*vp.vector(control[-1][0]+fin[0], control[-1][1]+fin[1],control[-1][2]+fin[2]), 
               axis=vp.vector(control[-1][0]-fin[0], control[-1][1]-fin[1],control[-1][2]-fin[2]), 
               height=0.3, width=0.3, color=self.cont_color))
    	#Que muestre en la simulación la posición de los controles en la simulación
        return [(points[i-1], points[i], config) for i in range(1, len(points))]
    
    '''
    TURN_LEFT = 0
    TURN_RIGHT = 1
    def turn_road(start, end, turn_direction, resolution=15):
    	# Get control point
    	x = min(start[0], end[0])
    	y = min(start[1], end[1])
    
    	if turn_direction == TURN_LEFT:
    		control = (
    			x - y + start[1],
    			y - x + end[0]
    		)
    	else:
    		control = (
    			x - y + end[1],
    			y - x + start[0]
    		)
    	
    	return curva_bez(start, end, control, resolution=resolution)
    '''
    #Rehacer Turn_road
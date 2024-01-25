#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 21 17:15:36 2021

@author: Daniel Lanchares
"""

import vpython as vp

import SimulacionIDM as IDM

#Intersección


parada=True
def parar(b):
    global parada
    parada = not parada
    if parada: b.text='Continuar'
    else: b.text=     '   Parar   '

visibles = False
ejecutado = False
def contr_curva(b):
    global visibles
    global ejecutado
    visibles = not visibles
    ejecutado = False
    if visibles: b.text='Manillas: Ocultas'
    else: b.text='Manillas: Visibles'

def H(s):
    x=sim.camera.pos.x
    y=sim.camera.pos.y
    z=sim.camera.pos.z
    sim.camera.pos=vp.vector(x+s,y,z)

def V(s):
    x=sim.camera.pos.x
    y=sim.camera.pos.y
    z=sim.camera.pos.z
    sim.camera.pos=vp.vector(x,y+s,z)
    
simu=IDM.Simulacion({'dt':1/100,'pos_camara':vp.vector(0,5,55)})
sim = simu.sim
vp.button(text='Ejecutar', pos=sim.title_anchor, bind=parar)
vp.button(text='Manillas: Visibles', pos=sim.title_anchor, bind=contr_curva)

n = 30 #Resolución de las curvas
carr_vis=True
lista = [#Desde Turborotonda
        ((50,-2,0),(80,-2,0),{'visible': carr_vis }),        #0
        ((50,2,0),(80,2,0),{'visible': carr_vis }),          #1
        ((100,6,0),(57,6,0),{'visible': carr_vis }),         #2
        ((100,10,0),(57,10,0),{'visible': carr_vis }),       #3
        ((100,14,0),(57,14,0),{'visible': carr_vis }),       #4
        ((100,18,0),(57,18,0),{'visible': carr_vis }),       #5
        
        #Avenida del Cristo
        ((21.5,33,0),(30,71.5,0),{'visible': carr_vis }),    #6
        ((17,34,0),(25.5,72,0),{'visible': carr_vis }),      #7
        ((21,79,0),(12,35,0),{'visible': carr_vis }),        #8
        ((16.5,79,0),(8,35.5,0),{'visible': carr_vis }),     #9
        ((12.5,79,0),(4,36,0),{'visible': carr_vis }),       #10
        
        #Hermanos Pidal
        ((-18,15,0),(-80,15,0),{'visible': carr_vis }),      #11
        ((-18,11,0),(-80,11,0),{'visible': carr_vis }),      #12
        ((-80,6,0),(-32,6,0),{'visible': carr_vis,}),        #13
        ((-80,2,0),(-32,2,0),{'visible': carr_vis,}),        #14
        ((-80,-2,0),(-32,-2,0),{'visible': carr_vis }),      #15
        
        #Avenida Galicia
        ((-9.5,-15,0),(-20,-57,0),{'visible': carr_vis }),   #16
        ((-5.5,-15.5,0),(-16,-57,0),{'visible': carr_vis }), #17
        ((-11.5,-57,0),(-4,-26,0),{'visible': carr_vis }),   #18
        ((-7.5,-57,0),(0,-26.5,0),{'visible': carr_vis }),   #19
        ((-3,-57,0),(4.5,-27,0),{'visible': carr_vis }),     #20
         
        
        
        #Continuación desde Turborotonda
        ((24,-2,0),(50,-2,0),{'visible': carr_vis }),        #21
        ((20,2,0),(50,2,0),{'visible': carr_vis }),          #22
        ((57,6,0),(20,6,0),{'visible': carr_vis }),          #23
        ((57,10,0),(20,10,0),{'visible': carr_vis }),        #24
        ((57,14,0),(20,14,0),{'visible': carr_vis }),        #25
        ((57,18,0),(40,18,0),{'visible': carr_vis }),        #26
        
        *simu.crea_curva(                                #26+n Unión 26-7
                (40, 18, 0), (21.5, 33, 0), ((26, 18, 0),(20,25,0)), 
                resolucion=n, config_seg={'visible': False,'v_max':20}),
        ((20,14,0),(-18,15,0),{'visible': False}),       #27+n  Unión 25-11
        ((20,10,0),(-18,11,0),{'visible': True,'color':vp.color.orange}),       #28+n  Unión 24-12
        *simu.crea_curva(                                #28+2n  Unión 24-16
                (20,10,0), (-9.5, -15, 0), ((2, 10, 0),(-5.6,-1,0)), 
                resolucion=n, config_seg={'visible': True,'color':vp.color.orange}), 
        *simu.crea_curva(                                #28+3n  Unión 23-17
                (20,6,0), (-5.5, -15.5, 0), ((6, 6, 0),(-1.4,-1,0)), 
                resolucion=n, config_seg={'visible': False}), 
        
        *simu.crea_curva(                                #28+4n  Unión 8-22
                (12,35,0), (20, 2, 0), ((6, 10, 0),(-1.4,2,0)), 
                resolucion=n, config_seg={'visible': False}),
        *simu.crea_curva(                                #28+5n  Unión 9-21
                (8,35,0), (24, -2, 0), ((0, 6, 0),(-4.4,-2,0)), 
                resolucion=n, config_seg={'visible': False}), #,config_curv={'cont_color':vp.color.red}
        ((8,35.5,0),(-5.5,-15.5,0),{'visible':False}),   #29+5n  Unión 9-17
        *simu.crea_curva(                                #29+6n  Unión 10-11
                (4,36,0), (-18, 15, 0), ((-2, 15, 0),(-4.4,15,0)), 
                resolucion=n, config_seg={'visible': False,'v_max':20}), 
        *simu.crea_curva(                                #29+7n  Unión 13-7
                (-32,6,0), (17, 34, 0), ((2, 5, 0),(11,12,0)), 
                resolucion=n, config_seg={'visible': True,'color':vp.color.yellow}), 
        ((-32,2,0),(20,2,0),{'visible':True, 'color':vp.color.yellow}),          #30+7n  Unión 14-22
        ((-32,-2,0),(24,-2,0),{'visible':False}),        #31+7n  Unión 15-21
        *simu.crea_curva(                                #31+8n  Unión 15-16
                (-32,-2,0), (-9.5, -15, 0), ((-12, -2, 0),(-7,-5,0)), 
                resolucion=n, config_seg={'visible': False,'v_max':20}), 
        *simu.crea_curva(                                #31+9n  Unión 18-12
                (-4,-26,0), (-18, 11, 0), ((2, -2, 0),(-5,11,0)), 
                resolucion=n, config_seg={'visible': False}),
        ((0,-26.5,0),(17,34,0),{'visible':False}),       #32+9n  Unión 19-7
        ((4.5,-27,0),(21.5,33,0),{'visible':False}),     #33+9n  Unión 20-6
        *simu.crea_curva(                                #33+10n Unión 20-21
                (4.5,-27,0), (24, -2, 0), ((10, -6, 0),(16,-2,0)), 
                resolucion=n, config_seg={'visible': False,'v_max':20}),
        
        ] 


simu.crea_carreteras(lista)
#simu.roads[0].vehiculos.append(Vehiculo({'path':[0,1, *range(3, 3+n), -1]}))

simu.crea_gen({ #Coches
    'ritmo_generacion': 60,
    'vehiculos': [
        #Desde Turborotonda
        [3, {'ruta':[2,23, *range(28+2*n+1, 28+3*n+1), 17]}],
        [3, {'ruta':[3,24,28+n,12]}],
        #[3, {'ruta':[3,24,*range(28+n+1,28+2*n+1),16]}],
        [3, {'ruta':[4,25,27+n,11]}],
        [5, {'ruta':[5,26,*range(26+1,26+n+1),6]}],
        
        #Desde Avenida del Cristo
        [3, {"ruta": [8, *range(28+3*n+1,28+4*n+1),22,1]}],
        [3, {"ruta": [9, 29+5*n,17]}],
        [3, {"ruta": [9, *range(28+4*n+1,28+5*n+1),21,0]}],
        [5, {"ruta": [10, *range(29+5*n+1,29+6*n+1),11]}],
        
        #Desde Hermanos Pidal
        [3, {"ruta": [13, *range(29+6*n+1,29+7*n+1),7]}],
        [3, {"ruta": [14, 30+7*n,22,1]}],
        [3, {"ruta": [15, 31+7*n,21,0]}],
        [3, {"ruta": [15, *range(31+7*n+1,31+8*n+1),16]}],
        
        #Desde Avenida Galicia
        [3, {"ruta": [18, *range(31+8*n+1,31+9*n+1),12]}],
        [3, {"ruta": [19, 32+9*n,7]}],
        [3, {"ruta": [20, 33+9*n,6]}],
        [3, {"ruta": [20, *range(33+9*n+1,33+10*n+1),21,0]}],

    ]
})

simu.crea_gen({ #Otros vehículos
    'ritmo_generacion': 10,
    'vehiculos': [
        #Desde Turborotonda
        #[3, {'ruta':[2,23, *range(28+2*n+1, 28+3*n+1), 17]}],
        [3, {'ruta':[3,24,28+n,12], 'l': 8,'h':2.5,'color': vp.color.blue, 'a_max':2.2,'b_max':5}],
        [4, {'ruta':[3,24,28+n,12], 'l': 8,'h':2.5,'color': vp.color.blue, 'a_max':2.2,'b_max':5}],
        #[3, {'ruta':[5,26,*range(26+1,26+n+1),6]}],
        
        #Desde Avenida del Cristo
        [3, {"ruta": [8, *range(28+3*n+1,28+4*n+1),22,1],'color': vp.color.white,'a_max':2.6}], #Taxis}],
        [6, {"ruta": [9, 29+5*n,17],'color': vp.color.white,'a_max':2.6}], #Taxis}],
        #[3, {"ruta": [9, *range(28+4*n+1,28+5*n+1),21,0]}],
        #[3, {"ruta": [10, *range(29+5*n+1,29+6*n+1),11]}],
        
        #Desde Hermanos Pidal
        #[3, {"ruta": [13, *range(29+6*n+1,29+7*n+1),7]}],
        [3, {"ruta": [14, 30+7*n,22,1],'color': vp.color.white,'a_max':2.6}], #Taxis}],
        #[3, {"ruta": [15, 31+7*n,21,0]}],
        #[3, {"ruta": [15, *range(31+7*n+1,31+8*n+1),16]}],
        
        #Desde Avenida Galicia
        [3, {"ruta": [20, 33+9*n,6], 'l': 8,'h':2.5,'color': vp.color.blue,'a_max':2.2, 'b_max':5, 'v_max':12.5}],
        [2, {"ruta": [20, *range(33+9*n+1,33+10*n+1),21,0],'l': 8,'h':2.5,'color': vp.color.blue,'a_max':2.2,'b_max':5, 'v_max':12.5}],

    ]
})



#Mirar el orden en que se ejecutan los grupos
simu.crea_semaforos([[2,3,4],[5],[8,9],[10],[13,14],[15],[18,19],[20]], {
            'ciclo':[(False,False,False,True ,False,False,True ,True ),
                     (False,False,False,True ,False,False,False,False),#ciclo de espera
                     (False,True ,False,True ,True ,True ,False,False),
                     (False,True ,False,True ,False,False,False,False),#ciclo de espera
                     (False,True ,True ,True ,False,False,False,False),
                     (False,True ,False,False,False,False,False,False),#ciclo de espera
                     (True ,True ,False,False,False,False,False,False),
                     (False,False,False,False,False,False,False,False),#ciclo de espera
                     ],
            'longitud_ciclo': [12,4,10,4,8,4,12,6],
            'distancia_detencion':20})

box=vp.box(pos=vp.vector(0,0,0), size=vp.vector(190,85,0.1),texture='Inter_IDM (baja).jpg')
cont=0
dx=0.5
fps= 100#*0.5
while True:
    vp.rate(fps) 
    k = vp.keysdown() # a list of keys that are down
    if 'left' in k: H(-dx)
    if 'right' in k: H(dx)
    if 'down' in k: V(-dx)
    if 'up' in k: V(dx)
    
    if visibles and not ejecutado:
        if len(simu.curvas)>0:
            for curva in simu.curvas: 
                for manilla in curva.manillas: manilla.visible= True
                for esfera in curva.controles: esfera.visible= True
        ejecutado=True
    elif not visibles and not ejecutado:
        if len(simu.curvas)>0:
            for curva in simu.curvas: 
                for manilla in curva.manillas: manilla.visible= False
                for esfera in curva.controles: esfera.visible= False
        ejecutado=True
    
    if not parada: 
        simu.actualiza()   
        cont +=1



#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 23 09:38:50 2021
"""
''' Sin implementar

from copy import deepcopy
from .vehicle_generator import VehicleGenerator
from .traffic_signal import TrafficSignal
'''
from .curva import Curva
from .carretera import Carretera
from .semaforo import Semaforo
from .generador import Generador_vehiculos
from copy import deepcopy
import vpython as vp

class Simulacion:
    def __init__(self, config={}):
        # Configuración
        self.config_predet()

        # Actualiza la configuración con los valores dados
        for attr, val in config.items():
            setattr(self, attr, val)
        
        self.sim = vp.canvas(title='Simulación IDM',
           width=1600, height=900,
           forward=self.vista, background=vp.color.black)
        self.sim.camera.pos=self.pos_camara

    def config_predet(self):
        self.t = 0.0            # Tiempo (dt != 1)
        self.fotograma = 0      # Iteración (df = 1)
        self.dt = 1/100         # Diferencial de tiempo
        self.curvas = []        # Lista de curvas
        self.segs = []          # Lista de segmentos rectilíneos
        self.generadores = []   # Lista de generadores (de vehículos)
        self.semaforos = []     # Lista de semáforos
        
        self.pos_camara=vp.vector(0,0,0)
        self.vista= vp.vector(0,0,-1)

#Métodos de creación del resto de clases
    def crea_curva(self, prin, fin, control, resolucion, config_seg={},config_curv={}):
        curva=Curva(prin, fin, control, resolucion, config_seg, config_curv)
        self.curvas.append(curva)
        return curva.puntos    
    
    def crea_carretera(self, prin, fin, config={}, indice='desconocido'):
        '''
        Crea un segmento dados principio y final. 
        El índice corresponde a self.gens.
        '''
        seg = Carretera(prin, fin, indice, config)
        self.segs.append(seg)
        return seg

    def crea_carreteras(self, lista_carret):
        '''
        Crea segmentos dada una lista de tuplas, cada una un segmento.
        '''
        for i, tupla in enumerate(lista_carret):
            self.crea_carretera(*tupla, indice=i)

    def crea_gen(self, config={}):
        '''
        Crea un generador de vehículos con atributos personalizables.
        (E indirectamente crea también los vehículos)
        '''
        gen = Generador_vehiculos(self, config)
        self.generadores.append(gen)
        return gen

    def crea_semaforos(self, carreteras, config={}):
        '''
        Crea un semáforo con atributos personalizables.
        
        Carreteras es una lista de grupos de carreteras cuyos semáforos irán sincronizados.
        '''
        segs_señal = [[self.segs[i] for i in grupo] for grupo in carreteras]
        señal = Semaforo(segs_señal, config)
        self.semaforos.append(señal)
        return señal

#Rutina de actualización de la simulación
    def actualiza(self):
        # Actualiza las carreteras (E indirectamente los vehículos)
        for seg in self.segs:
            seg.actualiza(self.dt)

        # Actualiza los generadores
        for gen in self.generadores:
            gen.actualiza()

        # Actualiza los semáforos
        for señal in self.semaforos:
            señal.actualiza(self)

        # Comprobación de coches fuera de su segmento actual
        for seg in self.segs:
            # Si el segmento no tiene vehículos, no hay nada que comprobar
            if len(seg.vehiculos) == 0: continue
            # Seleccionamos el líder (El único que podría haberse salido)
            vehiculo = seg.vehiculos[0]
            # Comprobamos si se ha salido
            if vehiculo.x >= seg.longitud:
                # Si el vehículo no ha terminado su ruta
                if vehiculo.ind_seg_actual + 1 < len(vehiculo.ruta):
                    # Actualizar el índice del segmeno que recorre del actual al próximo
                    vehiculo.ind_seg_actual += 1
                    # Copiar y resetear posición (relativa al segmento) 
                    #y que no se ha creado su instancia de vpython
                    nuevo_vehiculo = deepcopy(vehiculo)
                    nuevo_vehiculo.sin_pintar=True
                    nuevo_vehiculo.x = 0
                    # Se añade al siguiente segmento en su ruta
                    ind_seg_siguiente = vehiculo.ruta[vehiculo.ind_seg_actual]
                    self.segs[ind_seg_siguiente].vehiculos.append(nuevo_vehiculo)
                # Si el vehículo vuelve al inicio al terminar su ruta
                elif vehiculo.trayecto_circular:
                    # Copiar y resetear posición (relativa al segmento) 
                    #y que no se ha creado su instancia de vpython
                    nuevo_vehiculo = deepcopy(vehiculo)
                    nuevo_vehiculo.sin_pintar=True
                    nuevo_vehiculo.x = 0
                    # Se añade al primer segmento de su ruta
                    nuevo_vehiculo.ind_seg_actual = 0
                    ind_seg_siguiente = vehiculo.ruta[0]
                    self.segs[ind_seg_siguiente].vehiculos.append(nuevo_vehiculo)
                    
                # Eliminar del segmento actual
                vehiculo.coche.visible = False
                del vehiculo.coche
                seg.vehiculos.popleft() 
        # Actualizar tiempo y fotograma
        self.t += self.dt
        self.fotograma += 1


    def run(self, steps):
        '''
        Otra forma de ejecutar la simulación. En Vpython se suelen fomentar más los bucles while.
        '''
        for _ in range(steps):
            self.update()

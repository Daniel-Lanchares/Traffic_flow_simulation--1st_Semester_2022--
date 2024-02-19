# Simulation components

## The simulation itself
When using the library the only object one needs to interact with is the '_Simulacion_' class, which contains all 
creation routines for elements within the simulation as well as an actualization method that will start an update 
cascade of any created element
```Python
import vpython as vp
import SimulacionIDM as IDM

simulation_config = {'dt':1/100,'pos_camara':vp.vector(0,5,55)}

simu = IDM.Simulacion(simulation_config)
sim_canvas = simu.sim
```
## Roads & curves
Under the hood, a road is little more than a collections.deque object that gets rendered as a rectangle. The deque 
contains the vehicles that pass through that segment at the given time. Since they are all one lane roads with no 
passing allowed, the first vehicle on the deque will inevitably be the first to leave the road segment, being 
blitted onto the next on its route. The update routine invokes the update routine of its vehicles and handles their 
behaviour on traffic lights (if it has them).
```Python
n = 30 # Curve resolution. Determines the number of segments and therefore their id
carr_vis=True # Whether roads are visible. Some are set visible/invisible directly
lista = [# Road list
        
        # Straight roads heading into intersections
        ((50,-2,0),(80,-2,0),{'visible': carr_vis }),        #0
        ((50,2,0),(80,2,0),{'visible': carr_vis }),          #1
        ((100,6,0),(57,6,0),{'visible': carr_vis }),         #2

        # ...

        ((57,10,0),(20,10,0),{'visible': carr_vis }),        #24
        ((57,14,0),(20,14,0),{'visible': carr_vis }),        #25
        ((57,18,0),(40,18,0),{'visible': carr_vis }),        #26
        
        # Intersection connections (both straight and curved)
        *simu.crea_curva(                                #26+n Union 26-7
                (40, 18, 0), (21.5, 33, 0), ((26, 18, 0),(20,25,0)), 
                resolucion=n, config_seg={'visible': False,'v_max':20}),
        ((20,14,0),(-18,15,0),{'visible': False}),       #27+n  Union 25-11
        ((20,10,0),(-18,11,0),{'visible': True,'color':vp.color.orange}),       #28+n  Union 24-12
        
        # ...
    
        ((4.5,-27,0),(21.5,33,0),{'visible':False}),     #33+9n  Union 20-6
        *simu.crea_curva(                                #33+10n Union 20-21
                (4.5,-27,0), (24, -2, 0), ((10, -6, 0),(16,-2,0)), 
                resolucion=n, config_seg={'visible': False,'v_max':20}),    
        ] 
simu.crea_carreteras(lista)
```

## The traffic lights 
Traffic lights are a 2-state system that follow a pre-defined cycle. Each interval on the cycle can have a custom 
length, and each individual traffic light can affect multiple road segments, as shown bellow in matrix form.
```Python
simu.crea_semaforos([[2,3,4],[5],[8,9],[10],[13,14],[15],[18,19],[20]], {
            'ciclo':[(False,False,False,True ,False,False,True ,True ),
                     (False,False,False,True ,False,False,False,False), # Waiting cycle
                     (False,True ,False,True ,True ,True ,False,False),
                     (False,True ,False,True ,False,False,False,False), # Waiting cycle
                     (False,True ,True ,True ,False,False,False,False),
                     (False,True ,False,False,False,False,False,False), # Waiting cycle
                     (True ,True ,False,False,False,False,False,False),
                     (False,False,False,False,False,False,False,False), # Waiting cycle
                     ],
            'longitud_ciclo': [12,4,10,4,8,4,12,6],
            'distancia_detencion':20})
```
## The vehicles
The 'Vehiculo' class is the one actually responsible for implementing the IDM model by having the vehicle in front 
passed to the update function as an argument, allowing us to calculate the $s$ and $s_n$ variables.
Through the configuration dictionary all IDM parameters, as well as render colour and route. With this we can model 
various kinds of vehicles one would find (regular cars, buses, taxis, etc.)
## Stochastic traffic generators
To generate a dynamic traffic environment we require some degree of randomness while maintaining overall control of 
the conditions. It is for that reason that stochastic generation is so convenient. We set up a generator by passing 
it a pool of (weight, configuration) pairings from which it will draw every 1/generation_rate seconds.
```Python
simu.crea_gen({ # Regular cars
    'ritmo_generacion': 60, # Generation rate (vehicles per minute)
    'vehiculos': [
        # From Turborotonda (right)
        [3, {'ruta':[2,23, *range(28+2*n+1, 28+3*n+1), 17]}],
        [3, {'ruta':[3,24,28+n,12]}],
        [3, {'ruta':[4,25,27+n,11]}],
        [5, {'ruta':[5,26,*range(26+1,26+n+1),6]}],
        
        # From Avenida del Cristo (top)
        [3, {"ruta": [8, *range(28+3*n+1,28+4*n+1),22,1]}],
        [3, {"ruta": [9, 29+5*n,17]}],
        [3, {"ruta": [9, *range(28+4*n+1,28+5*n+1),21,0]}],
        [5, {"ruta": [10, *range(29+5*n+1,29+6*n+1),11]}],
        
        # From Hermanos Pidal (left)
        [3, {"ruta": [13, *range(29+6*n+1,29+7*n+1),7]}],
        [3, {"ruta": [14, 30+7*n,22,1]}],
        [3, {"ruta": [15, 31+7*n,21,0]}],
        [3, {"ruta": [15, *range(31+7*n+1,31+8*n+1),16]}],
        
        # From Avenida Galicia (bottom)
        [3, {"ruta": [18, *range(31+8*n+1,31+9*n+1),12]}],
        [3, {"ruta": [19, 32+9*n,7]}],
        [3, {"ruta": [20, 33+9*n,6]}],
        [3, {"ruta": [20, *range(33+9*n+1,33+10*n+1),21,0]}],

    ]
})

simu.crea_gen({ # Other vehicles
    'ritmo_generacion': 10,
    'vehiculos': [
        # From the right
            # Buses
        [3, {'ruta':[3,24,28+n,12], 'l': 8,'h':2.5,'color': vp.color.blue, 'a_max':2.2,'b_max':5}],
        [4, {'ruta':[3,24,28+n,12], 'l': 8,'h':2.5,'color': vp.color.blue, 'a_max':2.2,'b_max':5}],
        
        # From the top
            # Taxis
        [3, {"ruta": [8, *range(28+3*n+1,28+4*n+1),22,1],'color': vp.color.white,'a_max':2.6}],
        [6, {"ruta": [9, 29+5*n,17],'color': vp.color.white,'a_max':2.6}],
        
        # From the left
            # Taxis
        [3, {"ruta": [14, 30+7*n,22,1],'color': vp.color.white,'a_max':2.6}],
        
        # From the bottom
            # Buses
        [3, {"ruta": [20, 33+9*n,6], 'l': 8,'h':2.5,'color': vp.color.blue,'a_max':2.2, 'b_max':5, 'v_max':12.5}],
        [2, {"ruta": [20, *range(33+9*n+1,33+10*n+1),21,0],'l': 8,'h':2.5,'color': vp.color.blue,'a_max':2.2,'b_max':5, 'v_max':12.5}],

    ]
})
```
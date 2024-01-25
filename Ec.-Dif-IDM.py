# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 12:04:12 2021

@author: Daniel Lanchares
"""
import numpy as np
import scipy.integrate as inte
import matplotlib.pyplot as plt

plt.rcParams['text.usetex'] = True

def IDM(t, y):
    lista=[]
    #x0,v0 = y[0], y[1]
    #lista.append(max(0,v0))
    #lista.append(a_max * (1-(v0/v_max)**d ))#- ((s0 + max(0, T*v0 + (v0-y[-1])*v0/sqrt_ab)) / (y[-2]-x0-l) )**2))
    for i in range(0,len(y),2):
        x1,v1 = y[i],y[i+1]
        lista.append(v1)
        s=(s0 + max(0, T*v1 + (v1-y[i-1])*v1/sqrt_ab))
        Dx =y[i-2]-x1-l
        if i==0: 
            Dx += long
        a= a_max * (1-( min(parmax, max(parmin,v1/v_max)) )**d - (min(parmax, max(parmin,s/Dx)) )**2)
        lista.append(a)
    
    

    return lista #Modelo

tmax=1200
v0max=4
n=50
long=1000
parmin = 0.001
parmax = 100

l=4
s0=2
T=0
a_max=2.44 #Artificialmente bajo para simular condiciones de atasco
b_max=4.61
sqrt_ab=np.sqrt(a_max*b_max)
v_max=16.6
d=4
def f(i): #Condiciones iniciales
    if i%2==0: return 1*i*(l+s0) #Separación uniforme
    else: return v0max*np.random.rand() #Velocidad aleatoria entre 0 y v0max

y0= [f(2*n-i) for i in range(2*n)] #Creamos el vector de condiciones iniciales tipo [x01,v01,x02,v02,...]

#Integración del IDM
t=np.linspace(0,tmax,3000)
z=inte.solve_ivp(IDM,(0,tmax),y0, dense_output=True, method='RK45')
#print(z.sol(np.linspace(0,tmax,200))[-3:-1])
a=plt.figure(figsize=(12,14))

plt.subplot(2,1,1)
plt.title('Estudio de Ondas cinéticas ($x(t)$ y $v(t)$)',
          fontdict={'fontsize':25})


for i in range(len(y0)//2): plt.plot(t,10e-4*z.sol(t)[2*i])#, label='x'+str(i)) #Posiciones
for i in range(3*n//4,len(y0)//2): plt.plot(t,10e-4*(z.sol(t)[2*i]+long), '--') #Posiciones (Circular)
print(z.sol(t)[-2][-1]-z.sol(t)[-4][-1])
plt.ylabel('x (km)', fontsize=18)
plt.subplot(2,1,2)

metadatos1 = (r'\begin{eqnarray*}'
             r'n&=& %2i           \\'
             r'v_0&=& %3i (km/h)   '
             r'\end{eqnarray*}'%(n,round(3.6*v_max)))

metadatos2 = (r'\begin{eqnarray*}'
             r'a &=& %3.2f (m/s^2)\\'
             r'b &=& %3.2f (m/s^2)'
             r'\end{eqnarray*}'%(a_max,b_max))
metadatos3 = (r'\begin{eqnarray*}'
             r's0 &=& %3.1f (m)\\'
             r'L &=& %3.1f (km)'
             r'\end{eqnarray*}'%(s0,long*10e-4))
metadatos4 = (r'\begin{eqnarray*}'
             r'\delta &=& %3.1f \\'
             r'T &=& %3.1f (s)'
             r'\end{eqnarray*}'%(d,T))

plt.text(175*tmax/300, 15,'Parámetros', fontsize=18)
plt.text(70*tmax/300, 10, metadatos1, fontsize=18)
plt.text(135*tmax/300, 10, metadatos2, fontsize=18)
plt.text(200*tmax/300, 10, metadatos3, fontsize=18)
plt.text(260*tmax/300, 10, metadatos4, fontsize=18)

lv_media=[]
for i in range(len(y0)//2): 
    plt.plot(t,3.6*z.sol(t)[2*i+1]) #,label='v'+str(i)) #Velocidades
    lv_media.append(3.6*z.sol(t)[2*i+1][-1])
v_media=sum(lv_media)/len(lv_media)
plt.plot(t,v_media*np.ones_like(t), 'b--', label=r'$V_{lim}$: %4.2f'%v_media)
plt.legend(fontsize=18)
plt.xlabel('t (s)', fontsize=18)
plt.ylabel('v (km/h)', fontsize=18)
#plt.legend()

#plt.legend()
plt.show()

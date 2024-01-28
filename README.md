# Traffic_flow_simulation--1st_Semester_2022--
Project from the "Numerical Methods" course. 2nd semester of the 2021/2022 school-year.

Comparison between ODE and stochastic based simulations of traffic flow. Both based on the **I**nteligent **D**river 
**M**odel (IDM from now on).

The ODEs focus on the formation of traffic waves in long, congested roads while the Vpython renderer is optimized to 
model a real-life city-center intersection.

## On the IDM 



$$
\frac{dv_n}{dt} = a\left(1-\left( \frac{v_n}{v_0} \right)^\delta-\left(\frac{s_o+v_nT+\frac{v_n\Delta v_n}{2\sqrt{ab}}}{x_{n-1}-l_{n-1}-x_n} \right)^2 \right)
$$

```{=latex}
\begin{center}
\begin{tabular}{|c|c||c|c|}
\hline
Parameters & &Variables&\\
\hline
\hline 
$a$ & Max acceleration &$x_{n-1}$&Leader's position\\
\hline
$\delta$ & Factor de Suavidad&$x_n$&Posición del vehículo\\
\hline
$v_0$ & Velocidad deseada&$v_{n}$&Velocidad del vehículo\\
\hline
$s_0$ & Distancia mínima de seguridad&$\Delta v_n$&Diferencia de velocidad con el líder\\
\hline
$T$ & Tiempo de reacción &&\\
\hline
$b$ & Deceleración deseada&&\\
\hline
$l_{n-1}$ &Longitud del líder&&\\
\hline
\end{tabular}
\end{center}
```
[//]: # (This may be the most platform independent comment
| Parameter |                  | Variable  |                   |
|:---------:|:-----------------|:---------:|:------------------|
|    $a$    | max acceleration | $x_{n-1}$ | leader's position |
)

## Traffic waves on highways
If you have a driver's licence chances are you have experienced a so-called traffic wave. A car brakes suddenly on a 
busy highway, causing the one behind to slow down to avoid a collision, which in turn causes the next to slow down a 
causes a chain reaction... TO BE CONTINUED

## City flow simulation
While the ODE model is a very computationally inexpensive way to approach this problem it cannot be easily adapted 
to more complex situations such as the inner streets of a city. As such a much simpler way is to promote the 
abstract elements of our simulation to actual objects, so we can design their interactions through the OOP paradigm.

Building upon [this work](https://towardsdatascience.com/simulating-traffic-flow-in-python-ee1eab4dd20f) and 
exchanging Pygame for Vpython, which is not only 3D but also better suited for physical simulations in general, we 
can define a stretch of road in which our vehicles will be able to move. We can recover our calculus lessons to 
implement Bézier curves a series of small straight roads _et voilà!_. Though one ought to be careful with the refresh 
rate of the renderer or will end up with blinking cars. By adjusting their handles we can create any road we might 
think of.

On the vehicles themselves, we can customize their size, colour and stats (speed, acceleration, deceleration...)
![intersection simulator](https://raw.githubusercontent.com/Daniel-Lanchares/Traffic_flow_simulation--1st_Semester_2022--/main/Pictures_&_Figures/Intersection.png?raw=true)
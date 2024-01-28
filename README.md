# Traffic_flow_simulation--1st_Semester_2022--
Project from the "Numerical Methods" course. 2nd semester of the 2021/2022 school-year.

Comparison between ODE and stochastic based simulations of traffic flow. Both based on the **I**nteligent **D**river 
**M**odel (IDM from now on).

The ODEs focus on the formation of traffic waves in long, congested roads while the Vpython renderer is optimized to 
model a real-life city-center intersection.

## On the IDM 

When simulating traffic microscopically, what interests us is the relationship of each vehicle with its
environment, and specifically with the vehicle just in front. In the absence of vehicles, a driver will try to go to the
highest speed at which it feels comfortable ($v_0$), so long as the road or vehicle allows it. It will try to 
reach that speed by progressively decelerating from the desired maximum acceleration ($a$). The speed 
with which it decelerates depends on the smoothness factor ($\delta$), associated inversely with the 
aggressiveness of the driver. In this regime the driver will accelerate until reaching his desired maximum speed 
following a curve similar to the logistic (identical at $\delta = 1$), as can be deduced from the following 
differential equation:

$$
\frac{d}{dt}  v_{n(\textrm{leader})} = a \left( 1 - \left( \frac{v_n}{v_0} \right)^{\delta} \right)
$$


Naturally, when a vehicle encounters traffic it is forced to decelerate. In this other regime, the velocity is 
less than $v_0$, which raised to $\delta$ takes the velocity division term to $0$. The acceleration then becomes:

$$
\frac{d}{dt}  v_{n(\textrm{follower})} = a \left( 1 - \left( \frac{s(v_n,\Delta v_n)}{s_n}\right)^{2} \right)
$$

With $s(v_n,\Delta v_n)$ the desired net distance between vehicles, which is a function of both the speed of the 
leader and the follower and changes at each instant of $t$. This translates into a chasing behavior while maintaining 
distance, since the acceleration is positive if $s \lt s_n$ and negative if $s \gt s_n$. It should be noted that 
$s_n$ is not the position of the nth vehicle, but the distance between vehicles $n-1$ and $n$, taking into account the 
length of $n-1$.

$$
\begin{align}
s(v_n,\Delta v_n) &= s_o+v_nT+\frac{v_n\Delta v_n}{2\sqrt{ab}} \label{s(v)}\\
s_n & = x_{n-1}-l_{n-1}-x_n
\end{align}
$$

The previous equation shows the function $s$ explicitly. The first term corresponds to the minimum safety distance 
($s_0$), the second to speed multiplied by reaction time, $T$ (That is, the distance traveled from the moment a 
possible event occurred until the reaction by the driver) and the third and last term is associated with the 
deceleration at a rate between the desired ($-|b|$) and the maximum possible ($-|a|$), taking into account the 
difference in speeds $\Delta v_n = v_n - v_{n-1}$.


The intelligent driver model arises from combining both terms (taking care not to add the speeds directly but to add 
the dense traffic coefficient to the model for clear roads).

$$
\frac{dv_n}{dt} = a\left(1-\left( \frac{v_n}{v_0} \right)^\delta-\left(\frac{s_o+v_nT+\frac{v_n\Delta v_n}{2\sqrt{ab}}}{x_{n-1}-l_{n-1}-x_n} \right)^2 \right)
$$

<div align="center">

| Parameters |                               |  Variables   |                                    |
|:----------:|:------------------------------|:------------:|:-----------------------------------|
|    $a$     | Max acceleration              |  $x_{n-1}$   | Leader's position                  |
|  $\delta$  | Softness factor               |    $x_n$     | Vehicle's position                 |
|   $v_0$    | Desired velocity              |    $v_n$     | Vehicle's velocity                 |
|   $s_0$    | Minimum security <br>distance | $\Delta v_n$ | speed differential <br>with leader |
|    $T$     | Reaction time                 |              |                                    |
|    $b$     | Desired deceleration          |              |                                    |
| $l_{n-1}$  | Leader's length               |              |                                    |

</div>

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
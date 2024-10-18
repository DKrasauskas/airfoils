import math
import matplotlib.pyplot as plt
#initial conditions
rho = 1.225
S = 0.067535176
AR = 10
W = 0.662 #N
cd0 = 0.02 #typical value 
P = 5 #W
PREC = 100 #precision (higher -> more compute time)

vbegin = 1
vend = 5

aoa_begin = 1
aoa_end = 14 #typically above this airfoil stalls

class airfoil:
    # zero AOA cl, lift slope, name
    def __init__(self, c0, alpha, NAME):
        self.NAME = NAME
        self.c0 = c0
        self.alpha = alpha
        self.cl = lambda alpha : self.c0 + self.alpha * alpha 

#global paramaters
#lift
L = lambda v, cl : 0.5 * rho * v ** 2 * S * cl
# minimum cl_req for W = L
cl_req = lambda W, v : 2 * W / (rho * v ** 2 * S)
#assume e = 1
Cd = lambda c0, cl : c0 + cl ** 2 / (math.pi * 1 * AR)
#dynamic pressure
q = lambda v : 0.5 * rho * v ** 2 * S

#airfoils (as many as needed)
A = [
airfoil(0.3, 0.076667, "NACA2122"),
airfoil(-0.1, 0.11, "BR1"),
airfoil(0, 0.115, "NACA0012")
]

#computes drag curve and Thrust available, inputs -> list of airfoils, airplane Weight
def D_against_V(A, W):
    legend = []
    for airfoil in A:
        x = []
        thrust = []
        y = []
        for v in range(vbegin * PREC, vend *  PREC):
            drag = Cd(cd0, cl_req(W, v/PREC)) * q(v / PREC)
            x.append(v / PREC)
            thrust.append(P * PREC / v)
            y.append(drag)
        plt.plot(x, y)
        plt.plot(x, thrust)
        legend.append(airfoil.NAME)
    plt.legend(legend)
    plt.show()

#computes minimum velocity/aoa combination for condition W <= L, inputs - > list of airfoils, airplane Weight
def Lcurve(A, W):
    legend = []
    for airfoil in A:
        x = []     
        y = []
        for v in range(vbegin * PREC, vend* PREC):           
            for angle in range(aoa_begin * PREC, aoa_end * PREC):
                 if L(v /PREC, airfoil.cl(angle / PREC)) - W > 0 :
                     y.append(v / PREC)
                     x.append(angle / PREC)                    
                     break
            legend.append(airfoil.NAME)                 
        plt.plot(x, y, label = airfoil.NAME)
    plt.xlabel("AoA")
    plt.ylabel("min speed")
    plt.legend()
    plt.show()       
   
#main code here
#compute Lift curve for all airfoils
Lcurve(A, W)


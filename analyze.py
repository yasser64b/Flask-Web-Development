
import numpy as np
import matplotlib.pyplot as plt
import math


######################################################   BEAM    ########################################

def isOnLeftEdge(loc=0, beamLeftEdge=0, beamRightEdge=1):
    if loc==beamLeftEdge:
        return True
    return False

def isOnRightEdge(loc=0, beamLeftEdge=0, beamRightEdge=1):
    if loc==beamRightEdge:
        return True
    return False

def isOnBeam(loc=0, beamLeftEdge=0, beamRightEdge=1):
    if loc<beamLeftEdge or loc>beamRightEdge :
        return False
    else:
        return True

def supportCode(supports={'name1':['000',1]}):
    if len(supports)==0:
        return '000-000'

    elif len(supports)==1: 
        for value in supports.values():
            if value[1]==0:
                return value[0] +'-'+'000'
            else:
                return '000'+'-'+value[0]

    else:
        supCode=''
        for value in supports.values():
            supCode=supCode  + value[0]+ '-'   
        return supCode[:-1]
  
def beamCode(support_Code=''):
        beamVersionCode={
             '110-010': simple ,
             '010-110' : simple,
             '110-110' : simple,
            #  '100-110--' : simpleOverhangR ,
            #  '110-100--' : simpleOverhangL,
            #  '110-110--' : simpleOverhangL,
             '000-111': cantileverR , 
             '111-000': cantileverL , 
             '111-100': fixed_rollerL ,
             '111-010': fixed_rollerL ,
             '111-110': fixed_rollerL ,
             '100-111': fixed_rollerR ,
             '010-111': fixed_rollerR ,
             '110-111': fixed_rollerR ,
             '111-111': fixed_fixed ,
             '001-111': rotatFixed_fixed ,
             '111-001': fixed_rotatFixed ,
            #  '110-100-100': twoSpan_simple ,
            #  '100-110-100': twoSpan_simple ,
            #  '100-100-110': twoSpan_simple,
            #  '100-100-110': twoSpan_simple ,
            #  '110-100-100-100': threeSpan_simple,
            #  '110-100-100-100-100': fourSpan_simple
                                         }
        return beamVersionCode[support_Code]

def beamCodeMoment(support_Code=''):
        beamVersionCode={
             '110-110': simpleMoment ,
             '010-110' : simpleMoment ,
             '110-010' : simpleMoment ,
             '111-000' : conteliverMomentL ,
             '000-111' : conteliverMomentR ,
             '111-111' : fixedFixedMoment ,
             '111-110' : fixedPinnedMoment ,
             '111-100' : fixedPinnedMoment ,
             '111-010' : fixedPinnedMoment ,
             '100-111' : pinnedFixedMoment ,
             '110-111' : pinnedFixedMoment ,
                                         }
        return beamVersionCode[support_Code]

# to analyse a simple beam with a fomat of '110-100' and '100-110'
def simple(l=None,x=None,a=None, P=None, E=None, I=None):
    b=l-a
    R1=P*b/l
    R2=P*a/l
    x0_a=x[:np.where(x == a)[0][0]]
    xa_e=x[np.where(x == a)[0][0]:]
    
    V1=R1*np.ones(len(x0_a))
    V2=-R2*np.ones(len(xa_e))
    V=np.concatenate((V1, V2), axis=0)
   

    M1=(P*b/l)*x0_a 
    M2=R1*a -(R2)*(xa_e-a)
    M=np.concatenate((M1, M2), axis=0)

    D1=-(P*b*x0_a/(6*E*I*l))*(l**2 -b**2 - x0_a**2)
    D2=-(P*a*(l-xa_e)/(6*E*I*l))*(l**2-a**2 - (l-xa_e)**2)
    D=np.concatenate((D1, D2), axis=0)

    return R1, R2, V, M , D ,x

# to analyse a fixed-fixed end beam with a format of '111-1111' and '100-110'
def fixed_fixed (l=None,x=None,a=None, P=None, E=None, I=None):
    b=l-a
    R1=(P*(b**2)/(l**3))*(3*a + b)
    R2=(P*(a**2)/(l**3))*(a + 3*b)
    x0_a=x[:np.where(x == a)[0][0]]
    xa_e=x[np.where(x == a)[0][0]:]
    
    V1=R1*np.ones(len(x0_a))
    V2=-R2*np.ones(len(xa_e))
    V=np.concatenate((V1, V2), axis=0)
   

    M1=R1*x0_a - (P*a*b**2)/ (l**2)
    Ma=(2*P* a**2 * b**1)/(l**3)
    MM2=(P* a**2)/(l**2)
    M2=b*Ma- (Ma + MM2)*(xa_e - a)
    M=np.concatenate((M1, M2), axis=0)

    D1=-(P*(b**2) *x0_a**2 /(6*E*I*(l**3)))*(3*a*l -3*a*x0_a - b*x0_a)
    D2= -(P*(a**2)*(l-xa_e)**2 /(6*E*I*(l**3)))*(3*b*l -3*b*(l-xa_e) - a*(l-xa_e))
    D=np.concatenate((D1, D2), axis=0)
    return R1, R2, V, M , D, x


def cantileverR(l=15,x=[0, 15],a=5, P=20, E=29000, I=100):
    
    b=l-a
    R1=0
    R2=P
    x0_a=x[:np.where(x == a)[0][0]]
    xa_e=x[np.where(x == a)[0][0]:]
    
    V1=R1*np.ones(len(x0_a))
    V2=-R2*np.ones(len(xa_e))
    V=np.concatenate((V1, V2), axis=0)
   

    M1=-R1*x0_a 
    M2=-R2*(xa_e-a)
    M=np.concatenate((M1, M2), axis=0)

    D1=-(P*b**2/(6*E*I))*(3*l- 3*x0_a - b)
    D2=-(P*(l - xa_e)**2 /(6*E*I))*(3*b - l + xa_e)
    D=np.concatenate((D1, D2), axis=0)

    return R1, R2, V, M , D , x

def cantileverL(l=15,x=[0, 15],a=5, P=20, E=29000, I=100):
    R1=P
    R2=0
    x0_a=x[:np.where(x == a)[0][0]] 
    xa_e=x[np.where(x == a)[0][0]:]
    
    V1=-R1*np.ones(len(x0_a))
    V2=-R2*np.ones(len(xa_e))
    V=np.concatenate((V1, V2), axis=0)
   

    M1=-R1*(a-x0_a) 
    M2=R2*(xa_e)
    M=np.concatenate((M1, M2), axis=0)

    D1=(P*(x0_a)**2 /(6*E*I))*(3*a - x0_a)  #x<a   
    D2=(P*a**2/(6*E*I))*(3*xa_e -a) #x>a
    # D1=np.flip(D1, axis=0)
    # D2=np.flip(D2, axis=0)
    D=-np.concatenate((D1, D2), axis=0)
    
    return R2, R1, V, M , D, x

def fixed_rollerR(l=15,x=[0,15],a=5, P=20, E=29000, I=100):
    b=l-a
    R1=(P*(b**2)/(2*l**3))*(a+2*l)
    R2=(P*(a)/(2*l**3))*(3*l**2 - a**2)
    x0_a=x[:np.where(x == a)[0][0]]
    xa_e=x[np.where(x == a)[0][0]:]
    
    V1=R1*np.ones(len(x0_a))
    V2=-R2*np.ones(len(xa_e))
    V=np.concatenate((V1, V2), axis=0)
   

    M1=R1*x0_a 
    M2=R1*xa_e - P*(xa_e - a)
    M=np.concatenate((M1, M2), axis=0)

    D1=-(P*(b**2) *x0_a /(12*E*I*(l**3)))*(3*a * (l**2) -2*l * x0_a**2 -a* x0_a**2)
    D2=-(P*a /(12*E*I*l**3))*((l - xa_e)**2) * (3* l**2 *xa_e  - a**2 * xa_e -2* a**2 *l)
    D=np.concatenate((D1, D2), axis=0)


    return R1, R2, V, M , D, x

def fixed_rollerL(l=15,x=[0,15],a=5, P=20, E=29000, I=100):
    
    b=l-a
    R1=(P*(b)/(2*l**3))*(3*l**2 - b**2)
    R2=(P*(a**2)/(2*l**3))*(b+2*l)

    x0_a=x[:np.where(x == a)[0][0]]
    xa_e=x[np.where(x == a)[0][0]:]
    
    V1=-R1*np.ones(len(x0_a))
    V2=R2*np.ones(len(xa_e))
    V=np.concatenate((V1, V2), axis=0)
   
     
    M1=R2*(l-x0_a) - P*(a-x0_a)  #x<a
    M2=R2*(l-xa_e)         #x>1a
    M=np.concatenate((M1, M2), axis=0)

    D1=-(P*b /(12*E*I*l**3))*((x0_a)**2) * (3* l**2 *(l-x0_a)  - b**2 * (l-x0_a) -2* b**2 *l)
    D2=-(P*(a**2) *(l-xa_e) /(12*E*I*(l**3)))*(3*b * (l**2) -2*l * (l-xa_e)**2 -a* (l-xa_e)**2)
    D=np.concatenate((D1, D2), axis=0)


    return R1, R2, V, M , D , x       

def fixed_rotatFixed(l=15,x=[0,15],a=5, P=20, E=29000, I=100):
    le=2*l
    xn=x+l
    xe=np.concatenate((x, xn), axis=0)
    M=np.zeros(len(xe))
    V=np.zeros(len(xe))
    D=np.zeros(len(xe))
    R1=0
    R2=0
    for ae in [a, le-a]:
        R10, R20, V0, M0 , D0 , x= fixed_fixed(l=le,x=xe,a=ae, P=P, E=E, I=I)
        M = M + M0
        V = V + V0
        D=D + D0
        R1= R1+ R10
        R2= R2+ R20 
    V=V[: len(xn)]     
    M=M[: len(xn)]     
    D=D[: len(xn)]     
    x=x[:len(xn)]     
    R1=0

    return R1, R2, V, M , D, x


def rotatFixed_fixed(l=None,x=None,a=None, P=None, E=None, I=None):
    le=2*l
    xn=x+l
    xe=np.concatenate((x, xn), axis=0)
    
    M=np.zeros(len(xe))
    V=np.zeros(len(xe))
    D=np.zeros(len(xe))
    R1=0
    R2=0
    for ae in [l-a, l+a]:
        R10, R20, V0, M0 , D0 , x= fixed_fixed(l=le,x=xe,a=ae, P=P, E=E, I=I)
        M = M + M0
        V = V + V0
        D=D + D0
        R1= R1+ R10
        R2= R2+ R20 
    V=V[len(xn) :]     
    M=M[len(xn) :]     
    D=D[len(xn) :]     
    x=x[:len(xn)]     
    R1=0

    return R1, R2, V, M , D, x


# for moment load
def simpleMoment(l=None,x=None,a=None, m=None, E=None, I=None):
    R1=m/l
    R2=-R1
    x0_a=x[:np.where(x == a)[0][0]]
    xa_e=x[np.where(x == a)[0][0]:]
    
    V1=R1*np.ones(len(x0_a))
    V2=R1*np.ones(len(xa_e))
    V=np.concatenate((V1, V2), axis=0)
   

    M1= R1 *x0_a #x<a
    M2=-R1*(l-xa_e) #x>a
    M=np.concatenate((M1, M2), axis=0)

    D1=(m /(6*E*I))*((6*a - (3*a**2 /l) - 2*l)*x0_a - (x0_a**3)/l)  #x<a
    D2=(m/(6*E*I)) * (3*(a**2 + xa_e**2) - (xa_e**3 / l) - (2*l +  (3* a**2 /l) )*xa_e)  # x>a
    D=np.concatenate((D1, D2), axis=0)

    return -1*R1, -1*R2, V, M , D ,x

def conteliverMomentL(l=None,x=None,a=None, m=None, E=None, I=None):
    R1=0
    R2=0
    x0_a=x[:np.where(x == a)[0][0]]
    xa_e=x[np.where(x == a)[0][0]:]
    
    V1=0*np.ones(len(x0_a))
    V2=0*np.ones(len(xa_e))
    V=np.concatenate((V1, V2), axis=0)
   

    M1= -1*m * np.ones(len(x0_a)) #x<a
    M2=0*(l-xa_e) #x>a
    M=np.concatenate((M1, M2), axis=0)

    D1=-(m /(2*E*I))*(x0_a**2)  #x<a
    D2=-(m*a/(E*I)) * (xa_e - 0.5*a)  # x>a
    D=np.concatenate((D1, D2), axis=0)

    return R1, R2, V, M , D ,x

def conteliverMomentR(l=None,x=None,a=None, m=None, E=None, I=None):
    R1=0
    R2=0
    x0_a=x[:np.where(x == a)[0][0]]
    xa_e=x[np.where(x == a)[0][0]:]
    
    V1=0*np.ones(len(x0_a))
    V2=0*np.ones(len(xa_e))
    V=np.concatenate((V1, V2), axis=0)
   

    M1=0*(x0_a) #x<a
    M2= m*np.ones(len(xa_e)) #x>a
    M=np.concatenate((M1, M2), axis=0)

    D2=(m /(2*E*I))*((l-xa_e)**2) # x>a
    D1=(m*(l-a)/(E*I)) * (a-x0_a) + D2[0]  #x<a
    D=np.concatenate((D1, D2), axis=0)

    return R1, R2, V, M , D ,x

def fixedFixedMoment(l=None,x=None,a=None, m=None, E=None, I=None):
  
    b=l-a
    ta=l-3*a
    # tb=l-3*b
    R1=6*m*a*(b)/l**3
    R2=-R1
    x0_a=x[:np.where(x == a)[0][0]]
    xa_e=x[np.where(x == a)[0][0]:]
    
    V1=R1*np.ones(len(x0_a))
    V2=R1*np.ones(len(xa_e))
    V=np.concatenate((V1, V2), axis=0)
   

    M1=(m*b/l**3)*(l*ta +6*a*x0_a) #x<a
    M2= (m*b/l**3)*(l*ta + 6*a*xa_e)- m #x>a
    M=np.concatenate((M1, M2), axis=0)

    ma=m*b*ta/l**2

    D1=-(R1/(6*E*I))*(x0_a)**3 - ((ma)*(x0_a)**2)/(2*E*I)  #x<a
    D2=-(R1/(6*E*I))*(xa_e)**3 - ((ma)*(xa_e)**2)/(2*E*I)  + m*(xa_e - a)**2/(2*E*I) # x>a
    D=np.concatenate((D1, D2), axis=0)

    return -1*R1, -1*R2, V, M , D ,x


def fixedPinnedMoment(l=None,x=None,a=None, m=None, E=None, I=None):
    
    b=l-a
    # ta=l-3*a
    # tb=l-3*b
    R1=3*m*a*(l+b)/(2*l**3)
    R2=-R1
    x0_a=x[:np.where(x == a)[0][0]]
    xa_e=x[np.where(x == a)[0][0]:]
    
    V1=R1*np.ones(len(x0_a))
    V2=R1*np.ones(len(xa_e))
    V=np.concatenate((V1, V2), axis=0)
   

    ma=R2*l + m
    M1=ma + R1*(x0_a) #x<a
    M2= R2*(l-xa_e)  #x>a
    M=np.concatenate((M1, M2), axis=0)


    D1=-(R1/(6*E*I))*(x0_a)**3 - ((ma)*(x0_a)**2)/(2*E*I)  #x<a
    D2=-(R1/(6*E*I))*(xa_e)**3 - ((ma)*(xa_e)**2)/(2*E*I)  + m*(xa_e - a)**2/(2*E*I) # x>a
    D=np.concatenate((D1, D2), axis=0)

    return -1*R1, -1*R2, V, M , D ,x


def pinnedFixedMoment(l=None,x=None,a=None, m=None, E=None, I=None):
    
    a=l-a

    R1, R2, V, M , D ,x=fixedPinnedMoment(l,x,a, m, E, I)
    V=np.flip(V, axis=0)
    M=np.flip(-1*M, axis=0)
    D=np.flip(-1*D, axis=0)
    return R1, R2, V, M , D ,x
    # def simpleOverhangL(l=None,x=None,a=None, m=None, E=None, I=None):





# ######################### #####################################     COLUMN      ##############################################################
#  This section analyze a column structure

def isOnCol(loc=0, beamLeftEdge=0, beamRightEdge=1):
    if loc<beamLeftEdge or loc>beamRightEdge :
        return False
    else:
        return True

# def supportCode(supports={'name1':['000',1]}):
#     if len(supports)==0:
#         return '000-000'

#     elif len(supports)==1: 
#         for value in supports.values():
#             if value[1]==0:
#                 return value[0] +'-'+'000'
#             else:
#                 return '000'+'-'+value[0]

#     else:
#         supCode=''
#         for value in supports.values():
#             supCode=supCode  + value[0]+ '-'    
#         return supCode[:-1]
  
def columnCode(support_Code=''):
        colVersionCode={
             '110-010': simpleCol ,
             '010-110' : simpleCol,
             '110-110' : simpleCol,
             '000-111': cantileverCol , 
             '111-000': cantileverCol, 
             '111-100': fixed_rollerCol,
             '111-100': fixed_rollerCol,
             '111-110': fixed_rollerCol,
             '100-111': fixed_rollerCol,
             '010-111': fixed_rollerCol,
             '110-111': fixed_rollerCol,
             '111-111': fixed_fixedCol,
             '001-111': fixed_rotatFixedCol ,
             '111-001': fixed_rotatFixedCol,
             '111-101': fixed_rotatXFixedCol,
                                         }
        return colVersionCode[support_Code]


# to analyse a simple beam with a fomat of '110-100' and '100-110'
def simpleCol(l=None,x=None,a=None, P=None, E=None, I=None):
    K_factor=1
    buckling_load1= (1*np.pi)**2 *E*I / (K_factor*l)**2 
    buckling_load2= (2*np.pi)**2 *E*I / (K_factor*l)**2 
    buckling_load3= (3*np.pi)**2 *E*I / (K_factor*l)**2 

    D1=np.sin(np.pi*x/(K_factor*l))
    D2=np.sin(2*np.pi*x/(K_factor*l))
    D3=np.sin(3*np.pi*x/(K_factor*l))
    return K_factor, buckling_load1, buckling_load2, buckling_load3, D1,D2,D3, x

# to analyse a fixed-fixed end beam with a format of '111-1111' and '100-110'
def fixed_fixedCol (l=None,x=None,a=None, P=None, E=None, I=None):
    K_factor=0
    buckling_load1= float('inf')
    buckling_load2= float('inf')
    buckling_load3= float('inf')
    D1=0*x
    D2=0*x
    D3=0*x
    return K_factor, buckling_load1, buckling_load2, buckling_load3, D1,D2,D3, x


def cantileverCol(l=15,x=[0, 15],a=5, P=20, E=29000, I=100):
    
    K_factor=2
    buckling_load1= (1*np.pi)**2 *E*I / (K_factor*l)**2 
    buckling_load2= (2*np.pi)**2 *E*I / (K_factor*l)**2 
    buckling_load3= (3*np.pi)**2 *E*I / (K_factor*l)**2 
    D1=1- np.cos(np.pi*x/(K_factor*l))
    D2=1- np.cos(2*np.pi*x/(K_factor*l))
    D3=1- np.cos(3*np.pi*x/(K_factor*l))
    return K_factor, buckling_load1, buckling_load2, buckling_load3, D1,D2,D3, x
    
  

def fixed_rollerCol(l=15,x=[0,15],a=5, P=20, E=29000, I=100):
    K_factor=0.707

    buckling_load1= (1*np.pi)**2 *E*I / (l)**2 
    buckling_load2= (2*np.pi)**2 *E*I / (l)**2 
    buckling_load3= (3*np.pi)**2 *E*I / (l)**2 

    D1=(np.sin(np.pi*x/(K_factor*l))   - (np.pi/(K_factor*l))*l*np.cos(np.pi*x/(K_factor*l))     +(np.pi/(K_factor*l))*(l-x))*0.25
    D2=(np.sin(1*np.pi*x/(K_factor*l)) - (1*np.pi/(K_factor*l))*l*np.cos(1*np.pi*x/(K_factor*l)) +(1*np.pi/(K_factor*l))*(l-x))*0.25
    D3=(np.sin(1*np.pi*x/(K_factor*l)) - (1*np.pi/(K_factor*l))*l*np.cos(1*np.pi*x/(K_factor*l)) +(1*np.pi/(K_factor*l))*(l-x))*0.25

    return K_factor, buckling_load1, buckling_load2, buckling_load3, D1,D2,D3, x
    

def fixed_rotatFixedCol(l=15,x=[0,15],a=5, P=20, E=29000, I=100):

    K_factor=1
    buckling_load1= (1*np.pi)**2 *E*I / (K_factor*l)**2 
    buckling_load2= (1*np.pi)**2 *E*I / (K_factor*l)**2 
    buckling_load3= (1*np.pi)**2 *E*I / (K_factor*l)**2 

    D1=1-np.cos(np.pi*x/(K_factor*l))
    D2=1-np.cos(2*np.pi*x/(K_factor*l))
    D3=1-np.cos(3*np.pi*x/(K_factor*l))
    return K_factor, buckling_load1, buckling_load2, buckling_load3, D1,D2,D3, x

def fixed_rotatXFixedCol(l=15,x=[0,15],a=5, P=20, E=29000, I=100):

    K_factor=0.5
    buckling_load1= (1*np.pi)**2 *E*I / (K_factor*l)**2 
    buckling_load2= (2*np.pi)**2 *E*I / (K_factor*l)**2 
    buckling_load3= (3*np.pi)**2 *E*I / (K_factor*l)**2 

    D1=1-np.cos(np.pi*x/(K_factor*l))
    D2=1-np.cos(2*np.pi*x/(K_factor*l))
    D3=1-np.cos(3*np.pi*x/(K_factor*l))
    return K_factor, buckling_load1, buckling_load2, buckling_load3, D1,D2,D3, x



############################################### TRUSS   ########################################################################

def analyzeTruss(span=4, w=100, h=50, xco=[0,1,2,3,4,3,2,1], yco=[1,3],
                 A=100, E=1000, a=[1,2,3,4,5,6,6,6,7,7,8,8,8], b=[1,2,3,4,5,6,6,6,7,7,8,8,8] , supns=[1,5], conditions=['110', '110'], 
                 lon=[2,4], fx=[0, 0], fy=[-100, -100] ):
    #lon : load on nodes
    snofel = a #start node of elements
    enofel = b #end node of elements
    lenofel = [] #length of the element
    elcon = [] #constant of the element
    cosofel = [] #cos of element
    sinofel = [] #sin of element

    te = len(a)
    for i in range(te):  
        x1 = float(xco[a[i]-1])
        y1 = float(yco[a[i]-1])
        x2 = float(xco[b[i]-1])
        y2 = float(yco[b[i]-1])
        l = math.sqrt((x2-x1)**2+(y2-y1)**2)

        con = A*E/l
        cos = (x2-x1)/l
        sin = (y2-y1)/l
        

        lenofel.append(l)
        elcon.append(con)
        cosofel.append(cos)
        sinofel.append(sin)

    # print(cosofel)
    # print(sinofel)
    elstmat = [] #element stiffness matrix

    for i in range(te):
        cc = float(cosofel[i])**2
        ss = float(sinofel[i])**2
        cs = float(cosofel[i])*float(sinofel[i])
        
        mat = elcon[i]*np.array([[cc, cs, -cc, -cs],
                                [cs, ss, -cs, -ss],
                                [-cc, -cs, cc, cs],
                                [-cs, -ss, cs, ss]])


        elstmat.append(mat)
    tn = len(xco)

    gstmatmap = []                          ## Global stiffness matrix mapping, gstmatmap will be the sqare matrix of tn*
    for i in range(te):                     ## do this for each elements
        m = snofel[i]*2                     ## taking the start node of element(i) and multiply by 2
        n = enofel[i]*2
                                            ## taking the end node of element(i) and multiply by 2
        add = [m-1, m, n-1, n]              ## Address of columns and rows of gstmatmap for elemet(i)
                                                # if startnode is 1 and end node is 2 then add=[1,2,3,4]
                                                # if startnode is 1 and end node is 3 then add=[1,2,5,6]
        gmat = np.zeros((tn*2, tn*2))    ## global stiffness matrix loaded with zeros for element(i)
        elmat = elstmat[i]                  ## taking the element stiffness matrix of element(i)
        for j in range(4):                  
            for k in range(4):              
                a = add[j]-1                ## addressing row of GST matrix for element(i)
                b = add[k]-1                ## addressing column of GST matrix for element(i)
                gmat[a,b] = elmat[j,k]      ## updating the values in GST matrix with EST matrix of element(i)
        gstmatmap.append(gmat)              ## storing the resultant matrix in gstmatmap list
    
    GSM = np.zeros((tn*2, tn*2))         ## creating an empyty GSM matrix
    for mat in gstmatmap:
        GSM = GSM+mat                       ## adding all the matrix in the gstmatmap list
                                                # this will result in assembled stiffness matrix of the truss structure
    #-----------------------Boundry condition and Loading---------------------#
    displist = []
    forcelist = []
    for i in range(tn):
        a = str('u')+str(i+1)
        displist.append(a)
        b = str('v')+str(i+1)
        displist.append(b)
        c = str('fx')+str(i+1)
        forcelist.append(c)
        d = str('fy')+str(i+1)
        forcelist.append(d)
        
    # print('\n\n________________Support Specifications______________\n')

    dispmat = np.ones((tn*2,1))

    tsupn =len(supns)   #int(input('Enter the total number of nodes having supports : ')) #total number of supported nodes
    # supcondition = ['110 = pinned',
    #                 '100 = Horizonal restrained (vertical is free to move)',
    #                 '010 = Vertical restrained (Horizontal is free to move)']
    
    for i in range(tsupn):
        condition=conditions[i]
        supn=supns[i]
        if condition in['110', '110']:
            dispmat[supn*2-2, 0] = 0
            dispmat[supn*2-1, 0] = 0
        elif condition in['100', '100']:
            dispmat[supn*2-2, 0] = 0
        elif condition in['010', '010']:
            dispmat[supn*2-1, 0] = 0



    # print('\n_________________Loading____________________\n')
    tlon = len(lon)   #int(input('Enter the total number of loaded nodes : ')) #total number of loaded nodes
    forcemat = np.zeros((tn*2,1))


    for i in range(tlon):
        forcemat[lon[i]*2-2, 0] = fx[i]
        forcemat[lon[i]*2-1, 0] = fy[i]

    ###_________________Matrix Reduction_________________###


    rcdlist = []
    for i in range(tn*2):
        if dispmat[i,0] == 0:
            rcdlist.append(i)

    rrgsm = np.delete(GSM, rcdlist, 0) #row reduction
    crgsm = np.delete(rrgsm, rcdlist, 1) #column reduction
    rgsm = crgsm #reduced global stiffness matrix
    rforcemat = np.delete(forcemat, rcdlist, 0) #reduced force mat
    rdispmat = np.delete(dispmat, rcdlist, 0) #reduced disp mat

    ###_______________Solving____________________###

    dispresult = np.matmul(np.linalg.inv(rgsm), rforcemat)
    rin = 0
    for i in range(tn*2):
        if dispmat[i,0] == 1:
            dispmat[i,0] = dispresult[rin,0]
            rin = rin+1
    ##print(dispmat)

    forceresult = np.matmul(GSM, dispmat)
    # print(forceresult)


    ##____________________new co ordinates of nodes____________####

    newxco = []
    newyco = []
    count = 0
    for i in range(tn):
        k = xco[i]+dispmat[count,0]
        newxco.append(k)
        count = count+1
        l = yco[i]+dispmat[count,0]
        newyco.append(l)
        count = count+1

    ###____________________new length of memebers______________####
        
    newlenofel = []
    for i in range(te):
        a, b = snofel[i], enofel[i]
        x1 = float(newxco[a-1])
        y1 = float(newyco[a-1])
        x2 = float(newxco[b-1])
        y2 = float(newyco[b-1])
        l = math.sqrt((x2-x1)**2+(y2-y1)**2)
        newlenofel.append(l)

    ###______________strain in elements_______________________###
        
    # np.set_printoptions(3, suppress=False)

    elstrain = np.zeros((te,1))
    for i in range(te):
        elstrain[i,0] = (newlenofel[i]-lenofel[i])/(lenofel[i])
    # np.set_printoptions(3, suppress=True)

    ###__________________stress in elements______________________###

    elstress = np.zeros((te,1))
    for i in range(te):
        elstress[i,0] = E * elstrain[i,0]
        
    ###_________________Member forces____________________#########

    eforce = np.zeros((te,1))
    for i in range(te):
        eforce[i,0] = A * elstress[i,0]

    # print('\nGlobal Stiffness Matrix of the Truss\n')
    # print(np.around(GSM, 3))
    # print('dispmat=' ,dispmat)
    # print('\n\nGlobal Stiffness Matrix of the Truss\n')
    # print(GSM)
    # print('\n\nDisplacement matrix of nodes\n')
    # print(dispmat)
    # print('\n\nForce matrix of nodes\n')
    # print(forceresult)
    # print('\n***Positive is Tensile\nNegetive is Compressive***\n')

    # print('\n\nStrain in the elements')
    # print(elstrain)
    # print('\n\nStress in the elements')
    # print(elstress)
    # print('\n\nForce in the element')
    # print(eforce)
    return GSM, dispmat, forceresult, elstrain, elstress , eforce 

    # ############## TYPES oF Trusses
# Pratt_Bridge
def Pratt_NodeNum(truss_type=None, numSpans=None):
    if  truss_type=='Pratt Bridge' or 'Howe Roof':
        mid=0.5*(3*( numSpans+1)-1)
        a_st=np.arange(1, numSpans+2,1)
        b_end=np.arange(1, numSpans+2,1)+1

        for i in range( numSpans+2,2* numSpans+1):
            if i==mid:
                a_st_c=i*np.ones((2,), dtype=int)
                a_st=np.concatenate((a_st,a_st_c))
            else: 
                a_st_c=i*np.ones((3,), dtype=int)
                a_st=np.concatenate((a_st, a_st_c))
        if  numSpans==2:
            b_end2=[2,1]
        elif  numSpans==4:
            b_end2=[4,3,7,3,8,3,2,1]
        elif  numSpans==6:
            b_end2=[6,5,9,5,4,10,4,11,4,3,12,3,2,1]
        elif  numSpans==8:
            b_end2=[8,7,11,7,6,12,6,5,13,5,14,5,4,15,4,3,16,3,2,1]
        elif  numSpans==10:
            b_end2=b_end2=[10,9,13,9,8,14,8,7,15,7,6,16,6,17,6,5,18,5,4,19,4,3,20,3,2,1]
        b_end=np.concatenate((b_end,b_end2))
    return a_st, b_end


# Howe_Bridge
def Howe_NodeNum(truss_type=None, numSpans=None):
    if  truss_type=='Howe Bridge' or 'Pratt Roof':
        mid=0.5*(3*( numSpans+1)-1)
        a_st=np.arange(1, numSpans+2,1)
        b_end=np.arange(1, numSpans+2,1)+1

        for i in range( numSpans+2,2* numSpans+1):
            if i== numSpans+2 or i==2* numSpans:
                a_st_c=i*np.ones((2,), dtype=int)
                a_st=np.concatenate((a_st,a_st_c))
            elif i==mid:
                a_st_c=i*np.ones((4,), dtype=int)
                a_st=np.concatenate((a_st,a_st_c))
            else: 
                a_st_c=i*np.ones((3,), dtype=int)
                a_st=np.concatenate((a_st, a_st_c))
        if  numSpans==2:
            b_end2=[2,1]
        elif  numSpans==4:
            b_end2=[4,7,4,3,2,8,2,1]
        elif  numSpans==6:
            b_end2=[6,9,6,5,10,5,4,3,11,3,2,12,2,1]
        elif  numSpans==8:
            b_end2=[8,11,8,7,12,7,6,13,6,5,4,14,4,3,15,3,2,16,2,1]

        elif  numSpans==10:
            b_end2=b_end2=[10,13,10,9,14,9,8,15,8,7,16,7,6,5,17,5,4,18,4,3,19,3,2,20,2,1]

        b_end=np.concatenate((b_end,b_end2))
    return a_st, b_end

# Warren_Bridge 
def Warren_NodeNum(truss_type=None, numSpans=None):
    ''' Number of spans for Warren truss are 2, 4, 6, 8, 10'''    
    if  truss_type=='Warren Bridge':
        mid=0.5*(3*( numSpans+1)-1)
        a_st=np.arange(1, numSpans+2,1)
        b_end=np.arange(1, numSpans+2,1)+1

        for i in range (numSpans+2, 2*numSpans+1):
            if i== numSpans+2 or i==2* numSpans:
                a_st_c=i*np.ones((3,), dtype=int)
                a_st=np.concatenate((a_st,a_st_c))
            elif i==mid:
                a_st_c=i*np.ones((4,), dtype=int)
                a_st=np.concatenate((a_st,a_st_c))
            elif numSpans==10 and (i==mid+2 or i==mid-2): 
                a_st_c=i*np.ones((4,), dtype=int)
                a_st=np.concatenate((a_st,a_st_c))
            else: 
                a_st_c=i*np.ones((2,), dtype=int)
                a_st=np.concatenate((a_st, a_st_c))
        if  numSpans==2:
            b_end2=[2,1]
            a_st=a_st[:-1]
        elif  numSpans==6:
            b_end2=[6,5,9,5,10,5,4,3,11,3,12,3,2,1]
        elif  numSpans==10:
            b_end2=[10,9,13,9,14,9,8,7,15,7,16,7,6,5,17,5,18,5,4,3,19,3,20,3,2,1]
        b_end=np.concatenate((b_end,b_end2))
        
    return a_st, b_end

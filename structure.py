from analyze import * 
from visualize import *
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import matplotlib.ticker as mtick

# ########################################## General Structure Section ############################################################
class structure(object):
    ''' This object returns struture type and general properties like E'''
    id=1
    def __init__(self, structure_type=None, E=None, unit=None):
        self.structure_type=structure_type
        self.structure_id=structure.id
        self.E=E
        self.unit=unit
        structure.id +=1 

    def set_unit(self, new_unit):
        self.unit =new_unit

    def get_unit(self):
        return self.unit

    def get_structure_id(self):
        return self.structure_id

    def get_structure_type(self):
        return self.structure_type

    def set_structure_type(self, new_structure_type=None):
        self.structure_type = new_structure_type
    
    def set_E(self, new_E=None):
        self.E = new_E

    def get_E(self):
        return self.E

    def __str__ (self):
        return self.structure_type + ' : ' + str(self.structure_id)


######################################################### Single Span Beam Structure #######################################################
# Defining beam object and a root of structure object
class beam(structure):
    id=1
    def __init__(self, xNode1=None, xNode2=None, I=None):
        structure.__init__(self, structure_type=None, E=None, unit=None)
        self.xNode1=xNode1
        self.xNode2=xNode2
        self.supports={}
        self.pointLoads={}
        self.distributedLoads={}
        self.momentLoads={}
        self.beam_id=beam.id
        self.I=I
        # self.unit=unit
        beam.id += 1 
    
    def get_length(self):
        return self.xNode2- self.xNode1
    def get_nodes(self):
        return self.xNode1, self.xNode2
    def get_lengthList(self):
        return  np.array([x/100 for x in range(int(self.xNode1*100), int((self.xNode2+.01)*100))])
       
    # Supports
    def set_support(self, support_dof='000', name=None, Loc=0):
        ''' add support 'x,y,theta' 1=restricted 0=free'''
        for i in support_dof:
            if i=='0' or i=='1':
                pass
            else:
                return 'wrong input!, DOF values can only be 0 or 1'

        if not isOnBeam(Loc,self.xNode1, self.xNode2):
            return 'Error: support locatoin can not be out of beam length limit'
        else:
            if name in self.supports.keys():
                print('support ' + name + 'updated')
            self.supports[name] = [support_dof, Loc]

    def get_supports(self):
        return self.supports

    def get_supportCode(self):
        sub=supportCode(self.supports)
        return sub

    
    # Loads_point load
    def set_pointLoad(self, name=None, Loc=0, Mag=0):
        if not isOnBeam(Loc,self.xNode1, self.xNode2):
            return 'Error: load locatoin can not be out of beam length limit'
        else:
            if name in self.pointLoads.keys():
                print('point load ' + name + ' updated')
            self.pointLoads[name] = [Loc, Mag]
    
    def get_pointLoads(self):
        return self.pointLoads


    # Loads_ moment load
    def set_momentLoad(self, name=None, Loc=0, Mag=0):
        if not isOnBeam(Loc,self.xNode1, self.xNode2):
            return 'Error: load locatoin can not be out of beam length limit'
        else:
            if name in self.momentLoads.keys():
                print(' moment load ' + name + ' updated')
            self.momentLoads[name] = [Loc, Mag]
    
    def get_momentLoads(self):
        return self.momentLoads

    # Loads_ distributed load
    def set_distributedLoad(self, name=None, startLoc=0, stopLoc=1, startMag=0, stopMag=1):
        if not isOnBeam(startLoc,self.xNode1, self.xNode2) or not isOnBeam(stopLoc,self.xNode1, self.xNode2):
            return 'Error: load locatoin can not be out of beam length limit'
        else:
            if name in self.distributedLoads.keys():
                print('distributed load ' + name + ' updated')
            self.distributedLoads[name] = [startLoc, stopLoc, startMag, stopMag]
    
    def get_distributedLoads(self):
        return self.distributedLoads

    def drawBeam(self):
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        beamDraw(l=self.get_length(), ax=ax, unit=self.unit) 
        for code, loc in self.get_supports().values():
            if code== '111':
                fixedSupport(loc, ax=ax)   
            if code== '010':
                rollerSupport(loc, ax=ax)  
            if code == '110':
                pinnedSupport(loc, ax=ax)
            if code== '001':
                rotateFixedSupport(loc, ax=ax)  

        for loc , mag in self.get_pointLoads().values():
            pointLoad (loc, mag, ax=ax , unit=self.unit)

        for loc , mag in self.get_momentLoads().values():
            momentLoad (loc, mag, ax=ax, unit=self.unit)

        for loc , mag in self.get_momentLoads().values():
            momentLoad (loc, mag, ax=ax, unit=self.unit)

        for locLoad in self.get_distributedLoads().values():
            distributedLoad(locLoad, ax=ax, unit=self.unit)
    
        
        ax.tick_params(left=False, bottom=False,labelleft=False, labelbottom=False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)

        figfile = BytesIO()
        plt.savefig(figfile, format='png')
        figfile.seek(0)  # rewind to beginning of file
        # figdata_png = base64.b64encode(figfile.read())
        figdata_png = base64.b64encode(figfile.getvalue())
        figdata_png=figdata_png.decode('utf-8')
        return figdata_png


    def get_analyze(self):
        x=self.get_lengthList()
        M=np.zeros(len(x))
        V=np.zeros(len(x))
        D=np.zeros(len(x))
        R1=0
        R2=0
        #analyze for point load
        for [a,P] in self.get_pointLoads().values():
            R10, R20, V0, M0 , D0 , x=beamCode(self.get_supportCode())(l=self.get_length(), x=x , a=a, P=P, E=self.E, I=self.I)
            M = M + M0
            V = V + V0
            D=D + D0
            R1= R1+ R10
            R2= R2+ R20
        # analyze for distributed load
        distL=list(self.get_distributedLoads().values())
        for i in range (len(distL)):
            a1=distL[i][0]
            a2=distL[i][1]
            L1=distL[i][2]
            L2=distL[i][3]
            a1_2=np.array([x/100 for x in range(int(a1*100), int(a2*100)) ])
            if L1==L2:
                P=L1/100
                for a in a1_2:
                    R10, R20, V0, M0 , D0 , x=beamCode(self.get_supportCode())(l=self.get_length(), x=x , a=a, P=P, E=self.E, I=self.I)
                    M = M + M0
                    V = V + V0
                    D=D + D0
                    R1= R1+ R10
                    R2= R2+ R20
            else:
                L1_2=np.linspace(L1,L2, len(a1_2))/100
                for a,P  in zip(a1_2, L1_2) :
                    R10, R20, V0, M0 , D0, x =beamCode(self.get_supportCode())(l=self.get_length(), x=x , a=a, P=P, E=self.E, I=self.I)
                    M = M + M0
                    V = V + V0
                    D=D + D0
                    R1= R1+ R10
                    R2= R2+ R20
        # analyze for moment load 
        for [a,m] in self.get_momentLoads().values():
            R10, R20, V0, M0 , D0 , x=beamCodeMoment(self.get_supportCode())(l=self.get_length(), x=x , a=a, m=m, E=self.E, I=self.I)
            M = M + M0
            V = V + V0
            D=D + D0
            R1= R1+ R10
            R2= R2+ R20
        return  R1, R2, V, M , D ,x

    def plot_results(self):

        R1, R2, V, M , D , x =self.get_analyze()
        b=np.zeros(len(x))
        
        if self.unit=='SI( N  ,m ,C)':
            u, Vu,Mu, Du='SI', 'N', 'N-m', 'm'
        else:
            u, Vu,Mu, Du='US', 'kips', 'Kips-ft', 'ft'

        fig, axes =plt.subplots(nrows=3, ncols=1)
        axes[0].plot(x,V,'purple', x,b,'b')
        axes[0].set_ylim(-1.2*max(-min(V),max(V)) , 1.2*max(-min(V),max(V)))
        axes[0].fill_between(x,V,b, color='purple', alpha= 0.5)
        axes[0].set_ylabel('Shear ' +'('+ Vu +')')
        axes[1].plot(x,M,'g', x,b,'b')
        axes[1].fill_between(x,M,b, color='green', alpha=0.5)
        axes[1].set_ylim(-1.2*max(-min(M),max(M)) , 1.2*max(-min(M),max(M)))
        axes[1].set_ylabel('Moment '+'('+ Mu +')')
        axes[2].plot(x,D,'k--', x,b,'b')
        axes[2].fill_between(x,D,b, color='grey', alpha=0.5)
        axes[2].set_ylim(-1.2*max(-min(D),max(D)) , 1.2*max(-min(D),max(D)))
        axes[2].set_ylabel('Disp '+'('+ Du +')')
        axes[2].set_xlabel('Length '+'('+ Du +')')
        # axes[0].yaxis.set_major_formatter(mtick.FormatStrFormatter('%.0e'))
        # axes[1].yaxis.set_major_formatter(mtick.FormatStrFormatter('%.0e'))
        # axes[2].yaxis.set_major_formatter(mtick.FormatStrFormatter('%.0e'))

        for i in range(0,3):
            axes[i].tick_params(left=False, bottom=False,labelleft=False, labelbottom=False)
            axes[i].spines['top'].set_visible(False)
            axes[i].spines['bottom'].set_visible(False)
            axes[i].spines['right'].set_visible(False)
            axes[i].spines['left'].set_visible(False)

        figfile = BytesIO()
        plt.savefig(figfile, format='png')
        figfile.seek(0)  # rewind to beginning of file
        # figdata_png = base64.b64encode(figfile.read())
        figdata_png = base64.b64encode(figfile.getvalue())
        figdata_png=figdata_png.decode('utf-8')
        # plt.show()
        return figdata_png


    def get_resultsAtX(self, X):
        R1, R2, V, M , D , x =self.get_analyze()
        Vx=V[np.where(x == X)]
        Mx=M[np.where(x == X)]
        Dx=D[np.where(x == X)]
        return Vx, Mx, Dx
  
    
    
    # def __str__ (self):
    #     return  'E                  :' + str(self.E) + '\n' + \
    #             'Supports           :' + str(self.supports)+ '\n' + \
    #             'Supports code      :'  + str(self.get_supportCode())+ '\n' \
    #             'Point Loads        :'+  str(self.pointLoads) + '\n' + \
    #             'Moment Loads       :'+  str(self.momentLoads) + '\n' + \
    #             'Distributed Loads  :'+  str(self.distributedLoads) + '\n' \
    #             'Reaction R1        :' + str(self.get_analyze()[0])+ '\n' \
    #             'Reaction R2        :' + str(self.get_analyze()[1])+ '\n' \
    #             'Maximum Disp       :' + str(min(self.get_analyze()[4]))+ '\n' \
    #             'Moment at x=0      :' + str((self.get_analyze()[3][0]))+ '\n' \
    #             'Moment at x=L      :' + str((self.get_analyze()[3][-1]))+ '\n' \
    #             'Disp at x=1.25      :' + str(self.get_resultsAtX(1.25)[2][0])+ '\n' 
                



#################################################### Column Section ###########################################################
# Defining Column object and a root of structure object
class column(structure):
    id=1
    def __init__(self, xNode1=None, xNode2=None, I=None):
        structure.__init__(self, structure_type=None, E=None, unit=None)
        self.xNode1=xNode1
        self.xNode2=xNode2
        self.supports={}
        self.pointLoads={}
        self.column_id=column.id
        self.I=I
        # self.unit=unit
        column.id += 1 
    
    def get_length(self):
        return self.xNode2- self.xNode1
    def get_nodes(self):
        return self.xNode1, self.xNode2
    def get_lengthList(self):
        return  np.array([x/100 for x in range(int(self.xNode1*100), int((self.xNode2+.01)*100))])
       
    # Supports
    def set_support(self, support_dof='000', name=None, Loc=0):
        ''' add support 'x,y,theta' 1=restricted 0=free'''
        for i in support_dof:
            if i=='0' or i=='1':
                pass
            else:
                return 'wrong input!, DOF values can only be 0 or 1'

        if not isOnCol(Loc,self.xNode1, self.xNode2):
            return 'Error: support locatoin can not be out of beam length limit'
        else:
            if name in self.supports.keys():
                print('support ' + name + 'updated')
            self.supports[name] = [support_dof, Loc]

    def get_supports(self):
        return self.supports

    def get_supportCode(self):
        return supportCode(self.supports)

    
    # Loads_point load
    def set_pointLoad(self, name=None, Loc=0, Mag=0):
        print('Point Load applies!!!')
        if not isOnCol(Loc,self.xNode1, self.xNode2):
            return 'Error: load locatoin can not be out of beam length limit'
        else:
            if name in self.pointLoads.keys():
                print('point load ' + name + ' updated')
            self.pointLoads[name] = [Loc, Mag]
    
    def get_pointLoads(self):
        return self.pointLoads


    # Loads_ moment load

    def drawColumn(self):
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.set_xlim([-2,2])
        columnDraw(l=self.get_length(), ax=ax) 
        for code, loc in self.get_supports().values():
            if code== '111':
                colFixedSupport(loc, ax=ax)   
            if code== '010':
                colRollerSupport(loc, ax=ax)  
            if code == '110':
                colPinnedSupport(loc, ax=ax)
            if code== '001':
                colRotateFixedSupport(loc, ax=ax)  
            if code== '101':
                colDubleRollerSupport(loc, ax)  

        for loc , mag in self.get_pointLoads().values():
            colPointLoad (loc, mag, ax=ax , unit=self.unit)

        figfile = BytesIO()
        plt.savefig(figfile, format='png')
        figfile.seek(0)  # rewind to beginning of file
        # figdata_png = base64.b64encode(figfile.read())
        figdata_png = base64.b64encode(figfile.getvalue())
        figdata_png=figdata_png.decode('utf-8')
        return figdata_png

    def get_analyze(self):
        x=self.get_lengthList()
        #analyze for point load
        P_load=list(self.get_pointLoads().values())
        # print(P_load)
        a=P_load[0][0]
        P=P_load[0][1]
        K_factor, buckling_load1,buckling_load2,buckling_load3, D1,D2,D3, y=columnCode(self.get_supportCode())(l=self.get_length(), x=x , a=a, P=P, E=self.E, I=self.I)
        return  K_factor, buckling_load1,buckling_load2,buckling_load3, D1,D2,D3, y

    def plot_results(self):
        K_factor, buckling_load1,buckling_load2,buckling_load3, D1,D2,D3, y = self.get_analyze()
        b=np.zeros(len(y))
        # c=np.linspace(-2,2,len(y))
        
        if self.unit=='SI( N  ,m ,C)':
            u, fu, Du='SI', ' N' ,' m'
        else:
            u,fu, Du='US', ' kips',' ft'

        fig, axes =plt.subplots(nrows=1, ncols=4)
        fig.tight_layout()
        # axes[0].tick_params(bottom=False,labelleft=False, labelbottom=False)
        for i in range(0,4):
            axes[i].tick_params(left=False, bottom=False,labelleft=False, labelbottom=False)
            axes[i].spines['right'].set_visible(False)
            axes[i].spines['left'].set_visible(False)
            axes[i].set_ylim([-1, self.xNode2+5])
            axes[i].set_xlim([-2.5, 2.5])
            if i>0:
                axes[i].set_title('Mode shape ' + str(i))
        axes[0].set_xlim([-0.5,0.5])
        axes[0].set_title('Column', color='g')
        axes[0].set_xlabel('L='+ str(self.xNode2)+ Du + ', K='+str(K_factor), color='g')
       
        columnDraw(l=self.get_length(), ax=axes[0]) 
        # Add load on deformed shape
        for code, loc in self.get_supports().values():
            if code== '111':
                colFixedSupport(loc, ax=axes[0])   
            elif code== '010':
                colRollerSupport(loc, ax=axes[0])  
            elif code == '110':
                colPinnedSupport(loc, ax=axes[0])
            elif code== '001':
                colRotateFixedSupport(loc, ax=axes[0])  
            elif code== '101':
                colDubleRollerSupport(loc, ax=axes[0])  

        for loc , mag in self.get_pointLoads().values():
            colPointLoad (loc, mag, ax=axes[0] , unit=self.unit)
            colPointLoadDeformed (loc,D1[-1], mag, ax=axes[1] , unit=self.unit)
            colPointLoadDeformed (loc,D2[-1], mag, ax=axes[2] , unit=self.unit)
            colPointLoadDeformed (loc,D3[-1], mag, ax=axes[3] , unit=self.unit)
        
        axes[1].plot(D1,y,'purple', b,y,'g--')
        axes[1].set_xlabel('$P_{Cr}=$' + str(round(buckling_load1,1)) +fu)
        
        axes[2].plot(D2,y,'purple', b,y,'g--')
        axes[2].set_xlabel('$P_{Cr}=$' + str(round(buckling_load2,1)) +fu)
        
        axes[3].plot(D3,y,'purple', b,y,'g--')      
        axes[3].set_xlabel('$P_{Cr}=$' + str(round(buckling_load3,1)) +fu)

        figfile = BytesIO()
        plt.savefig(figfile, format='png')
        figfile.seek(0)  # rewind to beginning of file
        figdata_png = base64.b64encode(figfile.getvalue())
        figdata_png=figdata_png.decode('utf-8')
        
        return figdata_png, K_factor, buckling_load1,buckling_load2,buckling_load3, D1,D2,D3, y
       
    # def __str__ (self):
    #     return  'E                  :' + str(self.E) + '\n' + \
    #             'Supports           :' + str(self.supports)+ '\n' + \
    #             'Supports code      :'  + str(self.get_supportCode())+ '\n' \
    #             'Point Loads        :'+  str(self.pointLoads) 
                
    

###################################################   TRUSS  ########################################################

# Defining Truss object and a root of structure objects
class truss(structure):
    id=1
    def __init__(self, truss_type='Pratt_Bridge', numSpans=2,span_width=10, truss_height=5, A=20, unit=None):
        structure.__init__(self, structure_type=None, E=None, unit=None)
        self.truss_type=truss_type
        self.numSpans=numSpans
        self.span_width=span_width
        self.truss_height=truss_height
        self.A=A
        self.unit=unit
        self.truss_id=truss.id
        truss.id += 1 
        
        self.supports={}
        self.pointLoads={}
    # Supports
    def set_support(self, support_dof='000', node_num=1):
        ''' add support 'x,y,theta' 1=restricted 0=free'''
        self.supports[node_num] = [support_dof, node_num]
    #Loads
    def set_pointLoad(self, node_num=1, nodeLoadx=0, nodeLoady=0):
        ''' add support 'x,y,theta' 1=restricted 0=free'''
        if nodeLoadx !=0 or nodeLoady!=0:
            self.pointLoads[node_num] = [nodeLoadx, nodeLoady]

    def xyNodecoor(self):
        if self.truss_type=='Pratt Bridge' or self.truss_type=='Howe Bridge' or self.truss_type=='Warren Bridge':                            # Complete this part 
            xco1=np.arange(0,self.numSpans+1,1)
            xco2=np.arange(self.numSpans-1,0,-1)
            xco=self.span_width*np.concatenate((xco1,xco2))
            
            yco1=np.zeros( (self.numSpans+1,), dtype=int)
            yco2=np.ones((self.numSpans-1,), dtype=int)
            yco=self.truss_height*np.concatenate((yco1,yco2))

        elif self.truss_type=='Pratt Roof' or 'Howe Roof':          # Complete this part 
            xco1=np.arange(0,self.numSpans+1,1)
            xco2=np.arange(self.numSpans-1,0,-1)
            xco=self.span_width*np.concatenate((xco1,xco2))
            
            yco1=np.zeros( (self.numSpans+1,), dtype=float)
            yco2=np.linspace(0,self.truss_height, int(self.numSpans/2 +1))[1:]
            yco3=np.linspace(self.truss_height,0, int(self.numSpans/2 +1))[1:-1]
            yco=np.concatenate((yco1,yco2,yco3))

        elif self.truss_type=='K Bridge':
            pass

        return xco, yco 

    def nodeNumList(self):
        # Pratt_Bridge and roof
        if self.truss_type=='Pratt Bridge' or self.truss_type=='Howe Roof':
            a_st, b_end = Pratt_NodeNum(truss_type=self.truss_type, numSpans=self.numSpans)
        # Howe_Bridge and roof
        elif self.truss_type=='Howe Bridge' or self.truss_type=='Pratt Roof':
            a_st, b_end = Howe_NodeNum(truss_type=self.truss_type, numSpans=self.numSpans)
        # Warren_Bridge
        elif self.truss_type=='Warren Bridge':
            if  self.numSpans==4:
                a_st, b_end=Pratt_NodeNum(truss_type=self.truss_type, numSpans=self.numSpans)
            elif  self.numSpans== 8:
                a_st, b_end=Pratt_NodeNum(truss_type=self.truss_type, numSpans=self.numSpans)
                a_st=np.insert(a_st,-7, 14)
                a_st=np.insert(a_st,15, 12)
                b_end=np.insert(b_end, -7, 3)
                b_end=np.insert(b_end, 15, 7)
                
                a_st=np.delete(a_st,-6)
                a_st=np.delete(a_st,13)
                b_end=np.delete(b_end, -6)
                b_end=np.delete(b_end, 13)

                # print(a_st)
                # print(b_end)
            else: 
                a_st, b_end = Warren_NodeNum(truss_type=self.truss_type, numSpans=self.numSpans)
        return a_st, b_end
    # Drawings
    def drawTruss(self):
        fig = plt.figure(figsize=(10,10))
        ax = fig.add_subplot(1,1,1)
        xco, yco=self.xyNodecoor()
        a_st, b_end=self.nodeNumList()

        trussDraw(xco, yco,a_st, b_end,self.truss_type ,self.unit ,ax=ax) 
        # xco, yco= self.xyNodecoor() 

        for code, node in self.supports.values():
            node=node-1  
            if code== '010':
                trussRollerSupport(xco[node],yco[node],loadDraw=self.span_width, ax=ax)  
            if code == '110':
                trussPinnedSupport(xco[node],yco[node],loadDraw=self.span_width, ax=ax)
            if code== '100':
                trussRollerSupporty(xco[node], yco[node], loadDraw=self.span_width,ax=ax)  
        #draw loads
        for key in self.pointLoads:
            fx=self.pointLoads[key][0]
            fy=self.pointLoads[key][1]
            trussPointLoad(xco[key-1], yco[key-1], loadx=fx ,loady=fy,loadDraw=self.span_width, ax=ax, unit=self.unit)

        # for loc , mag in self.get_pointLoads().values():
        #     trussPointLoad(loc, mag, ax=ax , unit=self.unit)

        figfile = BytesIO()
        plt.savefig(figfile, format='png')
        figfile.seek(0)  # rewind to beginning of file
        # figdata_png = base64.b64encode(figfile.read())
        figdata_png = base64.b64encode(figfile.getvalue())
        figdata_png=figdata_png.decode('utf-8')
        return figdata_png

    def get_analyze(self):

        xco,    yco=self.xyNodecoor()
        a_st, b_end=self.nodeNumList()
        supns= list(self.supports.keys())
        conditions=[]
        for i in range(0, len(supns)):
            conditions.append(list(self.supports.values())[i][0])

        lon = list(self.pointLoads.keys())  # loads on nodes numbers
        
        fx=[]
        fy=[]
        for L in list(self.pointLoads.values()):
            fx.append(L[0])
            fy.append(L[1])

        GSM, dispmat, forceresult, elstrain, elstress , eforce=analyzeTruss(span=self.numSpans, w=self.span_width, h=self.truss_height, 
                xco=xco, yco=yco, A=self.A, E=self.E, a=a_st, b=b_end , supns=supns, conditions=conditions, 
                lon=lon, fx=fx, fy=fy )
        return  GSM, dispmat, forceresult, elstrain, elstress , eforce

    def plot_results(self):
        GSM, dispmat, forceresult, elstrain, elstress , eforce=self.get_analyze()
        xco, yco=self.xyNodecoor()
        a_st, b_end=self.nodeNumList()
       
        fig, axes =plt.subplots(nrows=3, ncols=1,figsize=(10,10))
        # fig.tight_layout()
        
        trussDraw(xco, yco,a_st, b_end,self.truss_type, self.unit ,ax=axes[0]) 
        #draw loads
        for key in self.pointLoads:
            fx=self.pointLoads[key][0]
            fy=self.pointLoads[key][1]
            trussPointLoad(xco[key-1], yco[key-1], loadx=fx ,loady=fy,loadDraw=self.span_width, ax=axes[0], unit=self.unit)  

        trussResultsDraw(xco, yco,dispmat,a_st, b_end,'Displacement' ,ax=axes[1])
        trussElemForceDraw(xco, yco,eforce,a_st, b_end,'Member forces of deflected truss', self.unit ,ax=axes[2])
        # Support Reaction 
        for key in self.supports.values():
            key=key[1]
            fx=forceresult[2*(key-1)]
            fy=forceresult[2*(key-1)+1]
            trussReaction(xco[key-1], yco[key-1], loadx=fx ,loady=fy,loadDraw=self.span_width, ax=axes[2], unit=self.unit)
        # Add support to all
        for ax in axes: 
            for code, node in self.supports.values():
                node=node-1  
                if code== '010':
                    trussRollerSupport(xco[node],yco[node],loadDraw=self.span_width, ax=ax)  
                if code == '110':
                    trussPinnedSupport(xco[node],yco[node],loadDraw=self.span_width, ax=ax)
                if code== '100':
                    trussRollerSupporty(xco[node], yco[node], loadDraw=self.span_width,ax=ax)  
        
        
        # Take off the spines
        for i in range(0,3):
            axes[i].tick_params(left=False, bottom=False,labelleft=False, labelbottom=False)
            axes[i].spines['right'].set_visible(False)
            axes[i].spines['top'].set_visible(False)
            axes[i].spines['bottom'].set_visible(False)
            axes[i].spines['left'].set_visible(False)
        # save image to text
        figfile = BytesIO()
        plt.savefig(figfile, format='png')
        figfile.seek(0)  # rewind to beginning of file
        figdata_png = base64.b64encode(figfile.getvalue())
        figdata_png=figdata_png.decode('utf-8')
        # plt.show()
        return figdata_png, GSM, dispmat, forceresult, elstrain, elstress , eforce


# truss1=truss(truss_type='Howe Bridge', numSpans=10,span_width=10, truss_height=10, A=0.5, unit='SI( N  ,m ,C)')
# truss1.set_E(29000)
# truss1.set_support(support_dof='110', node_num=1)
# truss1.set_support(support_dof='010', node_num=4)
# # for i in range(1,1):
# truss1.set_pointLoad(node_num=2, nodeLoadx=0, nodeLoady=0)
# print(truss1.structure_id)
# truss1.plot_results()
# plt.show()
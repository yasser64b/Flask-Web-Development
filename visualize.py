import matplotlib.pyplot as plt
import matplotlib.patches as patches 
import numpy as np
import itertools

def beamDraw(l=None,ax=None, unit=None):
    dt=0.05
    ax.plot([0,l], [0,0], 'green', lw=8)
    ax.plot([0-dt,l+dt], [-dt,-dt], 'k', lw=2)
    ax.plot([0-dt,l+dt], [dt,dt], 'k', lw=2)
    ax.set_ylim([-1,3])
    p1 = patches.FancyArrowPatch((0, -0.5), (l, -0.5), color='hotpink', arrowstyle='<->', mutation_scale=20)
    ax.add_patch(p1)
    if unit=='SI( N  ,m ,C)':
        ax.annotate(str(l) +' m', (l/2 , -0.75), fontsize=12 ,color='red', rotation=0,zorder=10)
    else:
        ax.annotate(str(l) +' ft', (l/2 , -0.75), fontsize=12 ,color='red', rotation=0,zorder=10)

def fixedSupport(loc, ax=None):
    ''' This function creat fixed support for beams '''
    x=loc
    if x==0:   
        support=patches.Rectangle(xy=(x-0.4,-0.5), width=0.4, height=1, color='blue', fill='False', hatch='//////')
        ax.add_patch(support)
    else:
        support=patches.Rectangle(xy=(x,-0.5), width=0.4, height=1,  color='blue',fill='False', hatch='//////')
        ax.add_patch(support)

def rotateFixedSupport(loc, ax=None):
    ''' This function creat rotateFixed support for beams '''
    x=loc
    if x==0:   
        support=patches.Rectangle(xy=(x-0.1,-0.5), width=0.1, height=1, color='blue', fill='False', hatch='//////')
        support1=patches.Rectangle(xy=(x-0.3,-0.5), width=0.1, height=1, color='blue', fill='False', hatch='//////')
        ax.add_patch(support)
        ax.add_patch(support1)
    else:
        support=patches.Rectangle(xy=(x,-0.5), width=0.1, height=1,  color='blue',fill='False', hatch='//////')
        support1=patches.Rectangle(xy=(x+0.2,-0.5), width=0.1, height=1,  color='blue',fill='False', hatch='//////')
        ax.add_patch(support)
        ax.add_patch(support1)


def rollerSupport(loc, ax=None):
    ''' This function creates roller support for beams '''

    dt=0.3
    dr=0.4
    x=loc
    support=patches.Polygon(([x,0-0.1], [x-dt, -dt], [x+dt, -dt]), color='blue', hatch='////')
    ax.add_patch(support)
    support2=patches.Polygon(([x-dt, -dr], [x+dt, -dr]), color='blue', hatch='////')
    ax.add_patch(support2)


def pinnedSupport(loc, ax=None):
    ''' This function creat pinned support for beams
    supportLocation='right' or  'left' '''

    dt=0.3
    x=loc
    support=patches.Polygon(([x,0-0.1], [x-dt, -dt], [x+dt, -dt]), color='blue', hatch='////')
    ax.add_patch(support)

def hing(loc, ax=None):
    ''' This function creat fixed support for beams
    supportLocation='right' or  'left' '''
    x=loc
    support=patches.Circle([x,0],0.2, color='blue', edgecolor='black',zorder=10)
    ax.add_patch(support)


def pointLoad(loc, load=10, ax=None, unit=None):
    ''' This function create point loads on beam'''

    # load_ratio=load/1000
    load_ratio=1
    x=loc
    l=load_ratio
    L=load
    support=patches.Arrow(x,l, 0, -l, width=0.3, color='red',zorder=10)
    ax.add_patch(support)
    if unit== 'SI( N  ,m ,C)':
        ax.annotate(str(L)+'N', (1.05*x,l), fontsize=12 ,color='red', rotation=-90,zorder=10)
    else: 
        ax.annotate(str(L)+' k', (1.05*x,l), fontsize=12 ,color='red', rotation=-90,zorder=10)


def momentLoad(loc=2, load=10, ax=None, unit=None):
    ''' This function create point moment on beam'''
    
    load_ratio=1
    x=loc
    l=load_ratio
    L=load
    ax.plot(x,0, color='pink', marker='o', markersize=3, alpha=0.8)
    if L<0:
        ax.plot(x, 0 , marker=r'$\circlearrowleft$',ms=50, lw=0.1, color='pink',markeredgewidth=0.01, alpha=0.8 )
    else:
        ax.plot(x, 0 , marker=r'$\circlearrowright$',ms=50, lw=0.1, color='pink',markeredgewidth=0.01,alpha=0.8)
    if unit== 'SI( N  ,m ,C)':
        ax.annotate(str(L)+'N-m', (1.05*x,abs(l)), fontsize=12 ,color='magenta', rotation=-90,zorder=10)
    else:
        ax.annotate(str(L)+'k-in', (1.05*x,abs(l)), fontsize=12 ,color='magenta', rotation=-90,zorder=10)

def distributedLoad(locLoad=[0,10, 5,10], ax=None, unit=None):
    ''' This function create distributed loads on beam'''
    locs=locLoad[0:2]
    load=locLoad[2:4]
    if load[0]==0:
        if load[1]==0:
            load_ratio=[0,0]
        elif load[1] !=0:
            load_ratio=[0,1]
    elif load[1]==0:
        if load[0]==0:
            load_ratio=[0,0]
        elif load[0] !=0:
            load_ratio=[1,0]
    else: 
        if load[0]==load[1]:
            load_ratio=[1,1]
        elif load[0]>load[1]:
            load_ratio=[1,0.5]
        elif load[0]<load[1]:
            load_ratio=[0.5,1]

    if len(locs)>0:         
        ax.plot(locs, load_ratio, 'purple')

        load_new=np.linspace(load_ratio[0], load_ratio[1], num=8)
        locs_new=np.linspace(locs[0], locs[1], num=8)
        
        for x,l in zip(locs_new,load_new):
            support=patches.Arrow(x,l, 0, -l, width=0.1, color='purple',zorder=10)
            ax.add_patch(support)
        

        for x,l,L in zip(locs,load_ratio,load):
            if L !=0:
                if unit=='SI( N  ,m ,C)':
                    ax.annotate(str(L)+' N', (x,1.15*l), fontsize=12 ,color='purple', rotation=-90,zorder=10)
                else: 
                    ax.annotate(str(L)+' k', (x,1.15*l), fontsize=12 ,color='purple', rotation=-90,zorder=10)




# ##################################### COLUMN Visualization Section ######################################################

def columnDraw(l=None,ax=None):
    dt=0.03
    ax.plot( [0,0],[0,l], 'green', lw=8)
    ax.plot( [-dt,-dt],[l+dt,0-dt], 'k', lw=2)
    ax.plot( [dt,dt],[l+dt, 0-dt], 'k', lw=2)
    # ax.set_xlim([-0.5,0.5])
    ax.set_ylim([-1,l+5])

def colFixedSupport(loc, ax=None):
    ''' This function creat fixed support for beams '''
    y=loc
    if y==0:   
        support=patches.Rectangle(xy=(-0.2, y-0.4), width=0.4, height=0.3, color='blue', fill='False', hatch='//////')
        ax.add_patch(support)
    else:
        support=patches.Rectangle(xy=(-0.2, y), width=0.4, height=0.3,  color='blue',fill='False', hatch='//////')
        ax.add_patch(support)

def colRotateFixedSupport(loc, ax=None):
    ''' This function creat rotateFixed support for beams '''
    y=loc
    if y==0:   
        support=patches.Rectangle(xy=(-0.2, y-0.5), width=0.4, height=0.25, color='blue', fill='False', hatch='//////')
        support1=patches.Rectangle(xy=(-0.2,y-0.1), width=0.4, height=0.1, color='blue', fill='False', hatch='//////')
        ax.add_patch(support)
        ax.add_patch(support1)
    else:
        support=patches.Rectangle(xy=(-0.2, y), width=0.4, height=0.1,  color='blue',fill='False', hatch='//////')
        support1=patches.Rectangle(xy=(-0.2,y+0.2), width=0.4, height=0.25,  color='blue',fill='False', hatch='//////')
        ax.add_patch(support)
        ax.add_patch(support1)


def colRollerSupport(loc, ax=None):
    ''' This function creates roller support for beams '''

    dt=0.3
    dr=0.35
    y=loc
    support=patches.Polygon(([0, y], [-dt, y-dt], [-dt, y+dt]), color='blue', hatch='////')
    ax.add_patch(support)
    support2=patches.Polygon(([-dr,y-dt], [-dr,y+dt]), color='blue', hatch='////')
    ax.add_patch(support2)


def colDubleRollerSupport(loc, ax=None):
    ''' This function creates roller support for beams '''

    dt=0.3
    dr=0.35
    y=loc

    support=patches.Polygon(([-0.05, y], [-dt, y-dt], [-dt, y+dt]), color='blue', hatch='////')
    ax.add_patch(support)
    support2=patches.Polygon(([-dr,y-dt], [-dr,y+dt]), color='k', hatch='////')
    ax.add_patch(support2)

    support3=patches.Polygon(([0.05, y], [+dt, y+dt], [dt, y-dt]), color='blue', hatch='////')
    ax.add_patch(support3)
    support4=patches.Polygon(([dr,y-dt], [dr,y+dt]), color='k', hatch='////')
    ax.add_patch(support4)
    
    y=y-0.5
    support5=patches.Polygon(([-0.05, y], [-dt, y-dt], [-dt, y+dt]), color='blue', hatch='////')
    ax.add_patch(support5)
    support6=patches.Polygon(([-dr,y-dt], [-dr,y+dt]), color='k', hatch='////')
    ax.add_patch(support6)

    support7=patches.Polygon(([0.05, y], [+dt, y+dt], [dt, y-dt]), color='blue', hatch='////')
    ax.add_patch(support7)
    support8=patches.Polygon(([dr,y-dt], [dr,y+dt]), color='k', hatch='////')
    ax.add_patch(support8)


def colPinnedSupport(loc, ax=None):

    ''' This function creat pinned support for beams
    supportLocation='right' or  'left' '''

    dt=0.3
    y=loc
    support=patches.Polygon(([0, y], [-dt, y-dt], [-dt, y+dt]), color='blue', hatch='////')
    # support=patches.Polygon(([x,0-0.1], [x-dt, -dt], [x+dt, -dt]), color='blue', hatch='////')
    ax.add_patch(support)


def colPointLoad(loc, load=10, ax=None, unit=None):
    ''' This function create point loads on beam'''

    # load_ratio=load/1000
    load_ratio=2
    y=loc
    l=load_ratio
    L=load
    support=patches.Arrow(0,l+y, 0, -l+0.2, width=0.08, color='red',zorder=10)
    ax.add_patch(support)
    if unit== 'SI( N  ,m ,C)':
        ax.annotate(str(L)+'N', (-0.15,y+3), fontsize=12 ,color='red', rotation=90,zorder=10)
    else: 
        ax.annotate(str(L)+' kips', (-0.15,y+3), fontsize=12 ,color='red', rotation=90,zorder=10)

def colPointLoadDeformed(loc,Dx, load=10, ax=None, unit=None):
    ''' This function create point loads on beam'''

    # load_ratio=load/1000
    load_ratio=2
    y=loc
    l=load_ratio
    L=load
    support=patches.Arrow(Dx,l+y, 0, -l+0.2, width=0.2, color='red',zorder=10)
    ax.add_patch(support)
    if unit== 'SI( N  ,m ,C)':
        ax.annotate(str(L)+'N', (Dx-0.6,y+3), fontsize=12 ,color='red', rotation=90,zorder=10)
    else: 
        ax.annotate(str(L)+' kips', (Dx-0.6,y+3), fontsize=12 ,color='red', rotation=90,zorder=10)



# ##################################### TRUSS Visualization Section ######################################################

def trussDraw(xco =[], yco=[],a_st=[], b_end=[], title_truss='Title' ,unit=None, ax=None):
    limx = max(xco)
    limy = max(yco)
    n=len(xco)/2

    ax.set_xlim([-0.3*limx , 1.1*limx])
    ax.set_ylim([-0.5*limy , 1.3*limy])
    ax.set_title(title_truss)
    ax.set_aspect(aspect=1, adjustable='box', anchor='C')
    for i in range (len(a_st)):
        x1,y1,x2,y2 = xco[a_st[i]-1], yco[a_st[i]-1], xco[b_end[i]-1], yco[b_end[i]-1]
        ax.plot([x1,x2],[y1,y2], color='lightgreen')
        ax.annotate(str(i+1), (0.5*(x1+x2),0.5*(y1+y2)), fontsize=9 ,color='darkgreen', rotation=0,zorder=10)
    
    # Dimension lines
    p1 = patches.FancyArrowPatch((-0.1*limx, 0), (-0.1*limx, limy), color='hotpink', arrowstyle='<->', mutation_scale=20)
    ax.add_patch(p1)
    p2 = patches.FancyArrowPatch((0,-0.3*limy), (limx, -0.3*limy), color='hotpink', arrowstyle='<->', mutation_scale=20)
    ax.add_patch(p2)
    if unit=='US(kips,ft,F)':
        ax.annotate( str(limy)+' ft' , xy=(-0.09*limx, limy/2), color='k', rotation=0)
        ax.annotate(str(int(n))+' @ '+str(limx/n)+'='+str(limx)+' ft', xy=(0.3*limx, -0.5*limy), color='k', rotation=0)
    else:
        ax.annotate(str(limy)+' m' , xy=(-0.09*limx, limy/2), color='k', rotation=0)
        ax.annotate(str(int(n))+' @ '+str(limx/n)+'='+str(limx)+' m', xy=(0.3*limx, -0.5*limy), color='k', rotation=0)
    
    # Node NUmbering 
    i=0
    for x,y in zip(xco, yco):
        i +=1
        ax.plot(x,y,marker='o', color='k', markersize=2)
        # if y==0:
        #     ax.annotate(str(i), (x,y-1.5), fontsize=8 ,color='k', rotation=0,zorder=10)
        # else: 
        #     ax.annotate(str(i), (x,y+0.5), fontsize=8 ,color='k', rotation=0,zorder=10)

def trussResultsDraw(xco =[], yco=[],dispmat=[],a_st=[], b_end=[], title_truss='Title' , ax=None):
    
    limx = max(xco)
    limy = max(yco)

    ax.set_xlim([-0.3*limx , 1.1*limx])
    ax.set_ylim([-0.5*limy , 1.3*limy])
    ax.set_title(title_truss)
    ax.set_aspect('equal', adjustable='box', anchor='C')
    # Node NUmbering 
    i=0
    for x,y in zip(xco, yco):
        i +=1
        ax.plot(x,y,marker='o', color='k',markersize=2)
        if y==0:
            ax.annotate(str(i), (x,y-1.5), fontsize=8 ,color='k', rotation=0,zorder=10)
        else: 
            ax.annotate(str(i), (x,y+0.5), fontsize=8 ,color='k', rotation=0,zorder=10)
    
    # Draw Displaced Truss
    dispmat=dispmat.flatten()
    dispmat=1*dispmat/max(max(dispmat), -min(dispmat))

    xco_D=xco+dispmat[::2]
    yco_D=yco-dispmat[1::2]

    for i in range (len(a_st)):
        x1,y1,x2,y2 = xco[a_st[i]-1], yco[a_st[i]-1], xco[b_end[i]-1], yco[b_end[i]-1]
        ax.plot([x1,x2],[y1,y2], color='lightgreen')
        
        x1d,y1d,x2d,y2d = xco_D[a_st[i]-1], yco_D[a_st[i]-1], xco_D[b_end[i]-1], yco_D[b_end[i]-1]
        ax.plot([x1d,x2d],[y1d,y2d], 'r--')

        # ax.annotate(str(i+1), (0.5*(x1+x2),0.5*(y1+y2)), fontsize=9 ,color='darkgreen', rotation=0,zorder=10)
    
    
    i=0
    for x,y in zip(xco, yco):
        ax.plot(x,y,marker='o', color='k',markersize=2)
        dx1=dispmat[2*i]
        dy1=dispmat[2*i+1]
        ax.plot(x+dx1,y-dy1,marker='o', color='red',markersize=2)
        i +=1

def trussElemForceDraw(xco =[], yco=[],eforce=[],a_st=[], b_end=[], title_truss='Title', unit='SI' , ax=None):
    
    limx = max(xco)
    limy = max(yco)

    ax.set_xlim([-0.3*limx , 1.1*limx])
    ax.set_ylim([-0.5*limy , 1.4*limy])
    ax.set_title(title_truss)
    ax.set_aspect('equal', adjustable='box', anchor='C')
    eforce=eforce.flatten()
    eforce=-1*eforce

    for i in range (len(a_st)):
        x1,y1,x2,y2 = xco[a_st[i]-1], yco[a_st[i]-1], xco[b_end[i]-1], yco[b_end[i]-1]
        ax.plot([x1,x2],[y1,y2], color='lightgreen')
        X=x2-x1
        XX=abs(x2-x1)
        if x2-x1==0:
             X=0.000000000001

        ax.annotate(str(round(eforce[i],1)), (0.5*(x1+x2)-0.1*XX,0.5*(y1+y2)), fontsize=9 ,color='red', rotation=180*np.arctan((y2-y1)/(X))/np.pi,zorder=10)
        # if unit== 'SI( N  ,m ,C)':
            # ax.annotate(str(round(eforce[i],1))+ ' N', (0.5*(x1+x2)-0.1*XX,0.5*(y1+y2)), fontsize=9 ,color='red', rotation=180*np.arctan((y2-y1)/(X))/np.pi,zorder=10)
    
        # else:
        #     ax.annotate(str(round(eforce[i],1))+ ' k', (0.5*(x1+x2)-0.1*XX,0.5*(y1+y2)), fontsize=9 ,color='red', rotation=180*np.arctan((y2-y1)/(X))/np.pi,zorder=10)
    
    for x,y in zip(xco, yco):
        ax.plot(x,y,marker='o', color='k',markersize=2)






def trussRollerSupport(xco, yco,loadDraw=1, ax=None):
    ''' This function creates roller support for truss '''
    x=xco
    y=yco
    
    dt=loadDraw/5
    dr=loadDraw/4

    support=patches.Polygon(([x,y], [x-dt, y-dt], [x+dt, y-dt]), color='SkyBlue', hatch='////')
    ax.add_patch(support)
    support2=patches.Polygon(([x-dt, y-dr], [x+dt, y-dr]), color='SkyBlue', hatch='////')
    ax.add_patch(support2)

def trussPinnedSupport(xco, yco, loadDraw=1, ax=None):
    x=xco
    y=yco

    dt=loadDraw/5
    dr=loadDraw/4
    
    support=patches.Polygon(([x,y], [x-dt, y-dr], [x+dt, y-dr]), color='SkyBlue', hatch='////')
    ax.add_patch(support)


def trussRollerSupporty(xco, yco, loadDraw=1,ax=None):
 
    x=xco
    y=yco

    dt=loadDraw/5
    dr=loadDraw/4
    support=patches.Polygon(([x, y], [x-dt, y-dt], [x-dt, y+dt]), color='blue', hatch='////')
    ax.add_patch(support)
    support2=patches.Polygon(([x-dr,y-dt], [x-dr,y+dt]), color='blue', hatch='////')
    ax.add_patch(support2)




def trussPointLoad(xco, yco, loadx=10,loady=10,loadDraw=1, ax=None, unit=None):
    ''' This function create point loads on Truss nodes'''

    x=xco
    y=yco

    l=loadDraw/2
    Lx=loadx
    Ly=loady
    if Lx !=0:
        supportx=patches.Arrow(x-0.5*l,y, 0.5*l,0, width=l/10, color='red',zorder=10)
        ax.add_patch(supportx)
    if Ly !=0:
        supporty=patches.Arrow(x,y, 0, -0.5*l, width=l/10, color='red',zorder=10)
        ax.add_patch(supporty)

    if unit== 'SI( N  ,m ,C)':
        if Lx !=0:
            ax.annotate(str(Lx)+'N', (x-0.5*l,y+l/10), fontsize=8 ,color='red', rotation=0,zorder=10)
        if Ly !=0:
            ax.annotate(str(Ly)+'N', (x-l/3,y-0.5*l), fontsize=8 ,color='red', rotation=90,zorder=10)
    else:
        if Lx !=0:
            ax.annotate(str(Lx)+'k', (x-0.5*l,y+l/10), fontsize=8 ,color='red', rotation=0,zorder=10)
        if Ly !=0:
            ax.annotate(str(Ly)+'k', (x-l/3,y-0.5*l), fontsize=8 ,color='red', rotation=90,zorder=10)

def trussReaction(xco, yco, loadx=10,loady=10,loadDraw=1, ax=None, unit=None):
    ''' This function create point loads on Truss nodes'''

    x=xco
    y=yco
    l=loadDraw/2
    Lx=1*round(loadx[0],1)
    Ly=-1*round(loady[0],1)
    supportx=patches.Arrow(x-0.5*l,y, 0.5*l,0, width=l/5, color='k',zorder=10)
    ax.add_patch(supportx)
    supporty=patches.Arrow(x,y-0.7*l, 0, 0.7*l, width=l/5, color='k',zorder=10)
    ax.add_patch(supporty)
    ax.annotate(str(Lx), (x-l,y-l/4), fontsize=8 ,color='black', rotation=0,zorder=10)
    ax.annotate(str(Ly), (x+l/3,y-0.5*l), fontsize=8 ,color='black', rotation=90,zorder=10)

    # if unit== 'SI( N  ,m ,C)':
    #         ax.annotate(str(Lx)+'N', (x-l,y-l/4), fontsize=8 ,color='black', rotation=0,zorder=10)
    #         ax.annotate(str(Ly)+'N', (x+l/3,y-0.5*l), fontsize=8 ,color='black', rotation=90,zorder=10)
    # else:
    #         ax.annotate(str(Lx)+'k', (x-l,y-l/4), fontsize=8 ,color='black', rotation=0,zorder=10)
    #         ax.annotate(str(Ly)+'k', (x+l/3,y-0.5*l), fontsize=8 ,color='black', rotation=90,zorder=10)





# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 09:57:51 2023

@author: oyvinpet
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 12:36:35 2022

@author: oyvinpet
"""

#%%

import sys
import numpy as np
import h5py
import matplotlib.pyplot as plt

sys.path.append('C:/Cloud/OD_OWP/Work/Python/Github')

# import abaqustools
from abaqustools import abq,gen

from abaqustools import odbexport


#%%

InputFileName='Testray_05.inp'

fid=open(InputFileName,'w')

L=100
N_node=100
nodenum_base=[1000]
elnum_base=[1000]
partname='Part_beam'
assemblyname='Assembly_beam'


x_node=np.linspace(0,L,N_node)
y_node=x_node*0
z_node=x_node*0

nodenum=nodenum_base[0]+np.arange(1,len(x_node)+1).astype(int)
elnum=elnum_base[0]+np.arange(1,len(x_node)).astype(int)

nodematrix_01=np.column_stack((nodenum,x_node,y_node,z_node))
elmatrix_01=np.column_stack((elnum,nodenum[:-1],nodenum[1:]))

gen.part(fid,partname)

gen.node(fid,nodematrix_01,'Nodes_01')

gen.element(fid,elmatrix_01,'B31','Elements_01')

gen.nset(fid, 'End_01', [nodenum[0],nodenum[-1]])
gen.nset(fid, 'Mid', [nodenum[int(N_node/2)]])

gen.beamgeneralsection(fid,'Elements_01',7850,[0.2 , .0003 , 0 , .0001 , .01],[0,1,0],[210e9,81e9])
# gen.Line(fid,'*DAMPING, ALPHA=0.03,BETA=0.02')

gen.partend(fid)

gen.comment(fid,'ASSEMBLY',True)

gen.assembly(fid,assemblyname)

gen.instance(fid,partname,partname)

gen.instanceend(fid)

gen.assemblyend(fid)


gen.step(fid,'NLGEO=NO, NAME=STEP1','Static')

gen.static(fid,'1e-3, 1, 1e-6, 1')

#gen.gravload(fid,'new',[''],9.81)

gen.boundary(fid,'new','End_01',[1,6,0],partname)
gen.boundary(fid,'new','Nodes_01',[2,2,0],partname)

gen.fieldoutput(fid,'NODE',['U' , 'RF' , 'COORD'],'','FREQUENCY=100')
gen.fieldoutput(fid,'ELEMENT',['SF'],'','FREQUENCY=100')

gen.stepend(fid)

gen.step(fid,'NAME=STEP_MODAL','')
gen.frequency(fid,10,'mass')
gen.fieldoutput(fid,'NODE',['U' , 'COORD'],'','')
gen.fieldoutput(fid,'ELEMENT',['SF'],'','')
gen.stepend(fid)

gen.step(fid,'NAME=STEP_COMPLEXMODAL','')
gen.Line(fid,'*COMPLEX FREQUENCY')
gen.Line(fid,'10')
gen.Line(fid,'*GLOBAL DAMPING, ALPHA=0.03,BETA=0.02')

gen.fieldoutput(fid,'NODE',['U' , 'COORD'],'','')
gen.fieldoutput(fid,'ELEMENT',['SF'],'','')
gen.stepend(fid)

#gen.step(fid,'NAME=STEPD','Dyn')
#gen.Line(fid,'*DYNAMIC,ALPHA=0,INITIAL=YES') #
#gen.Line(fid,'0.01,20,0.001,0.05') #ALPHA=0,INITIAL=YES
#gen.fieldoutput(fid,'NODE',['U' , 'COORD'],'','')
#gen.Dload(fid,'DELETE','','','')
#gen.stepend(fid)


gen.step(fid,'NAME=STEPD','Dyn')
gen.Line(fid,'*MODAL DYNAMIC') #
gen.Line(fid,'0.1,250') #ALPHA=0,INITIAL=YES



gen.Line(fid,'*AMPLITUDE,NAME=MYAMP,DEFINITION=TABULAR') #
gen.Line(fid,'0,0') #
gen.Line(fid,'1,1') #
gen.Line(fid,'1.1,0') #

gen.Line(fid,'*CLOAD,AMPLITUDE=MYAMP')
gen.Line(fid,partname + '.mid' + ',3,-100')
gen.Dload(fid,'DELETE','','','')

gen.fieldoutput(fid,'NODE',['U' , 'COORD'],'','')

gen.historyoutput(fid)
gen.historyoutputnode(fid,'U',partname + '.mid')
    
gen.Dload(fid,'DELETE','','','')
gen.stepend(fid)


fid.close()



#%%
foldername=r'C:\Cloud\OD_OWP\Work\Python\Github\abaqustools\develop\testrayleigh'

inputname=InputFileName

abq.runjob(foldername, inputname)

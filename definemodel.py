import torch
import time
from torch.autograd import Variable
import numpy as np

f = 0.1 #fraction of active KCs
M = 20 #number of MBONs
D = 20 #number of DANs
U = 2 #size of input vector
R = 1 #size of readout vector
O = 60 #number of "other" (feedback) neurons
S = 200 #size of input vector

dt = .5 #timestep
tau = 5 #stdp time constant
tauw = 5 #stdp time constant
stdpfac = 1. #scaling factor for STDP
wmax = 1./(S*f) #max weight
pvalid = 0.5 #fraction of trials that are "valid" (no CS/US omission or substitution)
minit = 0. #initial MBON activity
oinit = 0.1 #initial "other" neuron activity
dinit = 0.1 #initial DAN activity

dus = int(2/dt) #time between CS/US
cslen = int(2/dt) #CS presentation length
uslen = int(2/dt) #US presentation length
T = int(100/dt) #trial length
resettimes = [int(30/dt),int(60/dt)]

def initrand(X,Y,scalefac=.5): #random weight initialization
    return (scalefac*np.random.standard_normal([X,Y])/np.sqrt(Y)).astype(np.float32)

Jmd = Variable(torch.from_numpy(np.eye(M).astype(np.float32)),requires_grad=False)

#trained variables
Jmm = Variable(torch.from_numpy(initrand(M,M)),requires_grad=True)
Jmo = Variable(torch.from_numpy(initrand(M,O)),requires_grad=True)
Jdm = Variable(torch.from_numpy(initrand(D,M)),requires_grad=True)
Jdd = Variable(torch.from_numpy(initrand(D,D)),requires_grad=True)
Jdo = Variable(torch.from_numpy(initrand(D,O)),requires_grad=True)
Jom = Variable(torch.from_numpy(initrand(O,M)),requires_grad=True)
Jod = Variable(torch.from_numpy(initrand(O,D)),requires_grad=True)
Joo = Variable(torch.from_numpy(initrand(O,O)),requires_grad=True)
bm  = Variable(torch.from_numpy(.1*np.ones([M,1]).astype(np.float32)),requires_grad=True)
bd  = Variable(torch.from_numpy(.1*np.ones([D,1]).astype(np.float32)),requires_grad=True)
bo  = Variable(torch.from_numpy(.1*np.ones([O,1]).astype(np.float32)),requires_grad=True)
wou = Variable(torch.from_numpy(np.random.standard_normal([O,U]).astype(np.float32)),requires_grad=True)
wrm = Variable(torch.from_numpy(initrand(R,M,1)),requires_grad=True)

train_vars = [Jmm,Jmo,Jdm,Jdd,Jdo,Jom,Jod,Joo,bm,bd,bo,wou,wrm]

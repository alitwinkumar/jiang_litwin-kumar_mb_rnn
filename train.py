import torch
import time
from torch.autograd import Variable
import numpy as np
import matplotlib.pyplot as plt

doplot = True #show output during training
norecur = False #no recurrent MBON output circuitry
firstorder_only = False #only train for first-order trials
dostdp = True #do dopamine-dependent STDP updates

B = 30 #batch size
alphada = 0.01 #regularization parameter for dopamine activity

probs = dict()
probs["valid"] = 0.5
if firstorder_only:
    Nepochs = 2000
    probs["firstorder"] = 1.
    probs["secondorder"] = 0.
    probs["extinction"] = 0.
else:
    Nepochs = 5000
    probs["firstorder"] = 0.
    probs["secondorder"] = 0.5
    probs["extinction"] = 0.5

lr = 0.001 * np.ones(Nepochs) #learning rate
Nepochspc = max(int(Nepochs/100),1) #plot training status after this interval

exec(open("definemodel.py").read())
exec(open("plotutils.py").read())
if norecur:
    Jmm.data[:] = 0
    Jmo.data[:] = 0
    Jdm.data[:] = 0
    Jdd.data[:] = 0
    Jom.data[:] = 0
    Jod.data[:] = 0
    Joo.data[:] = 0
    train_vars = [Jdo,bm,bd,bo,wou,wrm]

exec(open("gentrials.py").read())

opt = torch.optim.RMSprop(train_vars,lr=lr[0])

track_loss = np.zeros(Nepochs)

lastt = time.time()
for ei in range(Nepochs):
    for g in opt.param_groups:
        g['lr'] = lr[ei]

    s0,u0,rtarg0,tinfo = genrandtrials(B,probs)

    m0,d0,o0,w0,sbar0,dastdpbar0 = geninitialcond(B)

    exec(open("runmodel.py").read())

    loss_err = torch.sum(torch.pow(r-rtarg,2))/B
    loss_da = alphada*dacost/B
    loss = loss_err + loss_da
    track_loss[ei] = loss

    loss.backward()
    opt.step()
    opt.zero_grad()

    if (ei % Nepochspc) == 0:
        if doplot:
            plt.clf()
            plt.subplot(311)
            if ei > 0:
                plt.semilogy(track_loss[:ei])
            plt.xlim(0,Nepochs)
            plt.xlabel("epoch")
            plt.ylabel("loss")

            plt.subplot(312)
            plottarg(r.detach().numpy()[:,:,0],rtarg.detach().numpy()[:,:,0],tinfo[0])
            plt.ylabel("valence")

            plt.subplot(313)
            plotunits(da[:,:,0],tinfo[0])
            plt.ylabel("DAN activity")
            plt.xlabel("time")

            plt.tight_layout()

            plt.pause(.0001)
            plt.show()

        curt = time.time()
        print("\r" + str(int(ei/Nepochspc)) + "%, ", np.round(curt-lastt,2), "seconds", end="")
        lastt = curt



import numpy as np
import matplotlib.pyplot as plt

def plotfill(tinfo,hmin,hmax):
    Acol = "b"
    Bcol = "c"
    Ccol = "m"
    if tinfo["valence"] > 0:
        UScol = "g"
    else:
        UScol = "r"

    tA = tinfo["tA"]
    tUS = tinfo["tUS"]
    ttest = tinfo["ttest"]

    if tinfo["type"] == "firstorder":
        plt.fill_between([tA,tA+cslen],[hmin,hmin],[hmax,hmax],color=Acol,alpha=0.2,linewidth=0)
        if tinfo["doC"]:
            plt.fill_between([ttest,ttest+cslen],[hmin,hmin],[hmax,hmax],color=Ccol,alpha=0.2,linewidth=0)
        else:
            plt.fill_between([ttest,ttest+cslen],[hmin,hmin],[hmax,hmax],color=Acol,alpha=0.2,linewidth=0)
        if tinfo["doUS"]:
            plt.fill_between([tUS,tUS+uslen],[hmin,hmin],[hmax,hmax],color=UScol,alpha=0.2,linewidth=0)
    elif tinfo["type"] == "secondorder":
        tA2 = tinfo["tA2"]
        tB = tinfo["tB"]
        plt.fill_between([tA,tA+cslen],[hmin,hmin],[hmax,hmax],color=Acol,alpha=0.2,linewidth=0)
        if tinfo["doA2"]:
            plt.fill_between([tA2,tA2+cslen],[hmin,hmin],[hmax,hmax],color=Acol,alpha=0.2,linewidth=0)
        if tinfo["doC"]:
            plt.fill_between([ttest,ttest+cslen],[hmin,hmin],[hmax,hmax],color=Ccol,alpha=0.2,linewidth=0)
        else:
            plt.fill_between([ttest,ttest+cslen],[hmin,hmin],[hmax,hmax],color=Bcol,alpha=0.2,linewidth=0)
        plt.fill_between([tB,tB+cslen],[hmin,hmin],[hmax,hmax],color=Bcol,alpha=0.2,linewidth=0)
        if tinfo["doUS"]:
            plt.fill_between([tUS,tUS+uslen],[hmin,hmin],[hmax,hmax],color=UScol,alpha=0.2,linewidth=0)
    elif tinfo["type"] == "extinction":
        tA2 = tinfo["tA2"]
        tUS2 = tinfo["tUS2"]
        if tinfo["doA"]:
            plt.fill_between([tA,tA+cslen],[hmin,hmin],[hmax,hmax],color=Acol,alpha=0.2,linewidth=0)
        if tinfo["doA2"]:
            plt.fill_between([tA2,tA2+cslen],[hmin,hmin],[hmax,hmax],color=Acol,alpha=0.2,linewidth=0)
        else:
            plt.fill_between([tA2,tA2+cslen],[hmin,hmin],[hmax,hmax],color=Bcol,alpha=0.2,linewidth=0)
        if tinfo["doUS2"]:
            plt.fill_between([tUS2,tUS2+uslen],[hmin,hmin],[hmax,hmax],color=UScol,alpha=0.2,linewidth=0)
        plt.fill_between([ttest,ttest+cslen],[hmin,hmin],[hmax,hmax],color=Acol,alpha=0.2,linewidth=0)
        if tinfo["doUS"]:
            plt.fill_between([tUS,tUS+uslen],[hmin,hmin],[hmax,hmax],color=UScol,alpha=0.2,linewidth=0)

def plottarg(r,rtarg,tinfo): #plot target valence
    tranges = (np.arange(5,50),np.arange(65,110),np.arange(125,180)) #time intervals to plot

    for trange in tranges:
        plt.plot(trange,r[trange],"gray")
        plt.plot(trange,rtarg[trange],"k")

    if tinfo["valence"] == 1:
        hmin = -.1
        hmax = 1.1
    else:
        hmin = -1.1
        hmax = 0.1

    plotfill(tinfo,hmin,hmax)
    plt.xlim(0,T)
    plt.xticks(())
    plt.yticks(())


def plotunits(r,tinfo): #plot activity of model neurons
    tranges = (np.arange(5,50),np.arange(65,110),np.arange(125,180)) #time intervals to plot
    hdiff = 1.
    N = r.shape[1]
    count = 0
    inds = np.arange(D)
    for ind in inds:
        for trange in tranges:
            plt.plot(trange,r[trange,ind]+hdiff*count,"k")
        count += 1

    hmax = len(inds)*hdiff
    hmin = 0

    plotfill(tinfo,hmin,hmax)

    plt.yticks(())
    plt.xlim(0,T)
    plt.xticks(())
